import sqlite3

from .. import sources


class DB:
    def __init__(self) -> None:
        self.conn: sqlite3.Connection

    def __enter__(
        self,
    ):
        self.conn = sqlite3.connect(':memory:')

        return self

    def __exit__(
        self,
        *_,
    ):
        if self.conn is not None:
            self.conn.close()

    def create_source_table(
        self,
        source: sources.base_source.BaseSource,
    ):
        fields = [
            field
            for field, _ in source.model.__fields__.items()
        ]
        fields_clause = ', '.join(fields)

        self.conn.execute(f'CREATE TABLE {source.name}({fields_clause})')

    def insert_source_data(
        self,
        source: sources.base_source.BaseSource,
    ):
        fields = [
            field
            for field, _ in source.model.__fields__.items()
        ]
        fields_clause = ', '.join(fields)

        values_clause = ', '.join(['?'] * len(fields))

        source_values = [
            tuple(
                getattr(source_item, field)
                for field in fields
            )
            for source_item in source.get_data()
        ]

        self.conn.executemany(
            f'INSERT INTO {source.name}({fields_clause}) VALUES({values_clause})',
            source_values,
        )

    def query(
        self,
        query: str,
    ):
        result = self.conn.execute(query)

        columns = [
            description[0]
            for description in result.description
        ]

        return (
            columns,
            result.fetchall(),
        )
