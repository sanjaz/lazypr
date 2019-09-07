import argparse
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os
import sys


CONFIG_FILE_NAME = "lazy_pr.ini"
ENV_PREFIX = "LAZY_PR_"


def get_command_line_options():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-file', help='config file path')
    parser.add_argument('-jt', '--jira-api-token', help='Jira API Token')
    parser.add_argument('-je', '--jira-email', help='Jira Email')
    parser.add_argument('-gt', '--github-token', help='Github Token')
    parser.add_argument('-r', '--repo', help='Git Repository')
    parser.add_argument('-rp', '--repo-path', help='Git Repository Local Path')
    parser.add_argument('-b', '--branch', help='Git Branch')
    parser.add_argument('-s', '--pr-base', help='PR Base')
    parser.add_argument('-t', '--pr-title', help='PR Title')
    parser.add_argument('-d', '--pr-desc', help='PR Description or Path')
    parser.add_argument('-tm', '--pr-team', help='PR Team Reviewers.')

    return parser.parse_args()


def get_config_file_options(config_file, section_name="default"):
    """Read config file and return `section_name` values."""
    config = configparser.SafeConfigParser()
    config.read([config_file])
    return dict(config.items(section_name))


def get_env_options(prefix):
    """Read and return environment variables prefixed with `prefix`.

    Prefix is stripped, names are lower cased and underscores are replaced with
    dashes.
    """
    options = {}
    for name in os.environ:
        if name.startswith(prefix):
            target_name = name[len(prefix):].lower().replace("_", "-")
            options[target_name] = os.environ[name]
    return options


def load_config():
    """Read and return configuration options."""
    cli_options = get_command_line_options()

    # Read configuration from .ini file.
    config_file = cli_options.config_file
    if config_file is None:
        # Read configuration from ~/.config/lazy_pr.ini.
        home = os.path.expanduser("~")
        config_file = os.path.join(home, '.config', CONFIG_FILE_NAME)
    config_options = get_config_file_options(config_file)

    # Override config with environment variables.
    env_options = get_env_options(ENV_PREFIX)
    for option_name in env_options:
        config_options[option_name] = env_options[option_name]

    # Override config with command line arguments.
    for option_key in vars(cli_options):
        option_value = getattr(cli_options, option_key)
        if option_value is not None:
            option_name = option_key.replace("_", "-")
            config_options[option_name] = option_value

    return config_options
