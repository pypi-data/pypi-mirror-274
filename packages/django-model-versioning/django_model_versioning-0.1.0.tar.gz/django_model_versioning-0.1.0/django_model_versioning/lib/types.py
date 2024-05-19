from typing import Union, Type

from django.db.models import Model, Field

from lib.versioned_model import VersionedModel
from lib.versioning_field import VersioningField

VersionedModelInstance = Union[Model, VersionedModel]
VersionedModelType = Type[Union[Model, VersionedModel]]
PersistentFieldInstance = Union[Field, VersioningField]
PersistentFieldType = Type[Union[Field, VersioningField]]
