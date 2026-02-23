"""Config tests for environment separation."""

from pathlib import Path

from app.core import config as config_module


def test_environment_file_resolution_for_test() -> None:
    files = config_module._environment_files("test")
    assert files[-1] == Path(files[0].parent / ".env.test")


def test_environment_file_resolution_for_production() -> None:
    files = config_module._environment_files("production")
    assert files[-1] == Path(files[0].parent / ".env.prod")
