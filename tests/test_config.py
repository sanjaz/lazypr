import os

import pytest

from lazypr.config import CONFIG_FILE_NAME, get_default_config_file_path


class TestConfig:
    """Test loading configuration."""

    def test_get_default_config_file_path(self):
        """Test getting default config file path."""
        real_home = os.environ.get("HOME")

        os.environ["HOME"] = "/some/test/value"
        expected_path = "/some/test/value/.config/lazy_pr.ini"
        assert get_default_config_file_path() == expected_path

        if real_home is not None:
            os.environ["HOME"] = real_home

    def test_get_default_config_file_path_xdg(self):
        """Test getting config file path when `XDG_CONFIG_HOME` is set."""
        real_config_home = os.environ.get("XDG_CONFIG_HOME")

        os.environ["XDG_CONFIG_HOME"] = "/some/test/value"
        expected_path = "/some/test/value/lazy_pr.ini"
        assert get_default_config_file_path() == expected_path

        if real_config_home is not None:
            os.environ["XDG_CONFIG_HOME"] = real_config_home
