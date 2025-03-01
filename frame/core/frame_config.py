import json
import os
import importlib.util
from typing import Any

from project_config import CONFIG_DICT

class ConfigManager:
    user_config = {}
    default_config = {}

    @classmethod
    def init_class(cls):
        # 获取测试床
        cls.user_config = {}
        cls.default_config = CONFIG_DICT
        # 读取用户自定义配置文件
        print(' =========================================== ')
        self_conf = None
        print('自定义配置文件格式应为 : ', '{"user_conf": {},"frame_conf": {}}')
        if os.path.exists('self_conf.json'):
            print('根目录存在自定义配置文件 : ', 'self_conf.json')
            self_conf = json.loads(open('self_conf.json').read())
            for k in self_conf['frame_conf']:
                cls.default_config[k] = self_conf['frame_conf'][k]
        else:
            print('根目录不存在自定义配置文件 : ', 'self_conf.json')
        print('当前测试床为 : ', cls.default_config['TEST_BED'])
        task_bed_path = os.path.join(os.path.join(cls.default_config['PROJECT_NAME'], 'config'), cls.default_config['TEST_BED'] + '.json')
        print('测试床路径为 : ', task_bed_path)
        cls.user_config = json.loads(open(task_bed_path).read())
        if self_conf is not None:
            for k in self_conf['user_conf']:
                cls.user_config[k] = self_conf['user_conf'][k]
        print(' =========================================== ')

    @classmethod
    def get(cls, key: str, default_value=None) -> Any:
        if key in ConfigManager.user_config:
            return ConfigManager.user_config[key]
        if key in ConfigManager.default_config:
            return ConfigManager.default_config[key]
        if default_value is not None:
            return default_value
        raise KeyError(f"配置项 '{key}' 不存在")
