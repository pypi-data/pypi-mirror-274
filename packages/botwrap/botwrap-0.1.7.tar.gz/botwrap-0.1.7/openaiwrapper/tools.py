# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\tools.py

import logging
from typing import List, Dict, Any, Optional
from .decorators import log_error_decorator

logger = logging.getLogger(__name__)

class ToolsManager:
    def __init__(self, make_api_call, logger: Optional[logging.Logger] = None):
        """Initializes the ToolsManager with a callable for making API requests and a logger."""
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
    async def update_tools(self, assistant_id: str, tools_config: List[Dict[str, Any]]):
        """Updates the tools configuration for a specific Assistant asynchronously."""
        self._validate_input(assistant_id, "Assistant ID")
        self._validate_tools_config(tools_config)

        data = {"tools": tools_config}
        self.logger.info(f"Updating tools for assistant {assistant_id}.")
        return await self.make_api_call(f"assistants/{assistant_id}/tools", method="PATCH", data=data)

    @log_error_decorator(logger=logger)
    async def retrieve_tool_configuration(self, assistant_id: str) -> List[Dict[str, Any]]:
        """Retrieves the current tool configuration for a specific assistant asynchronously."""
        self._validate_input(assistant_id, "Assistant ID")

        self.logger.info(f"Retrieving tool configuration for assistant {assistant_id}.")
        response = await self.make_api_call(f"assistants/{assistant_id}/tools", method="GET")
        return response.get('tools', [])

    @log_error_decorator(logger=logger)
    async def remove_tool(self, assistant_id: str, tool_type: str):
        """Removes a specific tool based on tool type from an assistant's configuration asynchronously."""
        self._validate_input(assistant_id, "Assistant ID")
        self._validate_input(tool_type, "Tool type")

        self.logger.info(f"Removing tool {tool_type} from assistant {assistant_id}.")
        current_tools = await self.retrieve_tool_configuration(assistant_id)
        updated_tools = [tool for tool in current_tools if tool.get('type') != tool_type]
        return await self.update_tools(assistant_id, updated_tools)

    @log_error_decorator(logger=logger)
    async def submit_tool_outputs(self, thread_id: str, run_id: str, tool_outputs: List[Dict[str, Any]]):
        """Submits tool outputs for a specific run to continue processing asynchronously."""
        self._validate_input(thread_id, "Thread ID")
        self._validate_input(run_id, "Run ID")
        self._validate_tools_config(tool_outputs)

        self.logger.info(f"Submitting tool outputs for run {run_id} in thread {thread_id}.")
        data = {"tool_outputs": tool_outputs}
        return await self.make_api_call(f"threads/{thread_id}/runs/{run_id}/submit_tool_outputs", method="POST", data=data)

    def _validate_input(self, input_value: str, input_name: str):
        if not input_value:
            self.logger.error(f"{input_name} must be provided and cannot be empty.")
            raise ValueError(f"{input_name} must be provided and cannot be empty.")

    def _validate_tools_config(self, tools_config: List[Dict[str, Any]]):
        if not isinstance(tools_config, list) or not all(isinstance(tool, dict) for tool in tools_config):
            self.logger.error("tools_config must be a list of dictionaries.")
            raise ValueError("tools_config must be a list of dictionaries.")
