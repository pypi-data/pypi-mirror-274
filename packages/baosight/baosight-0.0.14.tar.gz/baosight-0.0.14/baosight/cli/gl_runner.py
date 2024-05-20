from argparse import ArgumentParser
from baosight.gitlab_tools.gitlab_runner import main
from baosight.gitlab_tools.gitlab_runner_config_generator import generator

class CLICommand:
    """安装gitlab runner
    安装gitlab runner,配置文件格式如下：
    {
      "gitlab_url": "http://127.0.0.1",
      "gitlab_api_token": "xxxxxxx",
      "registration_token": "xxxxxxx",
      "runner_url": "https://s3.dualstack.us-east-1.amazonaws.com/gitlab-runner-downloads/latest/binaries/gitlab-runner-windows-amd64.exe",
      "runners": [
        {
          "description": "Windows Runner",
          "tags": [
            "windows"
          ],
          "service": "gitlab-runner",
          "work_dir": "C:\\Runners\\Runner3"
        },
      ],
    }
    """

    @staticmethod
    def add_arguments(parser: ArgumentParser):
        add = parser.add_argument
        add("--quite", action='store_true', help="静默安装当前目录下的config.json")
        add("--create-config", dest="config", action='store_true', help="交互式生成配置文件")

    @staticmethod
    def run(args, parser):
        if args.config:
            if generator():
                main("config.json")
            return
        if args.quite:
            main("config.json")
        else:
            main()
