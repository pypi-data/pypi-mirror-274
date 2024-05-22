import json
import re
from typing import Tuple

class Config:

    _raw_config: dict = {}# Raw config data
    _value_config: dict = {}# Config data with dynamic values parsed

    @staticmethod
    def get(key: str, default=None):
        keys = key.split('.')
        value = Config._value_config
        for key in keys:
            if key not in value:
                return default
            value = value[key]
        return value

    @staticmethod
    def set(key: str, value):
        keys = key.split('.')
        raw = Config._raw_config
        val = Config._value_config
        for key in keys[:-1]:
            if key not in raw:
                raw[key] = {}
            if key not in val:
                val[key] = {}
            raw = raw[key]
            val = val[key]
        raw[keys[-1]] = value
        val[keys[-1]] = value

    @staticmethod
    def load() -> bool:
        try:
            with open('.proj.config', 'r') as config_file:
                # load into raw config
                Config._raw_config = json.load(config_file)
                # parse dynamic values
                Config._value_config = Config.parse(str(Config._raw_config), Config._raw_config)
                # Swaps single and double quotes to avoid json parsing issues
                Config._value_config = Config._value_config.replace('"', '\u200b')
                Config._value_config = Config._value_config.replace("'", '"')
                Config._value_config = Config._value_config.replace('\u200b', "'")
                # Load the stringified json
                Config._value_config = json.loads(Config._value_config)
            return True
        except FileNotFoundError:
            return False

    @staticmethod
    def save():
        with open('.proj.config', 'w') as config_file:
            json.dump(Config._raw_config, config_file, indent=4)

    @staticmethod
    def parse(string: str, dict_obj: dict) -> str:
        # Parse dynamic values
        def parse_match(match: re.Match[str]) -> str:
            return parse_dynamic_value(match.group(0), dict_obj)
        
        # Parse dynamic values recursively
        def parse_dynamic_value(dynamic_value, dict, recursive_check: list = None) -> str:
            if recursive_check is None: # Initialize the recursive check list
                recursive_check = []

            # Check for circular references
            if dynamic_value in recursive_check:
                raise Exception(
                    f'Circular reference detected: {' => '.join(recursive_check)} => {dynamic_value}')
            recursive_check.append(dynamic_value) # Add the current dynamic value to the recursive check list

            # Get the value from the dict
            dot_walk = dynamic_value[1:-1].split('.')
            for key in dot_walk:
                dict = dict[key]

            # If the value is a string, parse it
            if isinstance(dict, str) and dict.startswith('%') and dict.endswith('%'):
                return parse_dynamic_value(dict, dict_obj, recursive_check)
            return dict

        string = re.sub(r'%.*?%', parse_match, string)

        return string
 
Config.load()