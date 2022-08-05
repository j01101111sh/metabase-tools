from typing import Optional

from .models.generic_models import Result
from .rest_adapter import RestAdapter


class MetabaseApi:
    # TODO: Add tools here
    def __init__(self, metabase_url: str, credentials: dict):
        self._rest_adapter = RestAdapter(
            metabase_url=metabase_url, credentials=credentials)

    def get(self, endpoint: str, params: Optional[dict] = None) -> Result:
        """HTTP GET request
        Args:
            endpoint (str): URL endpoint
            ep_params (Dict, optional): Endpoint parameters. Defaults to None.
        Returns:
            Result: a Result object
        """
        return self._rest_adapter.do(http_method='GET', endpoint=endpoint, params=params)

    def post(self, endpoint: str, params: Optional[dict] = None, json: Optional[dict] = None) -> Result:
        """HTTP POST request
        Args:
            endpoint (str): URL endpoint
            ep_params (Dict, optional): Endpoint parameters. Defaults to None.
            json (Dict, optional): Data payload. Defaults to None.
        Returns:
            Result: a Result object
        """
        return self._rest_adapter.do(http_method='POST', endpoint=endpoint, params=params, json=json)

    def delete(self, endpoint: str, params: Optional[dict] = None) -> Result:
        """HTTP DELETE request
        Args:
            endpoint (str): URL endpoint
            ep_params (Dict, optional): Endpoint parameters. Defaults to None.
        Returns:
            Result: a Result object
        """
        return self._rest_adapter.do(http_method='DELETE', endpoint=endpoint, params=params)

    def put(self, endpoint: str, params: Optional[dict] = None, json: Optional[dict] = None) -> Result:
        """HTTP PUT request
        Args:
            endpoint (str): URL endpoint
            ep_params (Dict, optional): Endpoint parameters. Defaults to None.
            json (Dict, optional): Data payload. Defaults to None.
        Returns:
            Result: a Result object
        """
        return self._rest_adapter.do(http_method='PUT', endpoint=endpoint, params=params, json=json)
