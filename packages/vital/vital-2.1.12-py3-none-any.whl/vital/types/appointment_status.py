# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class AppointmentStatus(str, enum.Enum):
    """
    An enumeration.
    """

    CONFIRMED = "confirmed"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    def visit(
        self,
        confirmed: typing.Callable[[], T_Result],
        pending: typing.Callable[[], T_Result],
        in_progress: typing.Callable[[], T_Result],
        completed: typing.Callable[[], T_Result],
        cancelled: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is AppointmentStatus.CONFIRMED:
            return confirmed()
        if self is AppointmentStatus.PENDING:
            return pending()
        if self is AppointmentStatus.IN_PROGRESS:
            return in_progress()
        if self is AppointmentStatus.COMPLETED:
            return completed()
        if self is AppointmentStatus.CANCELLED:
            return cancelled()
