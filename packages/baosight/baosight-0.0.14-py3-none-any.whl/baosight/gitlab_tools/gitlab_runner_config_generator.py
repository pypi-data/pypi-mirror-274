import json


def input_runner_info():
    """ 交互式输入单个runner的配置信息 """
    description = input("请输入runner的描述: ")
    tags = input("请输入runner的标签（使用逗号分隔）: ").split(',')
    service = input("请输入runner的服务名: ")
    work_dir = input("请输入runner的工作目录路径: ")
    install_options = input("请输入安装选项（--option1 value1,--option2 value2...）: ").split(',')
    start_options = input("请输入启动选项（--option1 value1,--option2 value2...）: ").split(',')
    register_options = input("请输入注册选项（--option1 value1,--option2 value2...）: ").split(',')

    return {
        'description': description.strip(),
        'tags': [tag.strip() for tag in tags],
        'service': service.strip(),
        'work_dir': work_dir.strip(),
        'install_options': [option.strip() for option in install_options],
        'start_options': [option.strip() for option in start_options],
        'register_options': [option.strip() for option in register_options]
    }


def generator():
    """ 主函数，生成JSON配置文件 """
    gitlab_url = input("请输入GitLab URL: ")
    gitlab_api_token = input("请输入GitLab API token: ")
    registration_token = input("请输入注册token: ")
    runner_url = input("请输入GitLab Runner的下载URL: ")

    runners = []
    more_runners = True
    while more_runners:
        runners.append(input_runner_info())
        more_runners = input("是否添加更多的runner? (y/n): ").lower() == 'y'

    config = {
        'gitlab_url': gitlab_url,
        'gitlab_api_token': gitlab_api_token,
        'registration_token': registration_token,
        'runner_url': runner_url,
        'runners': runners
    }

    file_path = input("请输入配置文件保存的路径及名称（例如 C:/path/to/config.json）: ") or "./config.json"
    with open(file_path, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"配置文件已保存到 {file_path}")
    return input("是否立即执行？（y/n）").lower() == "y"

