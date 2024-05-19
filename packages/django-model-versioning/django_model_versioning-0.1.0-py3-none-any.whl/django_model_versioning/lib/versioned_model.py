from typing import Optional, TYPE_CHECKING

from django.db import transaction
from django.db.models import Max

from lib.config import Config
from lib.versioning_options import VersioningOptions

if TYPE_CHECKING:
    from lib.types import VersionedModelInstance, PersistentFieldInstance, VersionedModelType


class VersionedModel:
    _versioning_options = None  # type: Optional[VersioningOptions]

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(VersionedModel, self).__init__(*args, **kwargs)
        self._django_model_versioning_original_state = {}
        self.store_original_state()
        self._django_model_versioning_avoid_signal = False

    def save(self: 'VersionedModelInstance', *args, **kwargs):
        self._django_model_versioning_avoid_signal = kwargs.pop('django_model_versioning_avoid_signal', False)
        if self.versioned_fields_changed():
            self.archive_original()
            # Set the primary key to None to generate a new model
            if self._meta.pk.attname != self._versioning_options.persistence_key:
                self.regenerate_persinstance_key()
            setattr(self, self._meta.pk.attname, None)
        super(VersionedModel, self).save(*args, **kwargs)

    def archive_original(self: 'VersionedModelInstance'):
        original = self.__class__.objects.get(id=self.id)
        # We use transavtion.atomic to avoid race conditions when multiple threads attempt to create a new version
        # for this model
        with transaction.atomic():
            new_attr_value = self.__class__.objects.aggregate(
                Max(Config.version_field_name)
            )[f"{Config.version_field_name}__max"] or 0
            setattr(original, Config.version_field_name, new_attr_value + 1)
            original.save()

    def regenerate_persinstance_key(self: 'VersionedModelInstance') -> None:
        current_value = getattr(self, self._versioning_options.persistence_key)
        setattr(self, self._versioning_options.persistence_key,
                self.versioned_field.generate_new_version(current_value))

    def store_original_state(self) -> None:
        if self._versioning_options is None:
            return

        for versioned_field in self._versioning_options.versioned_fields:
            self._django_model_versioning_original_state[versioned_field] = getattr(self, versioned_field, None)

    def versioned_fields_changed(self) -> bool:
        return any(getattr(self, versioned_field) != self._django_model_versioning_original_state.get(versioned_field)
                   for versioned_field in self._versioning_options.versioned_fields)

    @property
    def versioned_field(self: 'VersionedModelInstance') -> 'PersistentFieldInstance':
        return self.get_versioned_field()

    @property
    def persisted_field(self: 'VersionedModelInstance') -> 'PersistentFieldInstance':
        return self.get_persisted_field()

    @classmethod
    def get_versioned_field(cls: 'VersionedModelType') -> 'PersistentFieldInstance':
        return cls._meta.get_field(cls._versioning_options.persistence_key)

    @classmethod
    def get_persisted_field(cls: 'VersionedModelType') -> 'PersistentFieldInstance':
        return cls._meta.get_field(Config.persisted_field_name)

    @classmethod
    def get_versioning_options(cls) -> VersioningOptions:
        if cls._versioning_options is None:
            raise Exception("_versioning_options needs to be defined. "
                            "Did you initialize your model using @register methoid?")
        return cls._versioning_options
