from typing import Type, List, Tuple

from django.db.models import Model
from django.db.models.fields import BigIntegerField

from lib.config import Config
from lib.signals import versioning_initialized_signal
from lib.versioned_model import VersionedModel
from lib.versioning_options import VersioningOptions


def register(model: Type[Model]):
    def wrapper(options_class: Type[VersioningOptions]):
        # Inject `VersionedModule` within model's bases, right before `Model`
        bfr, aft = split_bases_on_model(*model.__bases__)
        # versioning_class_name = f"{model.__name__}Versioned"

        options = options_class()
        persistence_field = options.get_persistence_field(model)
        version_field = BigIntegerField(default=None, null=True)
        versioning_class = type('VersionedModel', (VersionedModel,), {
            "_versioning_options": options,
            Config.persisted_field_name: persistence_field,
            Config.version_field_name: version_field
        })
        inject_parent_class(bfr, aft, model, versioning_class)
        # TODO: might not be needed
        model.add_to_class(Config.persisted_field_name, persistence_field)
        model.add_to_class(Config.version_field_name, version_field)

        versioning_initialized_signal.send(sender=model)
        return options

    return wrapper


def split_bases_on_model(*bases: Type[object]) -> Tuple[List[Type[object]], List[Type[object]]]:
    bases_before = []
    bases_after = []
    model = None

    for base in bases:
        if base == Model or issubclass(base, Model):
            model = base
        if model is None:
            bases_before.append(base)
        else:
            bases_after.append(base)

    return bases_before, bases_after


def inject_parent_class(bases_before: List[Type[object]], bases_after: List[Type[object]],
                        base_model: Type[Model], injected_base: type) -> None:
    base_model.__bases__ = (*bases_before, injected_base, *bases_after)
