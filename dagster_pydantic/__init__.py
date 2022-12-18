from typing import Callable, Type

from pydantic import BaseModel, validate_model

from dagster import (
    DagsterType,
    TypeCheck,
    TypeCheckContext,
    MetadataEntry,
    MetadataValue,
)

from .version import __version__  # noqa

# ########################
# ##### PYDANTIC MODEL TO DAGSTER TYPE
# ########################


def pydantic_to_dagster_type(
    model: Type[BaseModel],
) -> DagsterType:
    """
    Converts a pydantic model to a dagster type.

    Args:
        model (Type[BaseModel]): The pydantic model to convert.

    Returns:
        DagsterType: The dagster type.

    """

    if not issubclass(model, BaseModel):
        raise TypeError(f"Expected pydantic model, got {model}.")

    name = model.__name__

    return DagsterType(
        name=name,
        type_check_fn=pydantic_type_check_fn(model),
        description=model.__doc__,
        metadata_entries=[
            MetadataEntry("schema", value=MetadataValue.json(model.schema())),
        ],
    )


def pydantic_type_check_fn(
    model: Type[BaseModel],
) -> Callable[["TypeCheckContext", object], TypeCheck]:
    def type_check_fn(_context, value: object) -> TypeCheck:
        if isinstance(value, model):
            *_, validation_error = validate_model(model, value.__dict__)
            if validation_error:
                return TypeCheck(
                    success=False,
                    description=str(validation_error),
                )
        else:
            desc = f"Expected {model.__name__}, got {type(value).__name__}."
            return TypeCheck(
                success=False,
                description=desc,
            )

        return TypeCheck(success=True)

    return type_check_fn
