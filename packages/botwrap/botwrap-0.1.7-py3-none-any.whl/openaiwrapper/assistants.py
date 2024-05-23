# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\assistants.py

import logging
from typing import List, Dict, Optional, Any
from .profiles import ProfileManager
from .decorators import log_error_decorator

class AssistantManager:
    def __init__(self, make_api_call, logger: Optional[logging.Logger] = None):
        self.make_api_call = make_api_call
        self.logger = logger or self._setup_logger()
        self.profile_manager = ProfileManager(logger)

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    @log_error_decorator(logger=None)
    async def create_assistant(self, profile_name: Optional[str] = None, profile_path: Optional[str] = None, name: Optional[str] = None, instructions: Optional[str] = None, model: Optional[str] = None, tools: Optional[List[Dict[str, Any]]] = None, tool_resources: Optional[Dict[str, Any]] = None, **kwargs) -> Dict:
        if profile_name:
            profile = self.profile_manager.load_profile(profile_name)
            self.logger.info(f"Creating new assistant with profile: {profile_name}")
            data = {**profile, **kwargs}
        elif profile_path:
            profile = self.profile_manager.load_profile_from_path(profile_path)
            self.logger.info(f"Creating new assistant with profile from path: {profile_path}")
            data = {**profile, **kwargs}
        else:
            if not (name and instructions and model):
                self.logger.error("Name, instructions, and model must be provided if no profile is used.")
                raise ValueError("Name, instructions, and model must be provided if no profile is used.")
            data = {
                "name": name,
                "instructions": instructions,
                "model": model,
                "tools": tools or [],
                "tool_resources": tool_resources or {},
                **kwargs
            }
            self.logger.info(f"Creating new assistant with name: {name}")

        return await self.make_api_call("assistants", method="POST", data=data)

    @log_error_decorator(logger=None)
    async def retrieve(self, assistant_id: str) -> Dict:
        self._validate_input(assistant_id, "Assistant ID")
        self.logger.info(f"Retrieving assistant with ID: {assistant_id}")
        return await self.make_api_call(f"assistants/{assistant_id}", method="GET")

    @log_error_decorator(logger=None)
    async def update(self, assistant_id: str, updates: Dict[str, Any]) -> Dict:
        if 'tools' in updates:
            await self._validate_tools_config(updates['tools'])
        self.logger.info(f"Updating assistant with ID: {assistant_id}")
        return await self.make_api_call(f"assistants/{assistant_id}", method="PATCH", data=updates)

    @log_error_decorator(logger=None)
    async def delete(self, assistant_id: str) -> Dict:
        self._validate_input(assistant_id, "Assistant ID")
        self.logger.info(f"Deleting assistant with ID: {assistant_id}")
        return await self.make_api_call(f"assistants/{assistant_id}", method="DELETE")

    @log_error_decorator(logger=None)
    async def list(self, **kwargs) -> List[Dict]:
        self.logger.info("Listing all assistants")
        response = await self.make_api_call("assistants", method="GET", params=kwargs)
        return response.get("data", [])

    def _validate_input(self, input_value: str, input_name: str):
        if not input_value:
            self.logger.error(f"{input_name} must be provided and cannot be empty.")
            raise ValueError(f"{input_name} must be provided and cannot be empty.")
