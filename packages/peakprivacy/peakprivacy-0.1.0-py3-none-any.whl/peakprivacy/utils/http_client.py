import os as os
from dotenv import load_dotenv

# load env file
load_dotenv()

import requests

# Disable SSL warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from typing import Optional

# Exceptions
from ..exceptions.bad_request_error import BadRequestError
from ..exceptions.authentication_error import AuthenticationError
from ..exceptions.permission_denied_error import PermissionDeniedError
from ..exceptions.not_found_error import NotFoundError
from ..exceptions.unprocessable_entity_error import UnprocessableEntityError
from ..exceptions.rate_limit_error import RateLimitError
from ..exceptions.internal_server_error import InternalServerError
from ..exceptions.api_status_error import ApiStatusError
from ..exceptions.api_connection_error import ApiConnectionError

ERROR_CLASSES = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    422: UnprocessableEntityError,
    429: RateLimitError,
    500: InternalServerError
}


class HttpClient:
    def __init__(self, api_url, api_token):
        self.__api_url = api_url
        self.__api_token = api_token

    def request(self, method, request_url, payload_data: Optional[list] = None, stream: Optional[bool] = False):
        try:
            request_url = self.__api_url + request_url

            headers = {
                'Api-Token': self.__api_token,
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }

            verify_request = True
            if os.environ.get("PEAKPRIVACY_VERIFY_REQUEST") is not None:
                os_verify_request = os.environ.get("PEAKPRIVACY_VERIFY_REQUEST")
                if os_verify_request == 'False':
                    verify_request = False

            if method == "GET":
                response = requests.get(request_url, headers=headers, stream=stream, verify=verify_request)
            else:
                response = requests.post(request_url, headers=headers, json=payload_data, stream=stream, verify=verify_request)

            status_code = response.status_code
            if stream is True:
                response_data = response
            else:
                response_data = response.json()

            if status_code != 200:
                if status_code in ERROR_CLASSES:
                    if status_code == 500:
                        response_data = None
                    error_class = ERROR_CLASSES[status_code]
                    raise error_class(response=response_data)
                else:
                    raise ApiStatusError(status_code=status_code, response=response_data)

            return response_data
        except ApiStatusError as api_error:
            raise api_error
        except Exception as e:
            raise ApiConnectionError()
