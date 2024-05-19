from typing import Type

from django.db.models import Field, Model


class VersioningOptions:
    versioned_fields = ()
    persistence_key = 'id'

    def __init__(self):
        try:
            self.validate()
        except AssertionError as err:
            raise Exception(f"Invalid versioning options configuration: {err}")

    def validate(self):
        assert self.persistence_key not in self.versioned_fields, "Persistence key cannot be versioned"

    def get_persistence_field(self, model: Type[Model]) -> Field:
        from lib.versioning_field import VersioningField

        persistence_field_origin = model._meta.get_field(self.persistence_key)
        if not isinstance(persistence_field_origin, Field):
            raise TypeError("Persistence field reference should be an instance of django.db.models.Field")

        persistance_field_class = type(persistence_field_origin)

        return VersioningField.of(model, persistance_field_class)(unique=False, null=True, blank=False)
