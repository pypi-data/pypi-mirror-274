from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Union

from django.db.models import ForeignKey, Q, Model
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.forms import Field

from lib.config import Config
from lib.versioned_model import VersionedModel

if TYPE_CHECKING:
    from lib.types import VersionedModelType


class ForwardVersionedForeignKeyDescriptor(ForwardManyToOneDescriptor):
    def __set__(self, instance, value):
        original_value = None
        try:
            # We need to trick Django into believing the foreign related field is our persisted_id.
            # However the setter of the `descriptor_class` only receives the value of the foreign field, not the field
            # or instance themselves, therefore we need to override the setter of the `forward_related_accessor_class`
            # This setter is kinda long so it can easily break with future updates, that's why we just override
            # the self.field.related_fields for this call only
            original_value = self.field.related_fields
            self.field.related_fields = [self.replace_related_fields(rhfs, value) for rhfs in self.field.related_fields]
            super(ForwardVersionedForeignKeyDescriptor, self).__set__(instance, value)
        finally:
            if original_value is not None:
                self.field.related_fields = original_value

    @staticmethod
    def replace_related_fields(fields: Tuple[Field, Field], value: Model) -> (
            Tuple)[Union[Field, VersionedForeignKey], Field]:
        lh_field, rh_field = fields
        if isinstance(lh_field, VersionedForeignKey) and isinstance(value, VersionedModel):
            return lh_field, value.persisted_field
        return lh_field, rh_field


class VersionedForeignKey(ForeignKey):

    forward_related_accessor_class = ForwardVersionedForeignKeyDescriptor

    # SuperClass is called within a child function
    # noinspection PyMissingConstructor
    def __init__(
            self,
            to: 'VersionedModelType',
            *args,
            **kwargs,
    ):
        # kwargs["to_field"] = Config.persisted_field_name
        self._reference_model = to
        super(VersionedForeignKey, self).__init__(
            to,
            *args,
            **kwargs,
        )

    def _check_unique_target(self):
        return []

    def get_forward_related_filter(self, obj):
        """
        Return the keyword arguments that when supplied to
        self.model.object.filter(), would select all instances related through
        this field to the remote obj. This is used to build the querysets
        returned by related descriptors. obj is an instance of
        self.related_field.model.
        """
        return {
            "%s__%s" % (self.name, rh_field.name): getattr(obj, rh_field.attname)
            for _, rh_field in self.related_fields
        }

    def get_reverse_related_filter(self, obj):
        """
        Complement to get_forward_related_filter(). Return the keyword
        arguments that when passed to self.related_field.model.object.filter()
        select all instances of self.related_field.model related through
        this field to obj. obj is an instance of self.model.
        """
        foreign_key_value = getattr(obj, self.attname)
        return Q(**{
            Config.persisted_field_name: foreign_key_value
        }) & Q(**{
            Config.version_field_name: None
        })
