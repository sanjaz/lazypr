Tool for creating and updating pull requests on GitHub.
------------------------------------------

Integrates with Jira API to fetch corresponding Jira ticket title and sets it
in pull request (mapping is done between branch name and jira ticket key
"proj_xxxx" -> "PROJ-XXXX").

Pull request description template path can be specified in configuration.

Supports setting team reviewers in the pull request.

# Usage

Create config file `~/.config/lazy_pr.ini` and set following values there:

```ini

[default]
jira-api-token = <jira api token>
jira-email = <jira email>
github-token = <your github token>
repo = <repository>
repo-path = <repository local path>
pr-base = master
pr-team = <team on github>
pr-desc = <pull request template file local path>
```

Alternatively, path to .ini config file can be specified as a command line
argument (`-c` or `--config-file-path`).

```python
lazypr -c '/home/sanja/.config/lazy_pr.ini'
```

Command line argument `-cs` or `--config-section` can be used to specify config
section. If not specified, "default" section is used.

Options can be set either in config file, as environment variables or as
command line arguments (run `lazypr --help` for more details):

```python

usage: lazypr [-h] [-c CONFIG_FILE_PATH] [-cs CONFIG_SECTION]
              [-jt JIRA_API_TOKEN] [-je JIRA_EMAIL] [-gt GITHUB_TOKEN]
              [-r REPO] [-rp REPO_PATH] [-b BRANCH] [-s PR_BASE] [-t PR_TITLE]
              [-d PR_DESC] [-tm PR_TEAM]
```

## Examples

- Create pull request for branch `lp_1` in repository `sanjaz/lazypr`.

Both branch and repository can be specified as command line args:
```python
lazypr -r "sanjaz/lazypr" -b "lp_1" `
```
In case repository command line arg is omitted, repository will be fetched from
`repo` value in config file.
```python
python lazypr -b "lp_1"
```
In case branch is not specified, it looks for current branch in local
repository (local repository path is set in `repo-path` in .ini config file):
```python
lazypr
```
Or local repository path can be specified as command line argument (and current
branch in local repository will be used):
```python
lazypr -rp "/home/sanja/moto/lazypr"
```

- Pull request title can be specified using command line argument `-t`
(`--title`):
```python
lazypr -b "lazypr_1" -t "Test title"
```
If not specified, title will be fetched from the corresponding Jira ticket.
Branch name is mapped to Jira ticket key as proj_xxxx -> PROJ_XXXX.

- Pull request description template path can be specified whether in .ini
config file (`pr-desc`), env variable or as a command line argument `-d`
(`--pr-desc`).
```python
lazypr -d "/home/sanja/moto/lazypr/.github/PULL_REQUEST_TEMPLATE.md"
```

- Pull request base branch (target branch where the pull request will be
merged) can be specified as command line argument:
```python
lazypr -s "release"
```
If omitted, default is specified in .ini config file (usually master).

- GiHub team can be assigned to review the pull request with:
```python
lazypr -tm "my-team"
```
If omitted, default is specified in .ini config file.
