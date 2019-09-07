import json
import requests

JIRA_BASE_ISSUE_URL = "https://motocommerce.atlassian.net/rest/api/2/issue"


def get_jira_ticket_key_from_branch(branch):
    """Construct a Jira ticket key based on the git branch name.

    For now it only replaces underscores with dashes and makes it uppercase.
    Eg. "proj_xxxx" -> "PROJ-XXXX"
    """
    if branch:
        jira_ticket_key = branch.upper().replace('_', '-')
    else:
        jira_ticket_key = None
    return jira_ticket_key


def get_pr_title_from_jira_ticket(branch, jira_email, jira_api_key):
    """Create a pull request title.

    Returns "jira ticket key: summary" as the title. Summary is pulled from the
    Jira ticket (summary field) and Jira ticket is chosen based on the branch.
    """
    jira_ticket_key = get_jira_ticket_key_from_branch(branch)
    if jira_ticket_key is None:
        return ""
    url = "{jira_issue_base_url}/{jira_ticket_key}?fields=summary".format(
        jira_issue_base_url=JIRA_BASE_ISSUE_URL,
        jira_ticket_key=jira_ticket_key)
    response = requests.get(
        url, auth=requests.auth.HTTPBasicAuth(jira_email, jira_api_key),
        headers= {"Content-Type" : "application/json"})
    if response.ok:
        response_data = json.loads(response.text)
        summary = response_data.get("fields", {}).get("summary", "")
        title = "{jira_ticket_key}: {summary}".format(
            jira_ticket_key=jira_ticket_key, summary=summary)
    else:
        title = jira_ticket_key
    return title
