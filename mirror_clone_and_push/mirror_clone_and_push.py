import git
import os

def mirror_clone_and_push(source_url, destination_url, pat):
    # Clone the source repository
    repo_path = os.path.basename(source_url).split('.')[0]
    git.Repo.clone_from(source_url, repo_path, mirror=True)

    # Open the cloned repository
    repo = git.Repo(repo_path)

    # Set up SSH key for pushing
    env = {
        "GIT_SSH_COMMAND": f'git -c http.extraheader="AUTHORIZATION: token {pat}"',
    }

    # Create the remote if it doesn't exist
    try:
        remote = repo.create_remote('destination', destination_url)
    except git.exc.GitCommandError:
        # Remote already exists
        remote = repo.remote('destination')

    # Push to the destination repository
    try:
        remote.push(env=env)
        print(f"Pushed mirror clone from {source_url} to {destination_url}")
    except git.exc.GitCommandError as e:
        print(f"Error pushing to {destination_url}: {e}")

# List of source and destination repositories
repositories = [
    {'source': 'https://github.com/example/source1.git', 'destination': 'https://github.com/example/destination1.git', 'pat': 'your_personal_access_token'},
    {'source': 'https://github.com/example/source2.git', 'destination': 'https://github.com/example/destination2.git', 'pat': 'your_personal_access_token'},
    # Add more repositories as needed
]

# Sync each repository
for repo_pair in repositories:
    source_url = repo_pair['source']
    destination_url = repo_pair['destination']
    pat = repo_pair['pat']
    mirror_clone_and_push(source_url, destination_url, pat)
