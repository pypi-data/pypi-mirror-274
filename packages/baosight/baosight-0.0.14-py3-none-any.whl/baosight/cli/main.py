import argparse
import importlib
import textwrap

subcommands = [
    ("gl-runner", "baosight.cli.gl_runner"),
    ("cmd", "baosight.cli.cmd_admin"),
]


def main():
    parser = argparse.ArgumentParser(prog="baosight", description="常用工具包")
    subparsers = parser.add_subparsers(title="subcommand", dest="subcommand")
    subparser_help = subparsers.add_parser("help", description="Help", help="子命令帮助")
    subparser_help.add_argument("helpcommand", nargs="?", metavar="subcommand", help="为子命令提供帮助")
    parsers = {}
    functions = {}
    for subcommand, module_name in subcommands:
        CLICommand = importlib.import_module(module_name).CLICommand
        docstring = CLICommand.__doc__
        short, long = docstring.split("\n", 1)
        long = textwrap.dedent(long)
        subparser = subparsers.add_parser(subcommand, description=long, help=short)
        CLICommand.add_arguments(subparser)
        parsers[subcommand] = subparser
        functions[subcommand] = CLICommand.run
    args = parser.parse_args()  # 默认会从命令行读取参数
    if args.subcommand == "help":
        if args.helpcommand is None:
            parser.print_help()
        else:
            parsers[args.subcommand].print_help()
    elif args.subcommand is None:
        parser.print_usage()
    else:
        f = functions[args.subcommand]
        f(args, parsers[args.subcommand])


if __name__ == '__main__':
    main()
