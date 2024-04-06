import os
import requests
import subprocess
from urllib.parse import urlparse

# GitHub个人访问令牌
my_github_pat = os.getenv('MY_GITHUB_PAT') or 'your_github_pat_here'

# 目标仓库的用户名
my_github_username = os.getenv('MY_GITHUB_USERNAME') or 'your_github_username_here'

# 定义源仓库信息的列表
source_repositories = [
    # {'url': 'https://github.com/example_user/example_repo_1.git'},  # 示例1
    # {'url': 'https://github.com/example_user/example_repo_2.git'},  # 示例2
]

def create_github_repo(repo_name):
    headers = {
        'Authorization': f'token {my_github_pat}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'name': repo_name,
        'private': False,  # 是否创建私有仓库
        # 其他参数可根据需求添加
    }
    response = requests.post(f'https://api.github.com/user/repos', headers=headers, json=data)
    if response.status_code == 201:
        print(f"Created repository: {repo_name}")
    else:
        print(f"Failed to create repository: {repo_name}")
        print(response.text)

def clone_or_update_repository(source_url, target_dir):
    if os.path.exists(target_dir):
        subprocess.run(['git', '-C', target_dir, 'fetch', '--prune'])
        subprocess.run(['git', '-C', target_dir, 'pull', '--ff-only'])
    else:
        subprocess.run(['git', 'clone', source_url, target_dir])

def mirror_push_to_github(source_url, target_url, target_repo_name):
    # 克隆源仓库到本地或更新本地仓库
    clone_or_update_repository(source_url, target_repo_name)

    # 切换到目标仓库的目录
    os.chdir(target_repo_name)

    # 添加目标仓库作为远程仓库（包含个人访问令牌）
    target_url_with_token = f'https://{my_github_pat}@{target_url[8:]}'
    # subprocess.run(['git', 'remote', 'add', 'target', target_url_with_token])

    # 强制推送到目标仓库
    subprocess.run(['git', 'push', '--mirror', target_url_with_token])

# 处理每个源仓库
for repo_info in source_repositories:
    source_repo_url = repo_info['url']
    parsed_url = urlparse(source_repo_url)
    source_username = parsed_url.path.split('/')[1]
    source_repo_name = parsed_url.path.split('/')[-1].split('.git')[0]
    target_repo_name = f"{source_username}_{source_repo_name}"
    target_repo_url = f'https://github.com/{my_github_username}/{target_repo_name}.git'

    # 检查目标仓库是否存在
    response = requests.get(target_repo_url)
    if response.status_code == 404:
        # 如果目标仓库不存在，则创建
        create_github_repo(target_repo_name)

    # 使用mirror方式推送到目标仓库
    mirror_push_to_github(source_repo_url, target_repo_url, target_repo_name)
