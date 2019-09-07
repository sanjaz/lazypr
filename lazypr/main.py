import os
import sys

from pygit2 import GitError, Repository

from .config import load_config
from .jira_api import get_pr_title_from_jira_ticket
from .pull_request import PullRequest


def get_branch(repo_local_path=None):
    """Return current branch in a local repository `repo_local_path`."""
    if repo_local_path is None:
        repo_local_path = "."
    try:
        branch = Repository(repo_local_path).head.shorthand
    except GitError:
        branch = None
    return branch


def read_file(path):
    """Read file contents and return it as a string."""
    if path and os.path.exists(path):
        with open(path, "r") as file_handle:
            data = file_handle.read()
    else:
        data = ""
    return data


def main():
    """Create pull request on Github."""
    config = load_config()

    # Get git branch from config or look for the locally used one in repo-path.
    branch = config.get("branch") or get_branch(config.get("repo-path"))
    if branch is None:
        print("Invalid branch.")
        sys.exit(1)

    # Get pull request title from config or create one from the Jira ticket.
    title = config.get("pr-title")
    if title is None:
        title = get_pr_title_from_jira_ticket(
            branch=branch,
            jira_email=config.get("jira-email"),
            jira_api_key=config.get("jira-api-token"))

    # Read pull request description from file (path is set in config).
    description = read_file(path=config.get("pr-desc"))

    # Create pull request.
    pull_request = PullRequest(
        repository_name=config.get("repo"),
        title=title,
        description=description,
        base=config.get("pr-base", "master"),
        branch=branch,
        team_reviewers=config.get("pr-team"))

    pull_request.create(github_token=config.get("github-token"))


if __name__ == "__main__":
    main()
