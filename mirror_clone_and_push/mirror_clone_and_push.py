import requests
import subprocess
import os

# Function to check if a repository exists
def repository_exists(name, pat):
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(f"https://api.github.com/repos/your_username/{name}", headers=headers)

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        print(f"Failed to check repository existence. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return True  # Assuming it exists to avoid retrying

# Function to create a repository
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

    if response.status_code == 201 or response.status_code == 422:  # 422 for repository already exists
        print(f"Repository '{name}' created successfully or already exists!")
        return True
    else:
        print(f"Failed to create repository '{name}'. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

# Function to clone and push a repository
def clone_and_push_repository(source_url, destination_url, pat):
    # Clone the repository from source URL
    subprocess.run(["git", "clone", source_url])

    # Get the repository name from the source URL
    repository_name = source_url.split("/")[-1].split(".")[0]

    # Change directory to the cloned repository
    os.chdir(repository_name)

    # Modify the remote URL to include the personal access token
    destination_url_with_pat = destination_url.format(pat=pat)

    # Set the new remote URL
    subprocess.run(["git", "remote", "set-url", "origin", destination_url_with_pat])

    # Push changes to the destination repository
    subprocess.run(["git", "push", "-f", "origin", "master"])  # Force push

    print(f"This is a mirror repository, source repository: {source_url}")
    print(f"Repository '{repository_name}' cloned and forcefully pushed successfully to '{destination_url}'!")
    print(f"Source repository: {source_url}")

# Function to get GitHub Personal Access Token
def get_github_pat():
    # Try to get PAT from environment variable
    pat = os.environ.get("MY_GITHUB_PAT")
    if pat:
        return pat
    else:
        # If PAT not found in environment variable, use hardcoded value
        return "your_personal_access_token"

# Main function
def main():
    # Get GitHub Personal Access Token
    pat = get_github_pat()

    # Source repository URLs and their corresponding destination repository URLs
    repository_mappings = {
        "https://github.com/your_username/source_repo1.git": "https://{pat}@github.com/your_username/destination_repo1.git",
        "https://github.com/your_username/source_repo2.git": "https://{pat}@github.com/your_username/destination_repo2.git",
        # Add more mappings as needed
    }

    tasks_completed = []
    tasks_failed = []

    # Clone and push each source repository to its corresponding destination repository
    for source_url, destination_url in repository_mappings.items():
        destination_repo_name = destination_url.split("/")[-1].split(".")[0]
        if not create_repository(destination_repo_name, f"This is a mirror repository of {source_url}.", False, pat):
            tasks_failed.append(source_url)
            continue
        clone_and_push_repository(source_url, destination_url, pat)
        tasks_completed.append(source_url)

    print("\nTasks completed:")
    for task in tasks_completed:
        print(task)

    print("\nTasks failed:")
    for task in tasks_failed:
        print(task)

if __name__ == "__main__":
    main()
