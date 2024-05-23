# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\threads.py

import logging
from typing import Dict, List, Optional, Any
from .error_logging import log_error_decorator

class ThreadManager:
    def __init__(self, make_api_call, logger: Optional[logging.Logger] = None):
        """Initializes the ThreadManager with a callable for making API requests and a logger."""
        self.make_api_call = make_api_call
        self.logger = logger or self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup logger configuration."""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    @log_error_decorator(logger=None)
    async def create(self, assistant_id: str, tool_resources: Optional[Dict[str, Any]] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict:
        """Creates a new thread with required assistant ID and optional tool resources and metadata."""
        self._validate_input(assistant_id, "Assistant ID")

        data = {
            'assistant_id': assistant_id,
            'tool_resources': tool_resources or {},
            'metadata': metadata or {}
        }

        self.logger.info(f"Creating a new thread with data: {data}")
        return await self.make_api_call("threads", method="POST", data=data)

    @log_error_decorator(logger=None)
    async def retrieve(self, thread_id: str) -> Dict:
        """Retrieves a specific thread by ID asynchronously."""
        self._validate_input(thread_id, "Thread ID")

        self.logger.info(f"Retrieving thread with ID: {thread_id}.")
        return await self.make_api_call(f"threads/{thread_id}", method="GET")

    @log_error_decorator(logger=None)
    async def update(self, thread_id: str, tool_resources: Optional[Dict[str, Any]] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict:
        """Updates a specific thread asynchronously."""
        self._validate_input(thread_id, "Thread ID")

        data = {}
        if tool_resources:
            data['tool_resources'] = tool_resources
        if metadata:
            data['metadata'] = metadata

        self.logger.info(f"Updating thread with ID: {thread_id} with data: {data}.")
        return await self.make_api_call(f"threads/{thread_id}", method="POST", data=data)

    @log_error_decorator(logger=None)
    async def delete(self, thread_id: str) -> Dict:
        """Deletes a specific thread by ID asynchronously."""
        self._validate_input(thread_id, "Thread ID")

        self.logger.info(f"Deleting thread with ID: {thread_id}.")
        return await self.make_api_call(f"threads/{thread_id}", method="DELETE")

    @log_error_decorator(logger=None)
    async def list(self, **kwargs) -> Dict:
        """Lists all threads asynchronously, with optional filtering parameters."""
        self.logger.info("Listing all threads.")
        return await self.make_api_call("threads", method="GET", params=kwargs)

    @log_error_decorator(logger=None)
    async def list_all_threads(self) -> List[Dict[str, Any]]:
        """Utility method to fetch and return all threads, handling pagination automatically."""
        all_threads = []
        page_token = None
        is_first_page = True

        while is_first_page or page_token:
            params = {'after': page_token} if page_token else {}
            page = await self.list(**params)
            threads_data = page.get('data', [])
            all_threads.extend(threads_data)
            page_token = page.get('pagination', {}).get('next_page_token')
            is_first_page = False

        self.logger.info(f"Retrieved all threads, total count: {len(all_threads)}")
        return all_threads

    def _validate_input(self, input_value: str, input_name: str):
        if not input_value:
            self.logger.error(f"{input_name} must be provided and cannot be empty.")
            raise ValueError(f"{input_name} must be provided and cannot be empty.")
