# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class Fats(pydantic.BaseModel):
    saturated: typing.Optional[float] = pydantic.Field(description="Amount of saturated fats in grams (g)")
    monounsaturated: typing.Optional[float] = pydantic.Field(description="Amount of monounsaturated fats in grams (g)")
    polyunsaturated: typing.Optional[float] = pydantic.Field(description="Amount of polyunsaturated fats in grams (g)")
    omega_3: typing.Optional[float] = pydantic.Field(
        alias="omega3", description="Amount of Omega-3 fatty acids in grams (g)"
    )
    omega_6: typing.Optional[float] = pydantic.Field(
        alias="omega6", description="Amount of Omega-6 fatty acids in grams (g)"
    )
    total: typing.Optional[float] = pydantic.Field(description="Total amount of fats in grams (g)")

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        json_encoders = {dt.datetime: serialize_datetime}
