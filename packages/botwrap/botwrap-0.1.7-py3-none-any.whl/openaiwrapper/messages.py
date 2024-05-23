# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\messages.py

import logging
from typing import Dict, Optional
from .decorators import log_error_decorator

logger = logging.getLogger(__name__)

class MessageManager:
    def __init__(self, make_api_call, logger: Optional[logging.Logger] = None):
        """Initializes the MessageManager with a callable for making API requests and a logger."""
        self.make_api_call = make_api_call
        self.logger = logger or logging.getLogger(__name__)
        self._setup_logging()

    def _setup_logging(self):
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levellevelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    @log_error_decorator(logger=logger)
    async def create(self, thread_id: str, content: str, role: str = "user", **kwargs) -> Dict:
        """Sends a new message to a thread."""
        self._validate_input(thread_id, "Thread ID")
        self._validate_input(content, "Message content")
        if role not in ["user", "assistant"]:
            self.logger.error("Role must be either 'user' or 'assistant'.")
            raise ValueError("Role must be either 'user' or 'assistant'.")

        data = {"content": content, "role": role, **kwargs}
        self.logger.info(f"Sending message to thread {thread_id}. Content: {content}")
        return await self.make_api_call(f"threads/{thread_id}/messages", method="POST", data=data)

    @log_error_decorator(logger=logger)
    async def retrieve(self, thread_id: str, message_id: str) -> Dict:
        """Retrieves a specific message by its ID from a thread."""
        self._validate_input(thread_id, "Thread ID")
        self._validate_input(message_id, "Message ID")

        self.logger.info(f"Retrieving message {message_id} from thread {thread_id}.")
        return await self.make_api_call(f"threads/{thread_id}/messages/{message_id}", method="GET")

    @log_error_decorator(logger=logger)
    async def delete(self, thread_id: str, message_id: str) -> Dict:
        """Deletes a specific message by its ID from a thread."""
        self._validate_input(thread_id, "Thread ID")
        self._validate_input(message_id, "Message ID")

        self.logger.info(f"Deleting message {message_id} from thread {thread_id}.")
        return await self.make_api_call(f"threads/{thread_id}/messages/{message_id}", method="DELETE")

    @log_error_decorator(logger=logger)
    async def list(self, thread_id: str, **kwargs) -> Dict:
        """Lists all messages in a specific thread."""
        self._validate_input(thread_id, "Thread ID")

        self.logger.info(f"Listing messages in thread {thread_id}.")
        return await self.make_api_call(f"threads/{thread_id}/messages", method="GET", params=kwargs)

    @log_error_decorator(logger=logger)
    async def wait_for_assistant_response(self, thread_id: str, timeout: int = 30) -> Dict:
        """Waits for the next assistant response in the specified thread, with a specified timeout."""
        self._validate_input(thread_id, "Thread ID")

        self.logger.info(f"Waiting for assistant's response in thread {thread_id} with timeout of {timeout} seconds.")
        end_time = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < end_time:
            messages = await self.list(thread_id)
            assistant_messages = [msg for msg in messages.get('data', []) if msg['role'] == 'assistant']
            if assistant_messages:
                self.logger.info(f"Received response from assistant in thread {thread_id}.")
                return assistant_messages[-1]
            await asyncio.sleep(1)
        
        self.logger.error(f"Timed out waiting for assistant's response in thread {thread_id}.")
        raise TimeoutError("Timed out waiting for assistant's response.")

    def _validate_input(self, input_value: str, input_name: str):
        if not input_value.strip():
            self.logger.error(f"{input_name} cannot be empty.")
            raise ValueError(f"{input_name} cannot be empty.")
