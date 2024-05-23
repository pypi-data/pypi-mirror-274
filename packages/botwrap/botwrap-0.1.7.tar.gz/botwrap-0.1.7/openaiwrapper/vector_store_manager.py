# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\vector_store_manager.py

import logging
from typing import List, Dict, Any, Optional
from .decorators import log_error_decorator

logger = logging.getLogger(__name__)

class VectorStoreManager:
    def __init__(self, make_api_call, logger: Optional[logging.Logger] = None):
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
    async def create_vector_store(self, name: str, file_ids: List[str], expires_after: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self._validate_input(name, "Name")
        self._validate_file_ids(file_ids)

        self.logger.info(f"Creating vector store with name: {name}")
        data = {"name": name, "file_ids": file_ids, "expires_after": expires_after}
        return await self.make_api_call("beta/vector_stores/create_and_poll", method="POST", data=data)

    @log_error_decorator(logger=logger)
    async def delete_vector_store(self, vector_store_id: str) -> None:
        self._validate_input(vector_store_id, "Vector store ID")

        self.logger.info(f"Deleting vector store with ID: {vector_store_id}")
        await self.make_api_call(f"beta/vector_stores/{vector_store_id}", method="DELETE")

    @log_error_decorator(logger=logger)
    async def list_vector_stores(self, **kwargs) -> List[Dict[str, Any]]:
        self.logger.info("Listing all vector stores.")
        response = await self.make_api_call("beta/vector_stores/list", method="GET", params=kwargs)
        return response.get("data", [])

    @log_error_decorator(logger=logger)
    async def add_files_to_vector_store(self, vector_store_id: str, file_ids: List[str]) -> Dict[str, Any]:
        self._validate_input(vector_store_id, "Vector store ID")
        self._validate_file_ids(file_ids)

        self.logger.info(f"Adding files to vector store with ID: {vector_store_id}")
        data = {"vector_store_id": vector_store_id, "file_ids": file_ids}
        return await self.make_api_call("beta/vector_stores/files/add", method="POST", data=data)

    @log_error_decorator(logger=logger)
    async def remove_files_from_vector_store(self, vector_store_id: str, file_ids: List[str]) -> Dict[str, Any]:
        self._validate_input(vector_store_id, "Vector store ID")
        self._validate_file_ids(file_ids)

        self.logger.info(f"Removing files from vector store with ID: {vector_store_id}")
        data = {"vector_store_id": vector_store_id, "file_ids": file_ids}
        return await self.make_api_call("beta/vector_stores/files/remove", method="POST", data=data)

    def _validate_input(self, input_value: str, input_name: str):
        if not input_value:
            self.logger.error(f"{input_name} must be provided and cannot be empty.")
            raise ValueError(f"{input_name} must be provided and cannot be empty.")

    def _validate_file_ids(self, file_ids: List[str]):
        if not file_ids or not all(isinstance(file_id, str) for file_id in file_ids):
            self.logger.error("file_ids must be a list of strings.")
            raise ValueError("file_ids must be a list of strings.")
