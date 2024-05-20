import re
from typing import Callable, Type, TypeVar

T = TypeVar('T')


def underscoring_entity_name(entity_name: str):
    return re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', '_', entity_name)


def standardize_entity_name(entity_name: str):
    return f'{underscoring_entity_name(entity_name[: -len("Entity")]).lower()}s'


def Entity() -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        class Settings:
            name = standardize_entity_name(cls.__name__)

        setattr(cls, "Settings", Settings)
        return cls

    return decorator
