import json
from typing import Union


def validate_json(data):
    # 检查顶层键
    keys = ['gitlab_url', 'gitlab_api_token', 'registration_token', 'runner_url', 'runners']
    if not all(key in data for key in keys):
        return False

    # 检查URL和Token的类型
    if not all(isinstance(data[key], str) for key in
               ['gitlab_url', 'gitlab_api_token', 'registration_token', 'runner_url']):
        return False

    # 检查runners数组
    if not isinstance(data['runners'], list):
        return False

    # 检查每个runner的字段和类型
    runner_keys = ['description', 'tags', 'service', 'work_dir']
    for runner in data['runners']:
        if not all(key in runner for key in runner_keys):
            return False
        if not (isinstance(runner['description'], str) and isinstance(runner['tags'], list) and isinstance(
                runner['service'], str) and isinstance(runner['work_dir'], str)):
            return False
        if not all(isinstance(tag, str) for tag in runner['tags']):
            return False

    return True


def load_and_validate_json(file_path) -> Union[bool, dict]:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if not validate_json(data):
                return False
            return data
    except (json.JSONDecodeError, FileNotFoundError, Exception):
        return False
