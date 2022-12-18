from dagster_pydantic import pydantic_to_dagster_type
from dagster import repository, job, Out, op, In

from pydantic import BaseModel


class MyPydanticModel(BaseModel):
    """
    This is a Pydantic model.
    """
    a: int
    b: str


MyPydanticModelDT = pydantic_to_dagster_type(MyPydanticModel)


@op(out=Out(MyPydanticModelDT))
def get_model():
    model = MyPydanticModel(
        a=1,
        b="hello"
    )
    # This should fail type checking in the Dagit UI.
    model.b = {}  # type: ignore
    return model


@op(ins={
    "model": In(MyPydanticModelDT)
})
def print_model(model):
    print(model)


@job
def my_job():
    model = get_model()
    print_model(model)


@repository
def my_dagster_project():
    return [my_job]
