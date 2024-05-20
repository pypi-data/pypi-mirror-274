from abc import ABC
from collections.abc import Generator
from contextlib import contextmanager, suppress
from typing import Optional, TYPE_CHECKING

import httpx
from pydantic import ValidationError

if TYPE_CHECKING:
    from ._api_methods import ErrorResponse


class UnisenderGoError(Exception, ABC):
    pass


@UnisenderGoError.register
class ClientSetupError(Exception, ABC):
    pass


@ClientSetupError.register
class SyncClientSetupError(Exception):
    def __init__(self) -> None:
        super().__init__('Requires SyncClient to be setup before call.')


@ClientSetupError.register
class AsyncClientSetupError(Exception):
    def __init__(self) -> None:
        super().__init__('Requires AsyncClient to be setup before call.')


@UnisenderGoError.register
class HTTPStatusError(httpx._exceptions.HTTPStatusError):
    # Common httpx.HTTPStatusError fields are filled by __init__ method:
    request: httpx.Request
    response: httpx.Response

    # Unisender Go specific extra data:
    response_payload: Optional['ErrorResponse']

    def __init__(
        self,
        *,
        request: httpx.Request,
        response: httpx.Response,
    ) -> None:
        from ._api_methods import ErrorResponse

        self.response_payload = None
        with suppress(ValidationError):
            self.response_payload = ErrorResponse.parse_raw(response.content)

        payload = self.response_payload
        message_template_lines = [
            "Error occured on {request.method} {request.url}",
            "HTTP status code: {response.status_code} {response.reason_phrase}",
            "Unisender Go API error: code={payload.code!r} message={payload.message!r};" if payload else None,
            "Response payload: {response.text!r}",
            'For more information check: https://godocs.unisender.ru/web-api-ref#api-errors',
        ]
        message_template = '\n'.join(line for line in message_template_lines if line)

        message = message_template.format(
            payload=self.response_payload,
            request=request,
            response=response,
        )

        super().__init__(message, request=request, response=response)


@UnisenderGoError.register
class ResponseFormatError(Exception):
    request: httpx.Request
    response: httpx.Response

    def __init__(
        self,
        *,
        request: httpx.Request,
        response: httpx.Response,
    ):
        self.request = request
        self.response = response
        exception_message = (
            f"Error occured on {request.method} {request.url}\n"
            f"HTTP status code: {response.status_code} {response.reason_phrase}\n"
            f"Response payload: {response.text!r}"
        )
        super().__init__(exception_message)

    @classmethod
    @contextmanager
    def reraise_from(
        cls,
        *exception_types: type[BaseException],
        request: httpx.Request,
        response: httpx.Response,
    ) -> Generator[None, None, None]:
        try:
            yield
        except Exception as exc:  # noqa: BLE001
            if not any(isinstance(exc, exc_type) for exc_type in exception_types):
                raise
            raise cls(request=request, response=response) from exc


def raise_for_status(response: httpx.Response) -> None:
    request = response._request

    if request is None:
        raise ValueError(
            'Cannot call `raise_for_status` as the request instance has not been set on this response.',
        )

    if response.is_success:
        return

    raise HTTPStatusError(request=request, response=response)
