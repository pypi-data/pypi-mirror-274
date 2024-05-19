import os
import subprocess
from argparse import ArgumentParser


class CLICommand:
    """命令行提权,默认为cmd
    """

    @staticmethod
    def add_arguments(parser: ArgumentParser):
        add = parser.add_argument
        add("--ps", action='store_true', help="使用powershell")

    @staticmethod
    def run(args, parser):
        current_directory = os.getcwd()
        if args.ps:
            start_ps_admin = f"Start-Process -FilePath 'powershell' -ArgumentList '-NoExit', '-Command cd \"{current_directory}\"' -Verb RunAs"
            subprocess.Popen(['powershell', '-Command', start_ps_admin])
        else:
            start_cmd_admin = f"Start-Process -FilePath 'cmd.exe' -ArgumentList '/K cd {current_directory}' -Verb RunAs"
            subprocess.Popen(['powershell', '-Command', start_cmd_admin])
