from github import Github, GithubException


class PullRequest():
    """PullRequest"""

    def __init__(self, repository_name, title, description, base, branch,
                 team_reviewers=None):
        self.repository_name = repository_name
        self.title = title
        self.description = description
        self.base = base
        self.branch = branch
        self.team_reviewers = team_reviewers

    def get_github_repository(self, github_token):
        """Fetch and return Github `Repository`."""
        try:
            gh = Github(github_token)
            gh_repository = gh.get_repo(self.repository_name)
        except GithubException:
            gh_repository = None
        return gh_repository

    def create(self, github_token):
        """Create Github `PullRequest` and set team reviewers.

        In case pull request already exists, update title and description.
        """
        gh_repository = self.get_github_repository(github_token)
        if gh_repository is None:
            return

        try:
            gh_pull_request = gh_repository.create_pull(
                title=self.title, body=self.description, base=self.base,
                head=self.branch)
            self.set_team_reviewers(gh_pull_request)
            html_url = gh_pull_request.html_url
            print("Pull request created at {}".format(html_url))
        except GithubException:
            gh_pull_request = self.update(github_token, gh_repository)
            if gh_pull_request:
                html_url = gh_pull_request.html_url
                print("Pull request updated at {}".format(html_url))
        return gh_pull_request

    def update(self, github_token, gh_repository):
        """Update Github `PullRequest` - set title and description.

        Find pull request by repository and branch.
        """
        assert(gh_repository is not None)

        gh_pull_requests = gh_repository.get_pulls(
            head="{repo}:{branch}".format(
                repo=self.repository_name, branch=self.branch),
            state="open")
        try:
            gh_pull_request = gh_pull_requests[0]
            gh_pull_request.edit(body=self.description, title=self.title)
        except IndexError:
            gh_pull_request = None
        return gh_pull_request

    def set_team_reviewers(self, github_pull_request):
        """Set team reviewers for the given pull request."""
        if self.team_reviewers:
            github_pull_request.create_review_request(
                team_reviewers=[self.team_reviewers])
