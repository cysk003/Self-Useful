import requests
import subprocess
import os

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

    if response.status_code == 201:
        print(f"Repository '{name}' created successfully!")
        return True
    else:
        print(f"Failed to create repository '{name}'. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

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

def main():
    # Your GitHub Personal Access Token
    pat = "your_personal_access_token"

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
        if repository_exists(destination_repo_name, pat):
            print(f"Destination repository '{destination_repo_name}' already exists. Skipping creation.")
        else:
            if create_repository(destination_repo_name, f"This is a mirror repository, source repository: {source_url}", False, pat):
                print(f"Destination repository '{destination_repo_name}' created successfully!")
            else:
                tasks_failed.append(destination_repo_name)
                continue

        try:
            clone_and_push_repository(source_url, destination_url, pat)
            tasks_completed.append(destination_repo_name)
        except Exception as e:
            tasks_failed.append(destination_repo_name)
            print(f"An error occurred while processing repository '{destination_repo_name}': {str(e)}")

    print("\nAll tasks completed!")
    print("Completed tasks:")
    for task in tasks_completed:
        print(f"- {task}")
    print("\nFailed tasks:")
    for task in tasks_failed:
        print(f"- {task}")

if __name__ == "__main__":
    main()
