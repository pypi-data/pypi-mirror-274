# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\runs.py

import logging
import asyncio
from typing import Dict, Any, Optional
from .decorators import log_error_decorator

logger = logging.getLogger(__name__)

class RunManager:
    def __init__(self, make_api_call, logger: Optional[logging.Logger] = None):
        """Initializes the RunManager with a callable for making API requests and a logger."""
        self.make_api_call = make_api_call
        self.logger = logger or self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup logger configuration."""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levellevelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    async def create(self, thread_id: str, assistant_id: str, **kwargs) -> Dict[str, Any]:
        """Create a new run within a specific thread."""
        self._validate_input(thread_id, "Thread ID")
        self._validate_input(assistant_id, "Assistant ID")

        self.logger.info(f"Creating run for assistant {assistant_id} in thread {thread_id}")
        data = {"assistant_id": assistant_id, **kwargs}
        return await self.make_api_call(f"threads/{thread_id}/runs", method="POST", data=data)

    async def create_and_poll(self, thread_id: str, assistant_id: str, **kwargs) -> Dict[str, Any]:
        """Create a run and poll until it completes."""
        run = await self.create(thread_id, assistant_id, **kwargs)
        run_id = run['id']
        return await self.wait_for_run_completion(thread_id, run_id)

    async def retrieve(self, thread_id: str, run_id: str) -> Dict[str, Any]:
        """Retrieve details about a specific run."""
        self._validate_input(thread_id, "Thread ID")
        self._validate_input(run_id, "Run ID")

        self.logger.info(f"Retrieving run {run_id} from thread {thread_id}")
        return await self.make_api_call(f"threads/{thread_id}/runs/{run_id}", method="GET")

    async def list(self, thread_id: str, **kwargs) -> Dict[str, Any]:
        """List all runs within a specific thread."""
        self._validate_input(thread_id, "Thread ID")

        self.logger.info(f"Listing runs in thread {thread_id}")
        return await self.make_api_call(f"threads/{thread_id}/runs", method="GET", params=kwargs)

    async def wait_for_run_completion(self, thread_id: str, run_id: str, timeout: int = 300) -> Dict[str, Any]:
        """Waits for a run to complete or fail within the specified timeout period."""
        self._validate_input(thread_id, "Thread ID")
        self._validate_input(run_id, "Run ID")

        self.logger.info(f"Waiting for run {run_id} to complete in thread {thread_id}")
        start_time = asyncio.get_event_loop().time()
        while True:
            if asyncio.get_event_loop().time() - start_time > timeout:
                msg = f"Timeout waiting for run {run_id} to complete."
                self.logger.error(msg)
                raise TimeoutError(msg)

            run_status = await self.retrieve(thread_id, run_id)
            if run_status.get('status') in ['completed', 'failed']:
                self.logger.info(f"Run {run_id} completed with status: {run_status['status']}")
                return run_status

            await asyncio.sleep(10)  # Consider adaptive polling strategy based on expected run times.

    def _validate_input(self, input_value: str, input_name: str):
        if not input_value:
            self.logger.error(f"{input_name} must be provided and cannot be empty.")
            raise ValueError(f"{input_name} must be provided and cannot be empty.")
