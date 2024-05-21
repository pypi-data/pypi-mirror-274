from contextlib import asynccontextmanager
from contextvars import ContextVar
import typing


_context_last_transaction = ContextVar('last_transaction')


@asynccontextmanager
async def add[T: typing.AsyncContextManager](
    *,
    pretransaction: T,
    use_last: bool = False,
) -> typing.AsyncIterator[T]:
    """
    Adds a new transaction to the chain if `use_last` is `False` or last active transaction not found.
    Otherwise yields last active transaction.

    IMPORTANT! Begin new transaction if __aenter__ was called using `asyncio.create_task`.

    Args:
        - pretransaction: A new transaction that is not began. Must implement `typing.AsyncConextManager`.
        - use_last: set `True` if you want to use last active transaction.
    """
    last_transaction = _context_last_transaction.get(None)

    if last_transaction is None:
        use_last = False

    if use_last is False:
        async with pretransaction as new_transaction:
            _context_last_transaction.set(new_transaction)

            try:
                yield new_transaction
            finally:
                _context_last_transaction.set(last_transaction)
    else:
        yield last_transaction
