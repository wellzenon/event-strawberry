from typing import Any
from dataclasses import asdict
from strawberry.arguments import is_unset


def remove_unset(data: Any) -> dict:
    valid_items = {}

    for key, value in asdict(data).items():
        if is_unset(value):
            continue
        valid_items[key] = value

    return valid_items


def create(model: Any, data: Any) -> Any:
    instance = model()

    for key, value in asdict(data).items():
        if is_unset(value):
            continue
        setattr(instance, key, value)

    if hasattr(instance, "password"):
        instance.set_password(data.password)

    instance.save()
    return instance


def update(instance: Any, data: Any) -> Any:
    update_fields = []

    for key, value in asdict(data).items():
        if is_unset(value):
            continue
        setattr(instance, key, value)
        update_fields.append(key)

    instance.save(update_fields=update_fields)
    return instance
