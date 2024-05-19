import os
import subprocess
from pathlib import Path

import requests

from baosight.tools.utils import insert_tk_text


def download_gitlab_runner(runner_url, text_area):
    download_path = Path.home() / "Documents" / "gitlab-runner.exe"
    if not download_path.exists():
        insert_tk_text(text_area, "Downloading GitLab Runner...\n")
        response = requests.get(runner_url, stream=True)
        response.raise_for_status()
        with open(download_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        insert_tk_text(text_area, "Download completed.\n")
    else:
        insert_tk_text(text_area, "GitLab Runner already downloaded.\n")
    os.environ["PATH"] += os.pathsep + str(download_path.parent)


def unregister_existing_runners(gl, description, text_area):
    runners = gl.runners.all()
    for runner in runners:
        if runner.description == description:
            insert_tk_text(text_area, f"Unregistering existing runner: {runner.id} - {runner.description}\n")
            runner.delete()


def register_runner(gl, runner_info, registration_token, text_area):
    description = runner_info["description"]
    tags = runner_info["tags"]
    unregister_existing_runners(gl, description, text_area)
    info = {
        'description': description,
        'active': True,
        'tag_list': tags,
        'run_untagged': True,
        'locked': False,
        'access_level': 'not_protected',
        'token': registration_token
    }
    runner = gl.runners.create(info)
    insert_tk_text(text_area, f"Runner ID: {runner.id}, Description: {description} registered.\n")
    return runner.token


def setup_runner_on_windows(token, runner_info, gitlab_url, text_area):
    service_name = runner_info['service']
    working_directory = runner_info["work_dir"]

    # 将列表转换为字符串命令的选项
    install_options = " ".join(runner_info.get("install_options", []))
    start_options = " ".join(runner_info.get("start_options", []))
    register_options = " ".join(runner_info.get("register_options", [
        "--shell powershell",
        "--executor shell",
        "--locked false",
        "--run-untagged true",
        "--access-level not_protected"
    ]))

    # 构建命令列表
    commands = [
        f"gitlab-runner stop --service {service_name}",
        f"gitlab-runner uninstall --service {service_name}",
        f"gitlab-runner install --service {service_name} --working-directory {working_directory} {install_options}",
        f"gitlab-runner start --service {service_name} {start_options}",
        f"gitlab-runner register --non-interactive --url {gitlab_url} --token {token} {register_options}"
    ]

    # 确保工作目录存在
    work_dir_path = Path(working_directory)
    work_dir_path.mkdir(parents=True, exist_ok=True)

    # 删除现有的配置文件，如果存在
    config_path = work_dir_path / "config.json"
    config_path.unlink(missing_ok=True)

    # 执行命令
    for cmd in commands:
        result = subprocess.run(cmd, cwd=work_dir_path, shell=True, text=True, capture_output=True)
        stdout = result.stdout
        insert_tk_text(text_area, f"{stdout}\n")
        if result.returncode != 0:
            insert_tk_text(text_area, f"Error: {cmd}\n")
            break  # 如果任何命令失败，终止循环
        else:
            insert_tk_text(text_area, f"Succeed: {cmd}\n")
            print(f"Succeed: {cmd}")
