# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\exceptions.py

import logging
import aiohttp
from typing import Optional

# Custom Base Exception
class OpenAIWrapperError(Exception):
    """Base exception class for OpenAI Wrapper related errors."""
    pass

# Specific Exception classes for different error categories
class APIConnectionError(OpenAIWrapperError):
    pass

class APITimeoutError(OpenAIWrapperError):
    pass

class APIResponseError(OpenAIWrapperError):
    def __init__(self, message, status_code, error_type='APIResponseError', details=None):
        super().__init__(message)
        self.status_code = status_code
        self.error_type = error_type
        self.details = details

class BadRequestError(APIResponseError):
    pass

class UnauthorizedError(APIResponseError):
    pass

class ServerError(APIResponseError):
    pass

class OpenAIRequestError(APIResponseError):
    def __init__(self, message=None, status_code=None, error_type=None, request_id=None, details=None):
        super().__init__(message, status_code, error_type, details)
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        self.request_id = request_id

    def __str__(self):
        return (f"Error Type: {self.error_type}, "
                f"Message: {self.message}, Status Code: {self.status_code}, "
                f"Request ID: {self.request_id}, Details: {self.details}")

async def create_openai_request_error(response: aiohttp.ClientResponse, logger: Optional[logging.Logger] = None) -> OpenAIRequestError:
    if not logger:
        logger = logging.getLogger(__name__)
    try:
        error_details = await response.json()
        error_message = error_details.get('error', {}).get('message', 'No error message provided.')
        error_type = error_details.get('error', {}).get('type', 'Unknown Error Type')
    except aiohttp.ContentTypeError:
        text = await response.text()
        error_message = text or "Failed to decode JSON response."
        error_type = 'ContentTypeError'

    status_code = response.status
    request_id = response.headers.get('X-Request-ID', 'Not provided')
    logger.error(f"{error_type}: {error_message} (Request ID: {request_id})")
    return OpenAIRequestError(message=error_message, status_code=status_code, error_type=error_type, request_id=request_id)

def log_error_decorator(logger: Optional[logging.Logger] = None):
    """Decorator to automatically log errors when they are raised."""
    if not logger:
        logger = logging.getLogger(__name__)
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except OpenAIWrapperError as error:
                logger.error(f"OpenAI Request Error Logged: {error}")
                raise  # Re-raise to handle elsewhere
        return wrapper
    return decorator
