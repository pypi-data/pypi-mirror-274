# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from .password_providers import PasswordProviders
from .provider_link_response_state import ProviderLinkResponseState
from .provider_mfa_request import ProviderMfaRequest

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class ProviderLinkResponse(pydantic.BaseModel):
    state: ProviderLinkResponseState
    redirect_url: typing.Optional[str]
    error_type: typing.Optional[str]
    error: typing.Optional[str]
    provider_mfa: typing.Optional[ProviderMfaRequest]
    provider: PasswordProviders
    connected: bool
    provider_id: str

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
