from dagster import DagsterType, check_dagster_type

from pydantic import BaseModel

import pytest

from dagster_pydantic import pydantic_to_dagster_type


class MyPydanticModel(BaseModel):
    """
    This is a Pydantic model.
    """

    a: int
    b: str


@pytest.fixture
def my_model():
    return MyPydanticModel(a=1, b="world")


@pytest.fixture
def dagster_type():
    return pydantic_to_dagster_type(MyPydanticModel)


# ########################
# ##### TESTS
# ########################

# ----- TYPE CONSTRUCTION


def test_pydantic_model_to_dagster_type(dagster_type):
    assert isinstance(dagster_type, DagsterType)
    assert len(dagster_type.metadata_entries) == 1
    assert dagster_type.metadata_entries[0].label == "schema"


# ----- VALIDATION


def test_validate_ok(dagster_type, my_model):
    result = check_dagster_type(dagster_type, my_model)
    assert isinstance(my_model, MyPydanticModel)
    assert result.success


def test_validate_inv_bad_value(dagster_type, my_model):
    my_model.a = "hello"
    result = check_dagster_type(dagster_type, my_model)
    assert not result.success


def test_validate_inv_missing_value(dagster_type, my_model):
    my_model.a = None
    result = check_dagster_type(dagster_type, my_model)
    assert not result.success
