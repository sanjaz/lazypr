Tool for creating pull requests on Github.
------------------------------------------

# Usage

Create `lazy_pr.ini` file in  `~/.config` and provide following values there:

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

Or use command line argument to specify path to .ini config file (`-c`).
