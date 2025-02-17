import os
import importlib.util
from typing import Dict, Any, Optional

from project_config import CONFIG_DICT


class ConfigManager:
    console_config = {}
    user_config = {}
    default_config = {}

    @classmethod
    def init_class(cls):
        console_config = {}
        user_config = {}
        cls.default_config = CONFIG_DICT

    @classmethod
    def get(cls, key: str, default_value=None) -> Any:
        if key in ConfigManager.console_config:
            return ConfigManager.console_config[key]
        if key in ConfigManager.user_config:
            return ConfigManager.user_config[key]
        if key in ConfigManager.default_config:
            return ConfigManager.default_config[key]
        if default_value is not None:
            return default_value
        raise KeyError(f"配置项 '{key}' 不存在")
