import requests
import subprocess
import os
import logging

# Global constants
GITHUB_USERNAME = "your_username"
DEFAULT_DESTINATION_REPO_URL = "https://github.com/{username}/{name}.git"
DEFAULT_PAT = "your_personal_access_token"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Function: Check if repository exists
def repository_exists(name, pat):
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(f"https://api.github.com/repos/{GITHUB_USERNAME}/{name}", headers=headers)

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        logger.error(f"Failed to check if repository '{name}' exists. Status code: {response.status_code}")
        logger.error(f"Response: {response.text}")
        return True  # Assume it exists to avoid retry

# Function: Create repository
def create_repository(name, description, private, pat):
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "name": name,
        "description": description,
        "private": private
    }

    response = requests.post("https://api.github.com/user/repos", json=data, headers=headers)

    if response.status_code == 201 or response.status_code == 422:  # 422 indicates repository already exists
        logger.info(f"Repository '{name}' created successfully or already exists!")
        return True
    else:
        logger.error(f"Failed to create repository '{name}'. Status code: {response.status_code}")
        logger.error(f"Response: {response.text}")
        return False

# Function: Clone and push repository if destination exists, otherwise do nothing
def clone_and_push_repository(source_url, destination_url, pat):
    repository_name = source_url.split("/")[-1].split(".")[0]

    if repository_exists(repository_name, pat):
        logger.info(f"Destination repository '{destination_url}' already exists. Proceeding...")
    else:
        logger.warning(f"Destination repository '{destination_url}' does not exist. Skipping...")
        return

    if os.path.exists(repository_name):
        logger.info(f"Repository '{repository_name}' already exists locally. Updating...")
        os.chdir(repository_name)
        subprocess.run(["git", "pull"])
    else:
        logger.info(f"Cloning repository '{repository_name}'...")
        subprocess.run(["git", "clone", source_url])
        os.chdir(repository_name)

    destination_url_with_pat = destination_url.format(username=GITHUB_USERNAME, name=repository_name, pat=pat)

    subprocess.run(["git", "remote", "set-url", "origin", destination_url_with_pat])
    subprocess.run(["git", "push", "-f", "origin", "master"])

    logger.info(f"Repository '{repository_name}' successfully cloned or updated and force-pushed to '{destination_url}'!")

# Function: Get GitHub personal access token
def get_github_pat():
    pat = os.environ.get("MY_GITHUB_PAT")
    if pat:
        return pat
    else:
        logger.warning("GitHub personal access token not found in environment variables. Using default token.")
        return DEFAULT_PAT

# Main function
def main():
    pat = get_github_pat()

    repository_mappings = {
        "https://github.com/your_username/source_repo": "https://github.com/your_username/destination_repo.git",
        # Add more source and destination repository URLs here
    }

    for source_url, destination_url in repository_mappings.items():
        logger.info(f"Processing source repository: {source_url}")
        clone_and_push_repository(source_url, destination_url, pat)

if __name__ == "__main__":
    main()
