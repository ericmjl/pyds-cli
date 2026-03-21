"""Tests for `pyds project` commands."""

from __future__ import annotations

from unittest.mock import patch

from typer.testing import CliRunner

from pyds.cli import project as project_module


def test_project_init_uses_default_cookiecutter_template() -> None:
    """`project init` calls cookiecutter with the cookiecutter-python-project URL."""
    with patch.object(project_module, "cookiecutter") as mock_cookiecutter:
        runner = CliRunner(mix_stderr=True)
        # Single-command Typer app: invoke with options only, not `init`.
        result = runner.invoke(project_module.app, [])
        assert result.exit_code == 0, result.output
        mock_cookiecutter.assert_called_once()
        url = mock_cookiecutter.call_args[0][0]
        assert "cookiecutter-python-project" in url
        assert mock_cookiecutter.call_args[1].get("accept_hooks") is True


def test_project_init_respects_template_flag() -> None:
    """`--template` overrides the default template."""
    with patch.object(project_module, "cookiecutter") as mock_cookiecutter:
        runner = CliRunner(mix_stderr=True)
        result = runner.invoke(
            project_module.app,
            ["--template", "https://example.com/tpl.git"],
        )
        assert result.exit_code == 0
        mock_cookiecutter.assert_called_once_with(
            "https://example.com/tpl.git",
            accept_hooks=True,
        )


def test_project_init_skip_hooks() -> None:
    """`--skip-hooks` passes accept_hooks=False to cookiecutter."""
    with patch.object(project_module, "cookiecutter") as mock_cookiecutter:
        runner = CliRunner(mix_stderr=True)
        result = runner.invoke(project_module.app, ["--skip-hooks"])
        assert result.exit_code == 0
        mock_cookiecutter.assert_called_once()
        assert mock_cookiecutter.call_args[1]["accept_hooks"] is False
