from http.client import HTTPException
from typing import Any, Callable, Dict, Optional
from urllib.parse import urljoin

from pydantic import BaseModel, HttpUrl, SecretStr
from requests import Response

from galileo_core.constants.http_headers import HttpHeaders


class ApiClient(BaseModel):
    host: HttpUrl
    jwt_token: SecretStr

    @property
    def auth_header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.jwt_token.get_secret_value()}"}

    @staticmethod
    def validate_response(response: Response) -> None:
        if not response.ok:
            raise HTTPException(
                f"Galileo API returned HTTP status code {response.status_code}. Error was: {response.text}"
            ) from None

    @staticmethod
    def make_request(
        request_method: Callable[..., Response],
        base_url: str,
        endpoint: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        response = request_method(urljoin(base_url, endpoint), *args, **kwargs)
        ApiClient.validate_response(response)
        return response.json()

    def request(
        self,
        method: Callable[..., Response],
        path: str,
        content_headers: Dict[str, str] = HttpHeaders.json(),
        read_timeout: Optional[float] = None,
        **kwargs: Any,
    ) -> Any:
        return ApiClient.make_request(
            request_method=method,
            base_url=self.host.unicode_string(),
            endpoint=path,
            headers={**content_headers, **self.auth_header},
            # Set a default connection timeout of 5 seconds and a read timeout of 60 seconds.
            timeout=(5, (60 if read_timeout is None else read_timeout)),
            **kwargs,
        )
