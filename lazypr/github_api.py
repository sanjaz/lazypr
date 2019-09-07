"""Module to access Github API."""

import logging

from github import Github, GithubException, Repository


class GitHubApi:
    """GitHub API access."""

    def __init__(self, github_token, logger=None):
        self.github_token = github_token
        if logger is None:
            self.logger = logging.getLogger()
        else:
            self.logger = logger

    def get_repository(self, repository_name):
        """Fetch and return Github `Repository`."""
        try:
            repository = Github(self.github_token).get_repo(repository_name)
        except GithubException:
            repository = None
        return repository

    def create_pull_request(self, repository, title, description, base, branch,
                            team_reviewers):
        """Create Github `PullRequest` and set team reviewers.

        In case pull request already exists, update title and description.
        """
        assert isinstance(repository, Repository.Repository)

        try:
            pull_request = repository.create_pull(
                title=title, body=description, base=base, head=branch)
            self.set_team_reviewers(pull_request, team_reviewers)
            msg = "Pull request created at {url}".format(
                url=pull_request.html_url)
            self.logger.debug(msg)
        except GithubException:
            pull_request = self.update_pull_request(
                repository=repository, branch=branch, title=title,
                description=description)
            if pull_request:
                msg = "Pull request updated at {url}".format(
                    url=pull_request.html_url)
                self.logger.debug(msg)
        return pull_request

    def update_pull_request(self, repository, branch, title, description):
        """Update Github `PullRequest` - set title and description.

        Find pull request by repository and branch.
        """
        assert isinstance(repository, Repository.Repository)

        pull_requests = repository.get_pulls(
            head="{repo}:{branch}".format(
                repo=repository.full_name, branch=branch),
            state="open")
        try:
            pull_request = pull_requests[0]
            pull_request.edit(body=description, title=title)
        except (IndexError, GithubException) as ex:
            self.logger.error(ex)
            pull_request = None
        return pull_request

    @classmethod
    def set_team_reviewers(cls, pull_request, team_reviewers):
        """Set team reviewers for the given pull request."""
        if not team_reviewers:
            return
        pull_request.create_review_request(team_reviewers=[team_reviewers])
