# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from .client_facing_provider import ClientFacingProvider

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class ConnectedSourceClientFacing(pydantic.BaseModel):
    provider: ClientFacingProvider = pydantic.Field(description="The provider of this connected source.")
    created_on: dt.datetime = pydantic.Field(description="When your item is created")
    source: ClientFacingProvider = pydantic.Field(
        description="Deprecated. Use `provider` instead. Subject to removal after 1 Jan 2024."
    )

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        json_encoders = {dt.datetime: serialize_datetime}
