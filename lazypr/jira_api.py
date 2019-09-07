"""Module to access Jira API."""

import json
import logging
import requests


class JiraApi:
    """Jira API access."""

    JIRA_BASE_ISSUE_URL = "https://motocommerce.atlassian.net/rest/api/2/issue"

    def __init__(self, jira_email, jira_api_key, logger=None):
        self.jira_email = jira_email
        self.jira_api_key = jira_api_key
        if logger is None:
            self.logger = logging.getLogger()
        else:
            self.logger = logger

    @classmethod
    def get_jira_ticket_key_from_branch(cls, branch):
        """Construct a Jira ticket key based on the git branch name.

        For now it only replaces underscores with dashes and makes it uppercase.
        Eg. "proj_xxxx" -> "PROJ-XXXX"
        """
        if branch:
            jira_ticket_key = branch.upper().replace('_', '-')
        else:
            jira_ticket_key = None
        return jira_ticket_key

    def get_jira_ticket_summary_url(self, jira_ticket_key):
        """Return Jira API endpoint to fetch ticket summary."""
        return "{jira_issue_base_url}/{jira_ticket_key}?fields=summary".format(
            jira_issue_base_url=self.JIRA_BASE_ISSUE_URL,
            jira_ticket_key=jira_ticket_key)

    def get_pr_title_from_jira_ticket(self, branch):
        """Create a pull request title.

        Returns "jira ticket key: summary" as the title. Summary is pulled from
        the Jira ticket (summary field) and Jira ticket is chosen based on the
        branch.
        """
        jira_ticket_key = self.get_jira_ticket_key_from_branch(branch)
        if jira_ticket_key is None:
            error_msg = "Invalid branch name {branch}.".format(branch=branch)
            self.logger.error(error_msg)
            return ""

        url = self.get_jira_ticket_summary_url(jira_ticket_key)
        auth = requests.auth.HTTPBasicAuth(self.jira_email, self.jira_api_key)
        headers = {"Content-Type" : "application/json"}
        try:
            response = requests.get(url=url, auth=auth, headers=headers)
            if response.ok:
                response_data = json.loads(response.text)
                summary = response_data.get("fields", {}).get("summary", "")
                title = "{jira_ticket_key}: {summary}".format(
                    jira_ticket_key=jira_ticket_key, summary=summary)
            else:
                title = jira_ticket_key
        except requests.exceptions.RequestException as ex:
            self.logger.error(ex)
            title = jira_ticket_key
        return title
