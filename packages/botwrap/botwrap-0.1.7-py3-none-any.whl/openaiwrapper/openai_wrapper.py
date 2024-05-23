# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\openai_wrapper.py

import asyncio
import logging
from typing import Dict, List, Any, Optional
from .api_client import OpenAIAPIClient
from .threads import ThreadManager
from .messages import MessageManager
from .runs import RunManager
from .tools import ToolsManager
from .vector_store_manager import VectorStoreManager
from .assistants import AssistantManager

class OpenAIWrapper:
    def __init__(self, api_key: str, logger: Optional[logging.Logger] = None):
        self.api_client = OpenAIAPIClient(api_key=api_key, logger=logger)
        self.logger = logger or logging.getLogger(__name__)
        self._setup_logging()
        self.setup_managers()

    def _setup_logging(self):
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levellevelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def __aenter__(self):
        await self.api_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.api_client.__aexit__(exc_type, exc_val, exc_tb)

    def setup_managers(self):
        make_api_call = self.api_client.make_api_call
        self.thread_manager = ThreadManager(make_api_call, self.logger)
        self.message_manager = MessageManager(make_api_call, self.logger)
        self.run_manager = RunManager(make_api_call, self.logger)
        self.tools_manager = ToolsManager(make_api_call, self.logger)
        self.vector_store_manager = VectorStoreManager(make_api_call, self.logger)
        self.assistant_manager = AssistantManager(make_api_call, self.logger)

    async def run_assistant_workflow(self, assistant_id: str, initial_message: str) -> Dict[str, Any]:
        """Encapsulates the logic of running an assistant workflow into a single method."""
        try:
            # Step 1: Create a thread
            thread_response = await self.thread_manager.create(assistant_id=assistant_id)
            thread_id = thread_response['id']
            self.logger.info(f"Thread created successfully: {thread_response}")

            # Step 2: Add a message to the thread
            message_response = await self.message_manager.create(thread_id=thread_id, content=initial_message, role="user")
            self.logger.info(f"Message added successfully: {message_response}")

            # Step 3: Create a run with the assistant
            run_response = await self.run_manager.create(thread_id=thread_id, assistant_id=assistant_id)
            run_id = run_response['id']
            self.logger.info(f"Run created successfully: {run_response}")

            # Step 4: Poll for run completion
            run_status = await self.run_manager.wait_for_run_completion(thread_id=thread_id, run_id=run_id)
            self.logger.info(f"Run completed: {run_status}")

            # Step 5: Retrieve and return the messages
            messages_response = await self.message_manager.list(thread_id=thread_id)
            messages = messages_response.get('data', [])
            return {"thread_id": thread_id, "messages": messages}
        except Exception as e:
            self.logger.error(f"An error occurred during the assistant workflow: {e}")
            raise

    async def create_thread_for_existing_assistant(self, assistant_id: str, initial_message: str) -> Dict[str, Any]:
        """Creates a new thread for an existing assistant."""
        return await self.run_assistant_workflow(assistant_id=assistant_id, initial_message=initial_message)

    async def create_assistant_and_thread(self, name: str, model: str, instructions: str, initial_message: str, tools: List[Dict[str, Any]] = [], tool_resources: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Creates a new assistant and a new thread for that assistant."""
        try:
            assistant = await self.create_assistant(name=name, model=model, instructions=instructions, tools=tools, tool_resources=tool_resources)
            assistant_id = assistant['id']
            return await self.run_assistant_workflow(assistant_id=assistant_id, initial_message=initial_message)
        except Exception as e:
            self.logger.error(f"Failed to create assistant and thread: {e}")
            raise

    async def reply_to_existing_thread(self, thread_id: str, message: str) -> Dict[str, Any]:
        """Replies to a message on an existing thread."""
        try:
            response = await self.message_manager.create(thread_id=thread_id, content=message, role="user")
            self.logger.info(f"Message replied successfully: {response}")
            messages_response = await self.message_manager.list(thread_id=thread_id)
            messages = messages_response.get('data', [])
            return {"thread_id": thread_id, "messages": messages}
        except Exception as e:
            self.logger.error(f"Failed to reply to existing thread: {e}")
            raise

    async def upload_file(self, file_path: str, purpose: str = "answers") -> Dict[str, Any]:
        try:
            return await self.api_client.file_manager.upload_file(file_path=file_path, purpose=purpose)
        except Exception as e:
            self.logger.error(f"Failed to upload file: {e}")
            raise

    async def create_assistant(self, name: str, model: str, instructions: str, tools: List[Dict[str, Any]] = [], tool_resources: Dict[str, Any] = {}) -> Dict[str, Any]:
        try:
            return await self.assistant_manager.create_assistant(name=name, model=model, instructions=instructions, tools=tools, tool_resources=tool_resources)
        except Exception as e:
            self.logger.error(f"Failed to create assistant: {e}")
            raise

    def _validate_input(self, input_value: str, input_name: str):
        if not input_value:
            self.logger.error(f"{input_name} must be provided and cannot be empty.")
            raise ValueError(f"{input_name} must be provided and cannot be empty.")
