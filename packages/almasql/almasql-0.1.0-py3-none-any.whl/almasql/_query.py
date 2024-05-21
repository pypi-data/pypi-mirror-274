import jinja2
import sqlalchemy as sqla

from . import _directives


class query:
    """
    Represents an sql query template that generates an sql statement (via jinja2).
    """

    def __init__(
        self,
        raw_statement: str,
    ) -> None:
        self._template = jinja2.Template(raw_statement)

    def render(
        self,
        *args,
        **kwargs,
    ) -> sqla.TextClause:
        statement = self._template.render(
            *args,
            **kwargs,
            **_directives.DIRECTIVES,
        )
        return sqla.text(statement)
