from datetime import datetime
from typing import Optional

from .models.result import Result
from .rest import RestAdapter


class MetabaseApi:
    def __init__(self, metabase_url: str, credentials: Optional[dict] = None, cache_token: bool = False, token_path: str = './metabase.token'):
        try:
            with open(token_path, 'r') as f:
                token = {'token': f.read()}
            self._rest_adapter = RestAdapter(
                metabase_url=metabase_url, credentials=token)
        except FileNotFoundError:
            if credentials:
                self._rest_adapter = RestAdapter(
                    metabase_url=metabase_url, credentials=credentials)
                if cache_token:
                    self.save_token(file=token_path)

    def save_token(self, file: str):
        token = self._rest_adapter.get_token()
        with open(file, 'w') as f:
            f.write(token)

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
