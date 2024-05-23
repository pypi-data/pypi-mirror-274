# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\test_convo.py

import asyncio
import logging
import os
from openaiwrapper.config import get_config
from openaiwrapper.api_client import OpenAIAPIClient

# Setup logging
log_path = os.path.join(os.path.dirname(__file__), 'api_calls.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# File handler for logging
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.DEBUG)

# Console handler for logging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Formatter for the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info(f"Logging to file: {log_path}")

# Load configuration
config = get_config()

async def main():
    async with OpenAIAPIClient(api_key=config.API_KEY, logger=logger) as client:
        assistant_manager = client.assistant_manager
        thread_manager = client.thread_manager
        message_manager = client.message_manager
        run_manager = client.run_manager

        # Step 1: Create or retrieve a pre-configured assistant
        assistant_name = "Test Assistant"
        assistant_id = None

        assistants = await assistant_manager.list()
        for assistant in assistants:
            if assistant['name'] == assistant_name:
                assistant_id = assistant['id']
                break

        if not assistant_id:
            logger.info(f"Assistant '{assistant_name}' not found, creating a new one.")
            assistant = await assistant_manager.create_assistant(
                name=assistant_name,
                model='gpt-4-1106-preview',  # Example model
                instructions='You are a personal math tutor. Write and run code to answer math questions.',
                tools=[{"type": "code_interpreter"}]
            )
            assistant_id = assistant['id']

        logger.info(f"Using assistant ID: {assistant_id}")

        # Step 2: Start a conversation with the assistant by creating a thread
        try:
            # Simplified request data for creating a thread
            request_data = {
                'assistant_id': assistant_id,
                # Removed tool_resources and metadata for debugging
            }
            logger.debug(f"Creating thread with data: {request_data}")
            thread = await thread_manager.create(**request_data)
            thread_id = thread['id']
            logger.info(f"Started conversation with thread ID: {thread_id}")

            # Step 3: Send a message to the assistant
            initial_message = "I need to solve the equation `3x + 11 = 14`. Can you help me?"
            await message_manager.create(thread_id=thread_id, content=initial_message, role="user")
            logger.info(f"Sent message to thread ID: {thread_id} with content: {initial_message}")

            # Step 4: Create a run and wait for it to complete
            run = await run_manager.create_and_poll(
                thread_id=thread_id,
                assistant_id=assistant_id,
                instructions="Please address the user as Jane Doe. The user has a premium account."
            )
            logger.info(f"Run completed with status: {run['status']}")

            # Step 5: Retrieve and print the messages
            if run['status'] == "completed":
                messages = await message_manager.list(thread_id=thread_id)
                logger.info("Messages:")
                for message in messages.get('data', []):
                    if message['content'][0]['type'] == "text":
                        logger.info({"role": message['role'], "message": message['content'][0]['text']['value']})

            # Clean up: Delete the assistant
            await assistant_manager.delete(assistant_id)
            logger.info(f"Assistant '{assistant_name}' deleted.")

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            # Log detailed request and response for debugging
            if hasattr(e, 'request') and e.request:
                logger.error(f"Request data: {e.request.body}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response content: {e.response.content}")
                logger.error(f"Response status code: {e.response.status}")
                try:
                    response_text = await e.response.text()
                    logger.error(f"Response text: {response_text}")
                except Exception as response_read_error:
                    logger.error(f"Failed to read response text: {response_read_error}")

if __name__ == "__main__":
    asyncio.run(main())
