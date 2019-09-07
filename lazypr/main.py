"""Create pull request on Github."""

import sys

from pygit2 import GitError, Repository

from .config import load_config
from .github_api import GitHubApi
from .jira_api import JiraApi
from .utils import read_file, setup_logger


def get_branch(repo_local_path=None):
    """Return current branch in a local repository `repo_local_path`."""
    if repo_local_path is None:
        repo_local_path = "."
    try:
        branch = Repository(repo_local_path).head.shorthand
    except GitError:
        branch = None
    return branch


def main():
    """Create pull request on Github."""
    config = load_config()
    logger = setup_logger()

    # Get git branch from config or look for the locally used one in repo-path.
    # If it doesn't exist, ask user to enter the branch via the command line.
    branch = config.get("branch") or get_branch(config.get("repo-path"))
    if branch is None:
        branch = input("Please insert git branch name:\n").strip()
        if branch == "":
            logger.error("Invalid branch.")
            sys.exit(1)

    # Get pull request title from config or create one from the Jira ticket.
    title = config.get("pr-title")
    if title is None:
        jira_api = JiraApi(
            jira_email=config.get("jira-email"),
            jira_api_key=config.get("jira-api-token"),
            logger=logger)
        title = jira_api.get_pr_title_from_jira_ticket(branch=branch)

    # Read pull request description from file (path is set in config).
    description = read_file(path=config.get("pr-desc"))

    # Create pull request.
    gihub_api = GitHubApi(
        github_token=config.get("github-token"), logger=logger)
    repository = gihub_api.get_repository(repository_name=config.get("repo"))
    gihub_api.create_pull_request(
        repository=repository,
        title=title,
        description=description,
        base=config.get("pr-base", "master"),
        branch=branch,
        team_reviewers=config.get("pr-team"))


if __name__ == "__main__":
    main()
