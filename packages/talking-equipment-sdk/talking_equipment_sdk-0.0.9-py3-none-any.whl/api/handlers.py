import json
from abc import ABC
import http.client
from urllib.parse import urlencode, urlparse

from .utils import encode_parameters

from .responses import TalkingEquipmentResponse
from ..config import config


class RequestHandler(ABC):
    _base_url = config.BASE_URL
    _version = config.VERSION
    _endpoint_path = None

    @classmethod
    def api_key(cls) -> str:
        return config.api_key

    @classmethod
    def create_connection(cls) -> http.client.HTTPSConnection:
        parsed_url = urlparse(cls._base_url)
        if parsed_url.scheme == "https":
            connection = http.client.HTTPSConnection(parsed_url.netloc)
        else:
            connection = http.client.HTTPConnection(parsed_url.netloc)

        return connection

    @classmethod
    def process_request(cls, method, path, encoded_body: bytes = None) -> dict:
        connection = cls.create_connection()

        if encoded_body:
            connection.request(method, path, body=encoded_body, headers=cls.headers())
        else:
            connection.request(method, path, headers=cls.headers())

        response = connection.getresponse()
        json_data = TalkingEquipmentResponse(response).parse_response()

        connection.close()

        return json_data

    @classmethod
    def delete_request(cls, path) -> dict:
        return cls.process_request("DELETE", path)

    @classmethod
    def get_request(cls, path) -> dict:
        return cls.process_request("GET", path)

    @classmethod
    def post_request(cls, url, body) -> dict:
        encoded_body = json.dumps(body).encode('utf-8')
        return cls.process_request("POST", url, encoded_body)

    @classmethod
    def generate_url_path(cls, *args, **kwargs) -> str:
        query_parameters = kwargs.get('query_params', {})
        path_parameters = '/'.join(encode_parameters(*args))

        url = f"/{cls._version}/api/{cls._endpoint_path}/{path_parameters}".rstrip('/')

        if query_parameters:
            query = urlencode(query_parameters)
            url += '?' + query

        return url


    @classmethod
    def headers(cls) -> dict:
        return {
            "Authorization": f"Bearer {cls.api_key()}",
            "Content-Type": "application/json",
        }

