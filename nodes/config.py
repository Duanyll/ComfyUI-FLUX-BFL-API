import os
import configparser
from urllib.parse import urljoin

class ConfigLoader:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        config_path = os.path.join(parent_dir, "config.ini")
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        
        # Regional endpoints for finetuning (required by BFL API)
        self.regional_endpoints = {
            "us": "https://api.us1.bfl.ai",
            "eu": "https://api.eu1.bfl.ai"
        }

    def get_key(self, section, key):
        try:
            return self.config[section][key]
        except KeyError:
            raise KeyError(f"{key} not found in section {section} of config file.")

    def create_url(self, path, region=None):
        """
        Create URL for API endpoints.
        
        Args:
            path: API endpoint path
            region: Optional region for finetuning operations ("us" or "eu")
                   If provided, uses regional endpoint instead of global
        """
        try:
            if region and region in self.regional_endpoints:
                base_url = self.regional_endpoints[region]
                return urljoin(base_url, f"/v1/{path}")
            else:
                base_url = self.get_key('API', 'BASE_URL')
                return urljoin(base_url, path)
        except KeyError as e:
            raise KeyError(f"Error constructing URL: {str(e)}")

    def get_regional_endpoint(self, region):
        """Get the full regional endpoint URL for a given region."""
        if region not in self.regional_endpoints:
            raise ValueError(f"Invalid region '{region}'. Must be one of: {list(self.regional_endpoints.keys())}")
        return self.regional_endpoints[region]
            
    def get_x_key(self):
        return self.get_key('API', 'X_KEY')

# Create a singleton instance to be shared across modules
config_loader = ConfigLoader() 


class CreateBFLConfig:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_url": ("STRING", {"default": "https://api.bfl.ml/v1/"}),
                "x_key": ("STRING", {"default": "your-key"})
            }
        }
        
    FUNCTION = "create_bfl_config"
    RETURN_TYPES = ("BFL_CONFIG",)
    CATEGORY = "BFL"
    
    def create_bfl_config(self, base_url, x_key):
        config = ConfigLoader()
        config.config['API']['BASE_URL'] = base_url
        config.config['API']['X_KEY'] = x_key
        return (config, )
    

NODE_CLASS_MAPPINGS = {
    "CreateBFLConfig_BFL": CreateBFLConfig
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreateBFLConfig_BFL": "Create BFL Config"
}