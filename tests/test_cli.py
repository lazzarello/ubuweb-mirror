"""Tests for the Click-based CLI."""

import pytest
from click.testing import CliRunner
from ubu.cli import cli
from ubu import __version__


@pytest.fixture
def runner():
    """Fixture for Click test runner."""
    return CliRunner()


def test_cli_help(runner):
    """Test that the CLI shows help."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "UbuWeb Mirror" in result.output
    assert "download" in result.output
    assert "analyze" in result.output
    assert "report" in result.output
    assert "random" in result.output


def test_cli_version(runner):
    """Test that --version shows the version."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_download_help(runner):
    """Test download command help."""
    result = runner.invoke(cli, ["download", "--help"])
    assert result.exit_code == 0
    assert "Download content" in result.output
    assert "--no-skip" in result.output
    assert "--download-path" in result.output


def test_analyze_help(runner):
    """Test analyze command help."""
    result = runner.invoke(cli, ["analyze", "--help"])
    assert result.exit_code == 0
    assert "Analyze the downloaded archive" in result.output
    assert "--download-path" in result.output
    assert "--html-path" in result.output


def test_report_help(runner):
    """Test report command help."""
    result = runner.invoke(cli, ["report", "--help"])
    assert result.exit_code == 0
    assert "Generate a report" in result.output
    assert "--format" in result.output
    assert "--output" in result.output


def test_random_help(runner):
    """Test random command help."""
    result = runner.invoke(cli, ["random", "--help"])
    assert result.exit_code == 0
    assert "Download a random work" in result.output
    assert "ARTIST_NAME" in result.output


def test_analyze_with_temp_dir(runner, tmp_path):
    """Test analyze command with temporary directory."""
    # Create test directories
    av_dir = tmp_path / "av"
    html_dir = tmp_path / "html"
    av_dir.mkdir()
    html_dir.mkdir()

    # Create some test files
    (av_dir / "test1.mp4").write_text("test video content")
    (av_dir / "test2.mp4").write_text("test video content 2")
    (html_dir / "test.html").write_text("<html></html>")

    result = runner.invoke(
        cli, ["analyze", "--download-path", str(av_dir), "--html-path", str(html_dir)]
    )

    assert result.exit_code == 0
    assert "ARCHIVE ANALYSIS" in result.output
    assert "A/V Files: 2" in result.output
    assert "HTML Files: 1" in result.output


def test_report_text_format(runner, mocker):
    """Test report command with text format."""
    # Mock the Page class to avoid network calls
    mock_page = mocker.MagicMock()
    mock_artist = mocker.MagicMock()
    mock_artist.name = "Test Artist"
    mock_artist.url = "http://test.com"
    mock_page.get_artists.return_value = [mock_artist]
    mock_page.get_artist_works.return_value = []

    mocker.patch("ubu.cli.Page", return_value=mock_page)

    result = runner.invoke(cli, ["report", "--format", "text"])

    assert result.exit_code == 0
    assert "UBUWEB ARCHIVE REPORT" in result.output
    assert "Test Artist" in result.output


def test_report_json_format(runner, mocker, tmp_path):
    """Test report command with JSON format."""
    # Mock the Page class
    mock_page = mocker.MagicMock()
    mock_artist = mocker.MagicMock()
    mock_artist.name = "Test Artist"
    mock_artist.url = "http://test.com"
    mock_page.get_artists.return_value = [mock_artist]
    mock_page.get_artist_works.return_value = []

    mocker.patch("ubu.cli.Page", return_value=mock_page)

    output_file = tmp_path / "report.json"
    result = runner.invoke(
        cli, ["report", "--format", "json", "--output", str(output_file)]
    )

    assert result.exit_code == 0
    assert output_file.exists()

    import json

    data = json.loads(output_file.read_text())
    assert data["total_artists"] == 1
    assert data["artists"][0]["name"] == "Test Artist"


def test_report_csv_format(runner, mocker, tmp_path):
    """Test report command with CSV format."""
    # Mock the Page class
    mock_page = mocker.MagicMock()
    mock_artist = mocker.MagicMock()
    mock_artist.name = "Test Artist"
    mock_artist.url = "http://test.com"

    mock_work = mocker.MagicMock()
    mock_work.name = "Test Work"
    mock_work.url = "http://test.com/work"

    mock_page.get_artists.return_value = [mock_artist]
    mock_page.get_artist_works.return_value = [mock_work]

    mocker.patch("ubu.cli.Page", return_value=mock_page)

    output_file = tmp_path / "report.csv"
    result = runner.invoke(
        cli, ["report", "--format", "csv", "--output", str(output_file)]
    )

    assert result.exit_code == 0
    assert output_file.exists()

    content = output_file.read_text()
    assert "Artist Name,Artist URL,Work Name,Work URL" in content
    assert "Test Artist" in content
    assert "Test Work" in content


def test_verbosity_levels(runner):
    """Test different verbosity levels."""
    # Test -v
    result = runner.invoke(cli, ["-v", "--help"])
    assert result.exit_code == 0

    # Test -vv
    result = runner.invoke(cli, ["-vv", "--help"])
    assert result.exit_code == 0

    # Test -vvv
    result = runner.invoke(cli, ["-vvv", "--help"])
    assert result.exit_code == 0
