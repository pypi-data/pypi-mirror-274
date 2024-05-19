from typing import Type, TYPE_CHECKING, Any

from django.db.models import Field
from django.db.models.signals import post_save

from lib.config import Config

# If this import doesn't happen within TYPE_CHECKING, for some reasons, Django doesn't dectect the
# new field when generating migrations
if TYPE_CHECKING:
    from lib.types import VersionedModelInstance, VersionedModelType


class VersioningField:
    replace_fields = []

    @classmethod
    def of(cls, model, original_field: Type[Field]):
        # We need to import fields to make them discoverable
        # noinspection PyUnresolvedReferences
        import lib.fields
        replace_array = cls.__subclasses__()
        for field in replace_array:
            if original_field in field.replace_fields:
                post_save.connect(cls.post_save, sender=model)
                return field
        raise Exception(f"Persistent field not supported for {original_field}")

    def generate_new_version(self, value: Any) -> Any:
        raise NotImplemented

    # noinspection PyUnusedLocal
    @staticmethod
    def post_save(sender: 'VersionedModelType', instance: 'VersionedModelInstance', created, **kwargs):
        if getattr(instance, '_django_model_versioning_avoid_signal', False):
            return

        field = instance._meta.get_field(Config.persisted_field_name)
        current_value = getattr(instance, field.attname)

        if current_value is not None:
            return

        persistent_key = instance.get_versioning_options().persistence_key

        id_value = getattr(instance, persistent_key)

        setattr(instance, field.attname, id_value)
        instance.save(django_model_versioning_avoid_signal=True)
