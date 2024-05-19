from . import base_source
from . import clients


class ProcessSource(
    base_source.BaseSource,
):
    name = 'processes'

    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.process_client = clients.process.Client()

    @property
    def model(
        self,
    ):
        return clients.process.Process

    def get_data(
        self,
    ):
        return list(self.process_client.get_processes())


