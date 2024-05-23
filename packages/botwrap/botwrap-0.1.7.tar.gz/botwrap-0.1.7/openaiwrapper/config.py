# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\config.py

import os
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

class Config:
    """
    Base configuration class containing settings applicable to all environments.
    """
    API_KEY = os.getenv("OPENAI_API_KEY")
    BASE_URL = "https://api.openai.com/v1"
    LOG_FILE = os.getenv("LOG_FILE", "api_calls.log")
    TOOLS = {
        "code_interpreter": {
            "enabled": True,
            "config_key": "example_value"
        }
    }

    @classmethod
    def validate(cls):
        """Validates the necessary configurations are set."""
        if not cls.API_KEY:
            raise ValueError("API_KEY must be set in environment variables.")
        if not cls.BASE_URL:
            raise ValueError("BASE_URL must be set in configuration.")

class DevelopmentConfig(Config):
    """
    Configuration for development environment with additional debugging and logging capabilities.
    """
    DEBUG = True
    LOG_LEVEL = 'DEBUG'  # Set higher log level for development to aid in debugging

class ProductionConfig(Config):
    """
    Configuration for production environment with optimizations and security enhancements.
    """
    DEBUG = False
    LOG_LEVEL = 'WARNING'  # Lower log level to avoid sensitive data exposure

class StagingConfig(Config):
    """
    Configuration for staging environment, mirroring production settings with slight adjustments.
    """
    DEBUG = False
    LOG_LEVEL = 'INFO'  # Moderate log level for operational visibility without too much noise

def get_config():
    """
    Determines which configuration to use based on the ENVIRONMENT environment variable.
    Returns the appropriate configuration class.
    """
    environment = os.getenv('ENVIRONMENT', 'development').lower()
    if environment == 'production':
        config = ProductionConfig
    elif environment == 'staging':
        config = StagingConfig
    else:
        config = DevelopmentConfig

    config.validate()  # Validate the selected configuration
    return config

# Example usage in your application
# from config import get_config
# current_config = get_config()
# api_key = current_config.API_KEY
# debug = current_config.DEBUG
