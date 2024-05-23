
import os
from git import Repo
from github import Github

def generate_release_notes(repo_path, from_tag, to_tag, github_repo_name, github_token, release_notes_file):
    """
    Generates release notes by extracting commit messages between two tags and fetching closed issues from GitHub.

    Parameters:
    - repo_path (str): Local path to the Git repository.
    - from_tag (str): Tag to start collecting commits.
    - to_tag (str): Tag to end collecting commits.
    - github_repo_name (str): Full GitHub repository name (e.g., 'username/repository').
    - github_token (str): GitHub access token for authentication.
    - release_notes_file (str): File path to save the release notes.
    """
    # Extract commits
    repo = Repo(repo_path)
    commits = list(repo.iter_commits(f'{from_tag}...{to_tag}'))
    commit_messages = [commit.message.strip() for commit in commits]

    # Fetch issues from GitHub
    g = Github(github_token)
    repo = g.get_repo(github_repo_name)
    issues = repo.get_issues(state='closed')
    issue_details = [(issue.number, issue.title) for issue in issues if issue.pull_request is None]

    # Write to release notes file
    with open(release_notes_file, 'w') as file:
        file.write('Release Notes:\n\n')
        file.write('Features and Enhancements:\n')
        for message in commit_messages:
            file.write(f'- {message}\n')
        file.write('\nFixed Issues:\n')
        for issue in issue_details:
            file.write(f'- Issue #{issue[0]}: {issue[1]}\n')

    print(f"Release notes saved to {release_notes_file}")

# Example usage
repo_path = '/path/to/your/repo'
from_tag = 'v1.0.0'
to_tag = 'v1.1.0'
github_repo_name = 'username/repo'
github_token = 'your_github_token'
release_notes_file = 'release_notes.md'

generate_release_notes(repo_path, from_tag, to_tag, github_repo_name, github_token, release_notes_file)

