import abc
import pydantic


class BaseSource(
    abc.ABC,
):
    name: str

    @property
    def model(
        self,
    ) -> pydantic.BaseModel:
        ...

    @abc.abstractclassmethod
    def get_data(
        self,
    ) -> list[pydantic.BaseModel]:
        ...
