import requests
import subprocess
import os

# Function: Check if repository exists
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
        print(f"Failed to check if repository '{name}' exists. Status code: {response.status_code}")
        print(f"Response: {response.text}")
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
        print(f"Repository '{name}' created successfully or already exists!")
        return True
    else:
        print(f"Failed to create repository '{name}'. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

# Function: Clone and push repository if destination exists, otherwise do nothing
def clone_and_push_or_update_repository(source_url, destination_url, pat):
    # Get the repository name from the source URL
    repository_name = source_url.split("/")[-1].split(".")[0]

    # Check if the destination repository exists
    if repository_exists(destination_url, pat):
        print(f"Destination repository '{destination_url}' already exists. Proceeding...")
    else:
        print(f"Destination repository '{destination_url}' does not exist. Skipping...")
        return

    # Check if the repository already exists locally
    if os.path.exists(repository_name):
        print(f"Repository '{repository_name}' already exists locally. Updating...")
        # Change directory to the existing repository
        os.chdir(repository_name)
        # Pull the latest changes from the remote repository
        subprocess.run(["git", "pull"])
    else:
        # Clone the repository at the source URL
        subprocess.run(["git", "clone", source_url])
        # Change directory to the cloned repository
        os.chdir(repository_name)

    # Modify the remote URL to include the personal access token
    destination_url_with_pat = destination_url.format(pat=pat)

    # Set the new remote URL
    subprocess.run(["git", "remote", "set-url", "origin", destination_url_with_pat])

    # Push changes to the destination repository
    subprocess.run(["git", "push", "-f", "origin", "master"])  # Force push

    print(f"This is a mirrored repository, source repository: {source_url}")
    print(f"Repository '{repository_name}' successfully cloned or updated and force-pushed to '{destination_url}'!")
    print(f"Source repository: {source_url}")


# Function: Get GitHub personal access token
def get_github_pat():
    # Attempt to get PAT from environment variable
    pat = os.environ.get("MY_GITHUB_PAT")
    if pat:
        return pat
    else:
        # Use hardcoded value if PAT is not found in environment variables
        return "your_personal_access_token"

# Main function
def main():
    # Get GitHub personal access token
    pat = get_github_pat()

    # Mapping of source repository URLs to their corresponding destination repository URLs
    repository_mappings = {
        "https://github.com/your_username/source_repo": "https://github.com/your_username/destination_repo.git",
        # Add more source and destination repository URLs here
    }

    # Iterate over each mapping and perform clone and push operation
    for source_url, destination_url in repository_mappings.items():
        print(f"Processing source repository: {source_url}")
        clone_and_push_repository(source_url, destination_url, pat)

if __name__ == "__main__":
    main()
