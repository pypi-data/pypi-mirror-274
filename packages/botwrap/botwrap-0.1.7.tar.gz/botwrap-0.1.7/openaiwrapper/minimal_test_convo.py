import asyncio
import logging
import os
import aiohttp
import sys
from openaiwrapper.api_client import OpenAIAPIClient
from openaiwrapper.profiles import ProfileManager

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

async def make_api_call(session, url, method='POST', headers=None, json=None):
    try:
        async with session.request(method=method, url=url, headers=headers, json=json) as response:
            logger.info(f"Response status: {response.status}")
            response_text = await response.text()
            logger.debug(f"Response text: {response_text}")

            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

            return await response.json()
    except aiohttp.ClientResponseError as e:
        logger.error(f"HTTP error occurred: {e.status}, {e.message}")
        logger.error(f"Failed request data: {json}")
        try:
            error_details = await e.response.text()
            logger.error(f"Error details: {error_details}")
        except Exception:
            logger.error("Failed to retrieve error details.")
        raise
    except aiohttp.ClientError as e:
        logger.error("Client error during the API request.", exc_info=True)
        raise
    except Exception as e:
        logger.error("Unexpected error", exc_info=True)
        raise

async def main(api_key, profile_path):
    base_url = "https://api.openai.com/v1"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "OpenAI-Beta": "assistants=v2"  # Specific header for beta features
    }

    # Debugging: Print the profile path
    logger.info(f"Profile path: {profile_path}")

    # Load profile
    profile_manager = ProfileManager(logger)
    profile = profile_manager.load_profile_from_path(profile_path)
    
    # Create the assistant
    assistant_data = {
        "name": profile['name'],
        "instructions": profile['instructions'],
        "model": profile['model'],
        "tools": profile['tools'],
        "tool_resources": profile['tool_resources']
    }

    async with aiohttp.ClientSession() as session:
        assistant_url = f"{base_url}/assistants"
        logger.debug("Creating assistant")
        try:
            assistant_response = await make_api_call(session, assistant_url, method='POST', headers=headers, json=assistant_data)
            assistant_id = assistant_response['id']
            logger.info(f"Assistant created successfully: {assistant_response}")
        except Exception as e:
            logger.error(f"An error occurred while creating assistant: {e}")
            return

        # Step 1: Create a thread
        thread_url = f"{base_url}/threads"
        logger.debug("Creating thread")
        try:
            thread_response = await make_api_call(session, thread_url, method='POST', headers=headers, json={})
            thread_id = thread_response['id']
            logger.info(f"Thread created successfully: {thread_response}")
        except Exception as e:
            logger.error(f"An error occurred while creating thread: {e}")
            return

        # Step 2: Add a message to the thread
        message_url = f"{base_url}/threads/{thread_id}/messages"
        message_data = {
            "role": "user",
            "content": "I need to solve the equation `3x + 11 = 14`. Can you help me?"
        }
        logger.debug(f"Adding message to thread {thread_id}: {message_data}")
        try:
            message_response = await make_api_call(session, message_url, method='POST', headers=headers, json=message_data)
            logger.info(f"Message added successfully: {message_response}")
        except Exception as e:
            logger.error(f"An error occurred while adding message: {e}")
            return

        # Step 3: Create a run with the assistant
        run_url = f"{base_url}/threads/{thread_id}/runs"
        run_data = {
            "assistant_id": assistant_id,
            "instructions": "Please address the user as Jane Doe. The user has a premium account."
        }
        logger.debug(f"Creating run for thread {thread_id} with assistant {assistant_id}")
        try:
            run_response = await make_api_call(session, run_url, method='POST', headers=headers, json=run_data)
            run_id = run_response['id']
            logger.info(f"Run created successfully: {run_response}")
        except Exception as e:
            logger.error(f"An error occurred while creating run: {e}")
            return

        # Step 4: Poll for run completion
        run_completion_url = f"{base_url}/threads/{thread_id}/runs/{run_id}"
        start_time = asyncio.get_event_loop().time()
        timeout = 300
        while True:
            if asyncio.get_event_loop().time() - start_time > timeout:
                logger.error("Polling for run completion timed out.")
                return

            try:
                run_completion_response = await make_api_call(session, run_completion_url, method='GET', headers=headers)
                run_status = run_completion_response.get('status')
                if run_status in ['completed', 'failed']:
                    logger.info(f"Run completed with status: {run_status}")
                    break
            except Exception as e:
                logger.error(f"An error occurred while polling for run completion: {e}")

            await asyncio.sleep(10)

        # Step 5: Retrieve and print the messages
        messages_url = f"{base_url}/threads/{thread_id}/messages"
        logger.debug(f"Retrieving messages for thread {thread_id}")
        try:
            messages_response = await make_api_call(session, messages_url, method='GET', headers=headers)
            messages = messages_response.get('data', [])
            logger.info("Messages:")
            for message in messages:
                if message['content'][0]['type'] == "text":
                    logger.info({"role": message['role'], "message": message['content'][0]['text']['value']})
        except Exception as e:
            logger.error(f"An error occurred while retrieving messages: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python minimal_test_convo.py <api_key> <profile_path>")
    else:
        api_key = sys.argv[1]
        profile_path = sys.argv[2]
        asyncio.run(main(api_key, profile_path))
