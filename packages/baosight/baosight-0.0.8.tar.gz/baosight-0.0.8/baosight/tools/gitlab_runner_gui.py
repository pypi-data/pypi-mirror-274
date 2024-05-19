import ctypes
import json
import os
import sys
import threading
import tkinter as tk
from pathlib import Path
from subprocess import Popen
from tkinter import ttk, filedialog  # 导入 filedialog
from typing import Union

import gitlab
import requests


def show_message(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x1000 | 0x40)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin(argv=None):
    if argv is None and sys.argv:
        argv = sys.argv
    if hasattr(sys, '_MEIPASS'):
        arguments = map(str, argv[1:])
    else:
        arguments = map(str, argv)
    cmd = ' '.join(arguments)
    # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, cmd, None, 0)
    show_message("错误", "请以管理员身份运行.")
    sys.exit()


def download_gitlab_runner(runner_url):
    download_path = Path.home() / "Documents" / "gitlab-runner.exe"
    if not download_path.exists():
        print("Downloading GitLab Runner...")
        response = requests.get(runner_url, stream=True)
        response.raise_for_status()
        with open(download_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download completed.")
    else:
        print("GitLab Runner already downloaded.")
    os.environ["PATH"] += os.pathsep + str(download_path.parent)


def unregister_existing_runners(gl, description):
    runners = gl.runners.all()
    for runner in runners:
        if runner.description == description:
            print(f"Unregistering existing runner: {runner.id} - {runner.description}")
            runner.delete()


def register_runner(gl, runner_info, registration_token):
    description = runner_info["description"]
    tags = runner_info["tags"]
    unregister_existing_runners(gl, description)
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
    print(f"Runner ID: {runner.id}, Description: {description} registered.")
    return runner.token


def setup_runner_on_windows(token, runner_info, gitlab_url):
    service_name = runner_info['service']
    working_directory = runner_info["work_dir"]
    commands = [
        f"gitlab-runner stop --service {service_name}",
        f"gitlab-runner uninstall --service {service_name}",
        f"gitlab-runner install --service {service_name} --working-directory {working_directory}",
        f"gitlab-runner start --service {service_name}",
        f"gitlab-runner register --non-interactive --url {gitlab_url} "
        f"--shell cmd --token {token} --executor shell --locked false --run-untagged true --access-level not_protected"
    ]
    work_dir_path = Path(working_directory)
    work_dir_path.mkdir(parents=True, exist_ok=True)
    for cmd in commands:
        Popen(cmd, cwd=work_dir_path, shell=True).wait()


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


def deploy(config_button, progress_bar, status_label, root, start_button):
    start_button.config(state=tk.DISABLED)
    config_path = config_button.invoke()
    if not config_path:
        start_button.config(state=tk.NORMAL)
        return
    config = load_and_validate_json(config_path)
    if not config:
        show_message("错误", "安装文件无效.")
        start_button.config(state=tk.NORMAL)
        return
    download_gitlab_runner(config['runner_url'])
    gl = gitlab.Gitlab(config['gitlab_url'], private_token=config['gitlab_api_token'])
    for i, runner_info in enumerate(config['runners']):
        runner_token = register_runner(gl, runner_info, config['registration_token'])
        if not runner_token:
            show_message("错误", "无法注册 runner.")
            return
        setup_runner_on_windows(runner_token, runner_info, config['gitlab_url'])
        progress_bar['value'] += 100 / len(config['runners'])
        status_label.config(text=f"已完成: {runner_info['description']}")
        progress_bar.update()
    start_button.config(text="完成", command=root.destroy)
    start_button.config(state=tk.NORMAL)


def center_window(root):
    """ 将窗口居中放置在屏幕上 """
    root.update_idletasks()  # 更新窗口状态
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def create_installation_ui():
    if not is_admin():
        run_as_admin()
    print("Script is running with administrator privileges.")
    root = tk.Tk()
    root.title("Gitlab Runner Installer")

    # 添加文件选择按钮
    config_button = tk.Button(root, text="选择配置文件",
                              command=lambda: filedialog.askopenfilename(filetypes=[("JSON files", "*.json")]))

    progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate', maximum=100)
    progress_bar.pack(pady=20)
    progress_bar.pack(padx=10)
    status_label = tk.Label(root, text="准备安装...")
    status_label.pack(pady=10)
    start_button = tk.Button(root, text="开始安装", command=lambda: threading.Thread(target=deploy, args=(
        config_button, progress_bar, status_label, root, start_button)).start())
    start_button.pack(pady=20)
    center_window(root)
    root.mainloop()


if __name__ == "__main__":
    create_installation_ui()
