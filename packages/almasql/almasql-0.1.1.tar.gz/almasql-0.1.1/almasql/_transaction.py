from contextlib import asynccontextmanager
import typing

import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import (
    AsyncConnection as sqla_connection,
    AsyncEngine as sqla_engine,
)

from . import _query
from . import _transactions_chain


class active_transaction:
    """
    Represents an active transaction.
    """

    def __init__(
        self,
        sqlac: sqla_connection,
    ):
        self._sqlac = sqlac

    async def fetch_one(
        self,
        q: _query.query,
        **parameters,
    ) -> sqla.RowMapping | None:
        """
        Returns the first row of the query result.
        """
        statement = q.render(**parameters)
        result = await self._sqlac.execute(statement, parameters)
        mapping_result = result.mappings()
        row = mapping_result.first()
        return row

    async def fetch_many(
        self,
        q: _query.query,
        **parameters,
    ) -> typing.Sequence[sqla.RowMapping]:
        """
        Returns the list of the query result.
        """
        statement = q.render(**parameters)
        result = await self._sqlac.execute(statement, parameters)
        mapping_result = result.mappings()
        rows = mapping_result.all()
        return rows

    async def execute(
        self,
        q: _query.query,
        **parameters,
    ) -> sqla.Row | None:
        """
        Executes the query and returns the result.
        """
        statement = q.render(**parameters)
        result = await self._sqlac.execute(statement, parameters)
        if result.returns_rows:
            returning = result.one()
            return returning


@asynccontextmanager
async def _make_transaction(
    engine: sqla_engine,
) -> typing.AsyncIterator[active_transaction]:
    """
    Begin a new transaction.
    """
    async with engine.connect() as sqlac:
        async with sqlac.begin():
            yield active_transaction(sqlac)


@asynccontextmanager
async def new_transaction(
    engine: sqla_engine,
    *,
    use_last: bool = True,
) -> typing.AsyncIterator[active_transaction]:
    pretransaction = _make_transaction(engine)
    async with _transactions_chain.add(
        pretransaction=pretransaction,
        use_last=use_last,
    ) as transaction:
        yield transaction
