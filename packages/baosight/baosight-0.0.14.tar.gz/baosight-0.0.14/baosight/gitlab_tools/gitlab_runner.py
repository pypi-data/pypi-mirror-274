import tkinter as tk

import gitlab

from baosight.gitlab_tools.config import load_and_validate_json
from baosight.gitlab_tools.core import download_gitlab_runner, register_runner, \
    setup_runner_on_windows
from baosight.gui.gl_runner_installer import create_installation_ui
from baosight.tools.utils import show_message, is_admin, run_as_admin, insert_tk_text


def deploy(config_path=None, gui_objs=None):
    progress_bar = None
    root = None
    start_button = None
    text_area = None
    if gui_objs:
        progress_bar = gui_objs['progress_bar']
        config_button = gui_objs["config_button"]
        root = gui_objs['root']
        start_button = gui_objs['start_button']
        text_area = gui_objs['text_area']
        start_button.config(state=tk.DISABLED)
        config_path = config_button.invoke()
        if not config_path:
            start_button.config(state=tk.NORMAL)
            return
    config = load_and_validate_json(config_path)
    if not config:
        show_message("错误", "安装文件无效.")
        if gui_objs:
            start_button.config(state=tk.NORMAL)
        return
    download_gitlab_runner(config['runner_url'], text_area)

    gl = gitlab.Gitlab(config['gitlab_url'], private_token=config['gitlab_api_token'])
    for runner_info in config['runners']:
        runner_token = register_runner(
            gl,
            runner_info,
            config['registration_token'],
            text_area
        )
        if not runner_token:
            show_message("错误", "无法注册 runner.")
            return
        setup_runner_on_windows(
            runner_token,
            runner_info,
            config['gitlab_url'],
            text_area
        )
        print(f"Succeed Install: {runner_info['description']}\n")
        if gui_objs:
            progress_bar['value'] += 100 / len(config['runners'])
            insert_tk_text(text_area, f"Succeed Install: {runner_info['description']}\n")
            progress_bar.update()
    if gui_objs:
        start_button.config(text="完成", command=root.destroy)
        start_button.config(state=tk.NORMAL)


def main(config_path=None):
    if not is_admin():
        run_as_admin()
    print("Script is running with administrator privileges.")
    if config_path:
        deploy(config_path)
    else:
        create_installation_ui(deploy)
