# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\utils.py

import logging
import aiohttp
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from .exceptions import OpenAIRequestError

class Utils:
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initializes utilities with a logger."""
        self.logger = logger or logging.getLogger(__name__)
        self._setup_logging()

    def _setup_logging(self):
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levellevelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def handle_http_error(self, response: aiohttp.ClientResponse) -> None:
        """Asynchronously handles HTTP errors by raising an OpenAIRequestError with detailed message."""
        if response.status >= 400:
            error_message, error_type, request_id = 'No error message provided.', 'APIError', 'N/A'
            try:
                json_response = await response.json()
                error_message = json_response.get('error', {}).get('message', error_message)
                error_type = json_response.get('error', {}).get('type', error_type)
                request_id = response.headers.get('X-Request-ID', request_id)
            except Exception as json_error:
                self.logger.error("Failed to parse JSON response", exc_info=json_error)
                error_message = str(json_error)

            msg = f"{error_type}: {error_message} (Request ID: {request_id})"
            self.logger.error(msg)
            raise OpenAIRequestError(message=msg, status_code=response.status, error_type=error_type, request_id=request_id)

    def log_api_call(self, method: str, url: str, status_code: Optional[int] = None, duration: Optional[float] = None, data: Optional[Dict[str, Any]] = None) -> None:
        """Logs details of an API call including method, URL, status, duration, and data in a structured format."""
        log_data = {
            "event": "APIRequest",
            "method": method,
            "url": url,
            "status_code": status_code,
            "duration": f"{duration:.2f}s" if duration else None,
            "request_data": json.dumps(data) if data else "{}"
        }
        self.logger.info("API call detail:", extra=log_data)

    def validate_response_content_type(self, response: aiohttp.ClientResponse, expected_content_type: str) -> None:
        """Validates the Content-Type of the response asynchronously."""
        if expected_content_type not in response.headers.get('Content-Type', ''):
            raise ValueError(f"Unexpected Content-Type. Expected {expected_content_type}.")

    def format_data_for_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Filters out None values from a dictionary for API request submission."""
        return {k: v for k, v in data.items() if v is not None}

    def validate_list_of_dicts(self, items: List[Dict[str, Any]], required_keys: List[str]) -> bool:
        """Validates that each item in the list is a dict containing all required keys."""
        return all(all(key in item for key in required_keys) for item in items)

    def datetime_to_iso(self, dt: datetime) -> str:
        """Converts a datetime object to an ISO formatted string."""
        return dt.replace(microsecond=0).isoformat()

    def sanitize_input(self, input_string: str) -> str:
        """Sanitizes input strings by stripping leading and trailing whitespace."""
        return input_string.strip()

    async def fetch_all_pages(self, make_api_call, endpoint: str, **params) -> List[Dict[str, Any]]:
        """Fetches all pages from a paginated API endpoint asynchronously using the provided API call function."""
        all_items, page_token = [], None
        while True:
            response, next_page_token = await make_api_call(endpoint, params={**params, 'page_token': page_token})
            all_items.extend(response)
            if not next_page_token: break
            page_token = next_page_token
        return all_items

    async def set_vector_store_expiration(self, make_api_call, vector_store_id: str, expires_after: Dict[str, Any]) -> Dict[str, Any]:
        """Sets the expiration policy for a vector store."""
        data = {"expires_after": expires_after}
        return await make_api_call(f"beta/vector_stores/{vector_store_id}/update", method="POST", data=data)
