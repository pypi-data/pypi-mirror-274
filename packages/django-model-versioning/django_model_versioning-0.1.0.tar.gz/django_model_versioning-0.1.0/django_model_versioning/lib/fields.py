from uuid import UUID, uuid4

from django.db.models.fields import UUIDField, BigIntegerField, IntegerField, CharField, BigAutoField

from lib.versioning_field import VersioningField


class VersionedBigIntegerField(VersioningField, BigIntegerField):
    replace_fields = [BigIntegerField, BigAutoField]

    def generate_new_version(self, value: int) -> int:
        return value + 1


class VersionedIntegerField(VersioningField, IntegerField):
    replace_fields = [IntegerField]

    def generate_new_version(self, value: int) -> int:
        return value + 1


class VersionedCharField(VersioningField, CharField):
    replace_fields = [CharField]

    def generate_new_version(self, value: str) -> str:
        chunks = value.split('_')

        if len(chunks) > 1 and chunks[-1].isnumeric():
            return f"{"_".join(chunks[:-1])}_{int(chunks[-1]) + 1}"

        return f"{value}_1"


class VersionedUUIDField(VersioningField, UUIDField):
    replace_fields = [UUIDField]

    def generate_new_version(self, value: UUID) -> UUID:
        return uuid4()
