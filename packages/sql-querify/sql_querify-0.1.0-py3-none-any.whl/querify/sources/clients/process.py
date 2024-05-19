import psutil
import pydantic
import typing


class Process(
    pydantic.BaseModel,
):
    pid: int
    name: str
    cpu_pct: float | None
    memory_pct: float | None


class Client:
    @staticmethod
    def get_processes() -> typing.Iterator[Process]:
        for proc in psutil.process_iter(
            [
                'pid',
                'name',
                'cpu_percent',
                'memory_percent']
        ):
            yield Process(
                pid=proc.info['pid'],
                name=proc.info['name'],
                cpu_pct=proc.info['cpu_percent'],
                memory_pct=proc.info['memory_percent'],
            )
