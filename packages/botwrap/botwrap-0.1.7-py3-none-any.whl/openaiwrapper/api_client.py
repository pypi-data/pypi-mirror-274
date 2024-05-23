# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\api_client.py

import aiohttp
import logging
from typing import Any, Dict, Optional
from .exceptions import OpenAIWrapperError, OpenAIRequestError
from .error_logging import setup_logger
from .config import get_config
from .assistants import AssistantManager
from .files import FileManager
from .messages import MessageManager
from .runs import RunManager
from .threads import ThreadManager
from .tools import ToolsManager
from .vector_store_manager import VectorStoreManager
from .profiles import ProfileManager
from .decorators import log_error_decorator

class OpenAIAPIClient:
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1", logger: Optional[logging.Logger] = None):
        self.api_key = api_key
        self.base_url = base_url
        self.session = None
        self.logger = logger or setup_logger(__name__, 'api_calls.log')
        self._initialize_managers()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            self.session = None

    def _initialize_managers(self):
        make_api_call = self.make_api_call
        self.vector_store_manager = VectorStoreManager(make_api_call, self.logger)
        self.thread_manager = ThreadManager(make_api_call, self.logger)
        self.message_manager = MessageManager(make_api_call, self.logger)
        self.run_manager = RunManager(make_api_call, self.logger)
        self.tools_manager = ToolsManager(make_api_call, self.logger)
        self.assistant_manager = AssistantManager(make_api_call, self.logger)
        self.file_manager = FileManager(api_key=self.api_key, make_request_func=make_api_call, logger=self.logger)
        self.profile_manager = ProfileManager(self.logger)

    @log_error_decorator(logger=None)
    async def make_api_call(self, endpoint: str, method: str = "GET", headers: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f'{self.base_url}/{endpoint}'
        headers = headers or {}
        headers.update({
            'Authorization': f"Bearer {self.api_key}",
            'Accept': 'application/json',
            'OpenAI-Beta': 'assistants=v2'  # Specific header for beta features
        })

        self.logger.info(f"Making {method} request to {url}")
        self.logger.debug(f"Request headers: {headers}")
        self.logger.debug(f"Request data: {data}")
        self.logger.debug(f"Request params: {params}")

        try:
            async with self.session.request(method=method, url=url, headers=headers, json=data, params=params) as response:
                self.logger.info(f"Response status: {response.status}")
                response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

                if 'application/json' in response.headers.get('Content-Type', ''):
                    json_response = await response.json()
                    self.logger.debug(f"Response JSON: {json_response}")
                    return json_response
                else:
                    content = await response.text()
                    self.logger.error(f"Unexpected MIME type: {response.headers.get('Content-Type')}, Content: {content}")
                    raise OpenAIWrapperError(f"Unexpected MIME type: {response.headers.get('Content-Type')}")
        except aiohttp.ClientResponseError as e:
            self.logger.error(f"HTTP error occurred: {e.status}, {e.message}")
            self.logger.error(f"Failed request data: {data}")
            try:
                error_details = await e.response.text()
                self.logger.error(f"Error details: {error_details}")
            except Exception:
                self.logger.error("Failed to retrieve error details.")
            raise OpenAIRequestError(message=e.message, status_code=e.status)
        except aiohttp.ClientError as e:
            self.logger.error("Client error during the API request.", exc_info=True)
            raise OpenAIWrapperError("Client error during the API request.")
        except Exception as e:
            self.logger.error("Unexpected error", exc_info=True)
            raise OpenAIWrapperError("Unexpected error during API call.")
