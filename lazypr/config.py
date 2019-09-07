"""Load configuration."""

import argparse
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os


CONFIG_FILE_NAME = "lazy_pr.ini"
DEFAULT_CONFIG_SECTION = "default"
ENV_PREFIX = "LAZY_PR_"


def get_default_config_file_path():
    """Return default configuration file path.

    $XDG_CONFIG_HOME defines the base directory relative to which user specific
    configuration files should be stored. If $XDG_CONFIG_HOME is either not set
    or empty, ~/.config should be used.
    """
    config_home = os.environ.get("XDG_CONFIG_HOME")
    if not config_home:
        home = os.path.expanduser("~")
        config_home = os.path.join(home, ".config")
    config_file_path = os.path.join(config_home, CONFIG_FILE_NAME)
    return config_file_path


def get_command_line_options():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-file-path', help='Config file path')
    parser.add_argument('-cs', '--config-section', help='Config section')
    parser.add_argument('-jt', '--jira-api-token', help='Jira API token')
    parser.add_argument('-je', '--jira-email', help='Jira user email')
    parser.add_argument('-gt', '--github-token', help='GitHub token')
    parser.add_argument('-r', '--repo', help='Git repository')
    parser.add_argument('-rp', '--repo-path', help='Git repository local path')
    parser.add_argument('-b', '--branch', help='Git branch')
    parser.add_argument('-s', '--pr-base', help='Pull request base branch')
    parser.add_argument('-t', '--pr-title', help='Pull request title')
    parser.add_argument(
        '-d', '--pr-desc', help='Pull request description template path')
    parser.add_argument('-tm', '--pr-team', help='Pull request team reviewers')

    return parser.parse_args()


def get_config_file_options(config_file_path, section_name):
    """Read config file and return `section_name` values."""
    config = configparser.SafeConfigParser()
    config.read([config_file_path])
    if not section_name:
        section_name = DEFAULT_CONFIG_SECTION
    if section_name in config.sections():
        config_data = dict(config.items(section_name))
    else:
        config_data = {}
    return config_data


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
    config_file_path = cli_options.config_file_path
    if config_file_path is None:
        config_file_path = get_default_config_file_path()
    config_section = cli_options.config_section or DEFAULT_CONFIG_SECTION
    config_options = get_config_file_options(config_file_path, config_section)

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
