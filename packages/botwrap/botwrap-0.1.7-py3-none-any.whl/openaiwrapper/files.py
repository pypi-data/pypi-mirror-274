# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\files.py

import os
import aiohttp
import logging
from typing import Any, Dict, Optional
from .exceptions import OpenAIWrapperError
from .decorators import log_error_decorator

logger = logging.getLogger(__name__)

class FileManager:
    def __init__(self, api_key: str, make_request_func, logger: Optional[logging.Logger] = None):
        self.api_key = api_key
        self.make_request = make_request_func
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
    async def upload_file(self, file_path: str, purpose: str = 'assistants', **kwargs) -> Dict[str, Any]:
        self.validate_file_for_upload(file_path)

        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = aiohttp.FormData()
        data.add_field('file', open(file_path, 'rb'), filename=os.path.basename(file_path), content_type='application/octet-stream')
        data.add_field('purpose', purpose)

        try:
            response = await self.make_request("POST", "files", headers=headers, data=data)
            self.logger.info(f"File {file_path} uploaded successfully.")
            return response
        except aiohttp.ClientResponseError as e:
            self.logger.error(f"HTTPError during file upload: {e.status}, {e.message}")
            raise OpenAIWrapperError(f"HTTPError during file upload: {e.status}, {e.message}")
        except Exception as e:
            self.logger.error(f"Unexpected error during file upload: {str(e)}")
            raise OpenAIWrapperError(f"Unexpected error during file upload: {str(e)}")

    def validate_file_for_upload(self, file_path: str):
        if not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
            self.logger.error(f"File {file_path} does not exist or is not readable.")
            raise ValueError(f"File {file_path} does not exist or is not readable.")

        max_file_size = 52428800  # 50 MB
        file_size = os.path.getsize(file_path)
        if file_size > max_file_size:
            self.logger.error(f"File exceeds the maximum allowed size of {max_file_size} bytes.")
            raise ValueError(f"File exceeds the maximum allowed size of {max_file_size} bytes.")

    async def create_and_upload_files(self, file_paths: list, purpose: str = 'assistants') -> list:
        file_ids = []
        for file_path in file_paths:
            response = await self.upload_file(file_path, purpose=purpose)
            file_ids.append(response['id'])
        return file_ids
