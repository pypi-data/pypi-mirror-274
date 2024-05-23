# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\profiles.py

import json
import os
import logging
from typing import Dict, Optional

class ProfileManager:
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or self._setup_logger()
        self.profiles_dir = os.path.join(os.path.dirname(__file__), 'profiles')
        self._ensure_profiles_dir_exists()

    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the ProfileManager class."""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levellevelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def _ensure_profiles_dir_exists(self):
        """Ensure the profiles directory exists."""
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)
            self.logger.info(f"Created profiles directory at {self.profiles_dir}")

    def load_profile(self, profile_name: str) -> Dict:
        """Load a profile by name."""
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")
        if not os.path.exists(profile_path):
            self.logger.error(f"Profile '{profile_name}' not found.")
            raise FileNotFoundError(f"Profile '{profile_name}' not found.")
        
        with open(profile_path, 'r') as file:
            profile = json.load(file)
            self.logger.info(f"Loaded profile '{profile_name}' from {profile_path}")
            return profile

    def load_profile_from_path(self, profile_path: str) -> Dict:
        """Load a profile from a specified path."""
        if not os.path.exists(profile_path):
            self.logger.error(f"Profile at path '{profile_path}' not found.")
            raise FileNotFoundError(f"Profile at path '{profile_path}' not found.")
        
        with open(profile_path, 'r') as file:
            profile = json.load(file)
            self.logger.info(f"Loaded profile from path '{profile_path}'")
            return profile

    def save_profile(self, profile_name: str, profile_data: Dict):
        """Save a profile with the given name and data."""
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")
        with open(profile_path, 'w') as file:
            json.dump(profile_data, file, indent=4)
            self.logger.info(f"Saved profile '{profile_name}' to {profile_path}")

    def list_profiles(self) -> Dict[str, str]:
        """List all available profiles."""
        profiles = {}
        for file_name in os.listdir(self.profiles_dir):
            if file_name.endswith('.json'):
                profile_name = file_name[:-5]
                profiles[profile_name] = os.path.join(self.profiles_dir, file_name)
        self.logger.info(f"Available profiles: {list(profiles.keys())}")
        return profiles
