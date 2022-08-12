import logging
from json import JSONDecodeError
from typing import Optional

from requests import Response, Session
from requests.exceptions import RequestException

from metabase_tools.exceptions import (
    AuthenticationFailure,
    InvalidDataReceived,
    RequestFailure,
)
from metabase_tools.models.result import Result


class RestAdapter:
    def __init__(self, metabase_url: str, credentials: dict):
        # Initialize logging
        self._logger = logging.getLogger(__name__)

        # Validate Metabase URL
        if metabase_url[-1] == "/":
            metabase_url = metabase_url[:-1]
        if metabase_url[-4:] == "/api":
            metabase_url = metabase_url[:-4]
        self.metabase_url = f"{metabase_url}/api"

        # Starts session to be reused by the adapter so that the auth token is cached
        self._session = Session()

        # Determines what was supplied in credentials and authenticates accordingly
        if "token" in credentials:
            self._logger.debug("Using supplied token for requests.")
            headers = {
                "Content-Type": "application/json",
                "X-Metabase-Session": credentials["token"],
            }
            self._session.headers.update(headers)
        elif "username" in credentials and "password" in credentials:
            self._logger.debug("Token not present, using username and password")
            self._authenticate(credentials=credentials)
        else:
            raise AuthenticationFailure(
                "Credentials missing [username and password] or [token]"
            )

    def _authenticate(self, credentials: dict):
        """Private method for authenticating a session with the API"""
        self._logger.debug("Starting authentication - RestAdapter member")
        try:
            post_request = self._session.post(
                f"{self.metabase_url}/session", json=credentials
            )
        except RequestException as error_raised:
            self._logger.error(str(error_raised))
            raise RequestFailure(
                "Request failed during authentication"
            ) from error_raised

        status_code = post_request.status_code
        if status_code == 200:
            headers = {
                "Content-Type": "application/json",
                "X-Metabase-Session": post_request.json()["id"],
            }
            self._session.headers.update(headers)
            self._logger.debug("Authentication successful")
        else:
            reason = post_request.reason
            raise AuthenticationFailure(
                f"Authentication failed. {status_code} - {reason}"
            )

    def get_token(self) -> str:
        return str(self._session.headers.get("X-Metabase-Session"))

    def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Response:
        """Perform an HTTP request, catching and re-raising any exceptions
        Args:
            method (str): GET or POST
            url (str): URL endpoint
            params (dict): Endpoint parameters
            json (dict): Data payload
        Returns:
            request result
        """
        log_line_pre = f"{method=}, {url=}, {params=}"
        try:
            self._logger.debug(log_line_pre)
            return self._session.request(
                method=method, url=url, params=params, json=json
            )
        except RequestException as error_raised:
            self._logger.error(str(error_raised))
            raise RequestFailure("Request failed") from error_raised

    def do(
        self,
        http_method: str,
        endpoint: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Result:
        """Private method for get and post methods
        Args:
            http_method (str): GET or POST
            endpoint (str): URL endpoint
            ep_params (Dict, optional): Endpoint parameters. Defaults to None.
            data (Dict, optional): Data payload. Defaults to None.
        Returns:
            Result: a Result object
        """
        full_api_url = self.metabase_url + endpoint

        log_line_post = "success=%s, status_code=%s, message=%s"
        response = self._make_request(
            method=http_method, url=full_api_url, params=params, json=json
        )
        # Deserialize JSON output to Python object, or return failed Result on exception
        try:
            data = response.json()
        except (ValueError, JSONDecodeError) as error_raised:
            if response.status_code == 204:
                data = None
            elif response.status_code == 401:
                self._logger.error(
                    log_line_post, False, response.status_code, error_raised
                )
                raise AuthenticationFailure(
                    f"{response.status_code} - {response.reason}"
                ) from error_raised
            else:
                self._logger.error(
                    log_line_post, False, response.status_code, error_raised
                )
                raise InvalidDataReceived(
                    f"{response.status_code} - {response.reason}"
                ) from error_raised

        # If status_code in 200-299 range, return Result, else raise exception
        is_success = 299 >= response.status_code >= 200
        if is_success:
            self._logger.debug(
                log_line_post, is_success, response.status_code, response.reason
            )
            return Result(
                status_code=response.status_code, message=response.reason, data=data
            )

        if isinstance(data, dict) and "errors" in data:
            error_line = (
                f'{response.status_code} - {response.reason} - {data["errors"]}'
            )
            self._logger.error(error_line)
        else:
            error_line = f"{response.status_code} - {response.reason}"
        self._logger.error(log_line_post)
        raise RequestFailure(error_line)
