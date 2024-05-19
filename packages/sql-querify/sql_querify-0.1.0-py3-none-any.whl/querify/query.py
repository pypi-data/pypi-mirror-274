import colorama
import tabulate
import typing
import sys
import sql_metadata

from . import database
from . import sources


def query(
    query=None,
    *_,
):
    if query is None:
        raise Exception('Missing query')

    parsed_query = sql_metadata.Parser(query)

    source = sources.get_source_by_name(
        source_name=parsed_query.tables[0],
    )

    with database.client.DB() as db:
        db.create_source_table(
            source=source,
        )

        db.insert_source_data(
            source=source,
        )

        columns, rows = db.query(
            query=query,
        )

        display(
            columns=columns,
            rows=rows,
        )


def display(
    columns: list[str],
    rows: list[typing.Any],
):
    print(
        tabulate.tabulate(
            rows,
            [
                colorama.Style.BRIGHT +
                f'{column}' +
                colorama.Style.RESET_ALL
                for column
                in columns
            ],
            tablefmt='psql',
        )
    )


def main():
    query(*sys.argv[1:])


if __name__ == '__main__':
    main()
