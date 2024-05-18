# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class QuestionType(str, enum.Enum):
    """
    An enumeration.
    """

    CHOICE = "choice"
    TEXT = "text"
    NUMERIC = "numeric"
    MULTI_CHOICE = "multi_choice"

    def visit(
        self,
        choice: typing.Callable[[], T_Result],
        text: typing.Callable[[], T_Result],
        numeric: typing.Callable[[], T_Result],
        multi_choice: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is QuestionType.CHOICE:
            return choice()
        if self is QuestionType.TEXT:
            return text()
        if self is QuestionType.NUMERIC:
            return numeric()
        if self is QuestionType.MULTI_CHOICE:
            return multi_choice()
