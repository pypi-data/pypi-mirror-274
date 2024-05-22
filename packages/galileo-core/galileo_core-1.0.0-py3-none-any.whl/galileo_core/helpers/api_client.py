from http.client import HTTPException
from typing import Any, Dict
from urllib.parse import urljoin

from httpx import AsyncClient, HTTPError, Response, Timeout
from pydantic import BaseModel, HttpUrl, SecretStr
from typing_extensions import assert_never

from galileo_core.constants.http_headers import HttpHeaders
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.execution import async_run


class ApiClient(BaseModel):
    host: HttpUrl
    jwt_token: SecretStr

    @property
    def auth_header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.jwt_token.get_secret_value()}"}

    @staticmethod
    def validate_response(response: Response) -> None:
        try:
            response.raise_for_status()
        except HTTPError:
            raise HTTPException(
                f"Galileo API returned HTTP status code {response.status_code}. Error was: {response.text}"
            )

    @staticmethod
    async def make_request(
        request_method: RequestMethod,
        base_url: str,
        endpoint: str,
        read_timeout: float = 60.0,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        url = urljoin(base_url, endpoint)
        async with AsyncClient(timeout=Timeout(read_timeout, connect=5.0)) as client:
            if request_method == RequestMethod.GET:
                response = await client.get(url, *args, **kwargs)
            elif request_method == RequestMethod.POST:
                response = await client.post(url, *args, **kwargs)
            elif request_method == RequestMethod.PUT:
                response = await client.put(url, *args, **kwargs)
            elif request_method == RequestMethod.DELETE:
                response = await client.delete(url, *args, **kwargs)
            elif request_method == RequestMethod.PATCH:
                response = await client.patch(url, *args, **kwargs)
            elif request_method == RequestMethod.OPTIONS:
                response = await client.options(url, *args, **kwargs)
            elif request_method == RequestMethod.HEAD:
                response = await client.head(url, *args, **kwargs)
            else:
                assert_never(request_method)

            ApiClient.validate_response(response)
            return response.json()

    def request(
        self, method: RequestMethod, path: str, content_headers: Dict[str, str] = HttpHeaders.json(), **kwargs: Any
    ) -> Any:
        return async_run(self.arequest(method=method, path=path, content_headers=content_headers, **kwargs))

    async def arequest(
        self, method: RequestMethod, path: str, content_headers: Dict[str, str] = HttpHeaders.json(), **kwargs: Any
    ) -> Any:
        return await ApiClient.make_request(
            request_method=method,
            base_url=self.host.unicode_string(),
            endpoint=path,
            headers={**content_headers, **self.auth_header},
            **kwargs,
        )
