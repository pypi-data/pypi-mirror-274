import ctypes
import json
import os
import sys
from pathlib import Path
from subprocess import Popen

import gitlab
import requests


def show_message(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x1000 | 0x40)


def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin(argv=None, debug=False):
    if argv is None and sys.argv:
        argv = sys.argv
    if hasattr(sys, '_MEIPASS'):
        arguments = map(str, argv[1:])
    else:
        arguments = map(str, argv)
    cmd = ' '.join(arguments)
    if debug:
        print('Command line:', cmd)
    shell32 = ctypes.windll.shell32
    shell32.ShellExecuteW(None, "runas", sys.executable, cmd, None, 0)
    show_message("安装状态", "安装完成！")


def download_gitlab_runner(runner_url):
    """Download the GitLab runner if it is not already downloaded."""
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
    """Unregister any existing runners with the same description."""
    runners = gl.runners.all()
    for runner in runners:
        if runner.description == description:
            print(f"Unregistering existing runner: {runner.id} - {runner.description}")
            runner.delete()


def register_runner(gl, runner_info, registration_token):
    description = runner_info['description']
    tags = runner_info['tags']
    """Register a new runner on GitLab."""
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
    working_directory = runner_info['work_dir']
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


def deploy(config_path):
    """Main function to control the flow of script."""
    with open(config_path, 'r') as file:
        config = json.load(file)
    GITLAB_URL = config['gitlab_url']
    GITLAB_API_TOKEN = config['gitlab_api_token']
    REGISTRATION_TOKEN = config['registration_token']
    RUNNER_URL = config['runner_url']
    runners = config['runners']

    if not is_admin():
        print("The script is not running with administrator privileges.")
        run_as_admin()
        print("The script has been restarted with administrator privileges")
        sys.exit(0)
    print("Script is running with administrator privileges.")
    download_gitlab_runner(RUNNER_URL)
    gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_API_TOKEN)

    for runner_info in runners:
        runner_token = register_runner(
            gl,
            runner_info,
            REGISTRATION_TOKEN
        )
        if not runner_token:
            raise Exception("Failed to register runner.")
        setup_runner_on_windows(
            runner_token,
            runner_info,
            GITLAB_URL
        )


if __name__ == "__main__":
    deploy('./config.json')
