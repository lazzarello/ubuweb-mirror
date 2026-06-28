"""
Command-line interface for UbuWeb Mirror using Click.

Provides commands for downloading, analyzing, and reporting on the UbuWeb archive.
"""

import click
import logging
from . import (
    __version__,
    full_download_run,
    download_random_work_from,
    DOWNLOAD_PATH,
    HTML_PATH,
    FILM_URL,
    Page,
)
from .file_index import build_file_index


@click.group()
@click.version_option(version=__version__, prog_name="ubu")
@click.option(
    "-v", "--verbose", count=True, help="Increase verbosity (use -v, -vv, or -vvv)"
)
@click.pass_context
def cli(ctx, verbose):
    """
    UbuWeb Mirror - Archive and analyze content from UbuWeb.

    A tool for downloading and managing the UbuWeb film archive.
    """
    # Ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)

    # Set logging level based on verbosity
    if verbose == 0:
        level = logging.WARNING
    elif verbose == 1:
        level = logging.INFO
    else:  # verbose >= 2
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("transfers.log", mode="a"),
        ],
        force=True,
    )

    ctx.obj["verbose"] = verbose


@cli.command()
@click.option(
    "--no-skip",
    is_flag=True,
    help="Re-check all files instead of skipping existing downloads",
)
@click.option(
    "--download-path",
    type=click.Path(),
    default=None,
    help=f"Override download path (default: {DOWNLOAD_PATH})",
)
@click.pass_context
def download(ctx, no_skip, download_path):
    """
    Download content from the UbuWeb archive.

    By default, skips files that already exist in the download directory.
    Use --no-skip to force re-checking all files.

    Examples:

        ubu download                  # Download new files only

        ubu download --no-skip        # Re-check all files

        ubu download --download-path ~/custom/path
    """
    skip_existing = not no_skip

    if skip_existing:
        click.echo("Running with skip-existing ENABLED (will skip downloaded files)")
    else:
        click.echo("Running with skip-existing DISABLED (will re-check all files)")

    click.echo(f"Download path: {download_path or DOWNLOAD_PATH}")
    click.echo()

    # Run the full download
    try:
        full_download_run(skip_existing=skip_existing, download_path=download_path)
        click.secho("✓ Download complete!", fg="green")
    except Exception as e:
        click.secho(f"✗ Error during download: {e}", fg="red", err=True)
        if ctx.obj.get("verbose", 0) > 0:
            logging.exception("Full traceback:")
        raise


@cli.command()
@click.option(
    "--download-path",
    type=click.Path(exists=True),
    default=None,
    help=f"Path to analyze (default: {DOWNLOAD_PATH})",
)
@click.option(
    "--html-path",
    type=click.Path(exists=True),
    default=None,
    help=f"HTML path to analyze (default: {HTML_PATH})",
)
@click.pass_context
def analyze(ctx, download_path, html_path):
    """
    Analyze the downloaded archive.

    Scans the download directories and provides statistics about
    the archived content including file counts and total size.

    Examples:

        ubu analyze

        ubu analyze --download-path ~/custom/path
    """
    av_path = download_path or DOWNLOAD_PATH
    html_path_to_use = html_path or HTML_PATH

    click.echo("Analyzing archive...")
    click.echo()

    # Build indices
    try:
        av_index = build_file_index(av_path)
        html_index = build_file_index(html_path_to_use)

        av_size_gb = av_index.total_size / (1024**3)
        html_size_gb = html_index.total_size / (1024**3)
        total_size_gb = av_size_gb + html_size_gb

        click.echo("=" * 60)
        click.echo("ARCHIVE ANALYSIS")
        click.echo("=" * 60)
        click.echo(f"A/V Files: {len(av_index):,} files ({av_size_gb:.2f} GB)")
        click.echo(f"  Location: {av_path}")
        click.echo()
        click.echo(f"HTML Files: {len(html_index):,} files ({html_size_gb:.2f} GB)")
        click.echo(f"  Location: {html_path_to_use}")
        click.echo()
        click.echo(
            f"Total: {len(av_index) + len(html_index):,} files ({total_size_gb:.2f} GB)"
        )
        click.echo("=" * 60)

    except Exception as e:
        click.secho(f"✗ Error during analysis: {e}", fg="red", err=True)
        if ctx.obj.get("verbose", 0) > 0:
            logging.exception("Full traceback:")
        raise


@cli.command()
@click.option(
    "--format",
    type=click.Choice(["text", "json", "csv"], case_sensitive=False),
    default="text",
    help="Output format for the report",
)
@click.option(
    "--output",
    type=click.Path(),
    default=None,
    help="Write report to file instead of stdout",
)
@click.pass_context
def report(ctx, format, output):
    """
    Generate a report of the archive contents.

    Creates a detailed report of all artists and works in the archive,
    supporting multiple output formats.

    Examples:

        ubu report

        ubu report --format json --output archive-report.json

        ubu report --format csv > archive.csv
    """
    click.echo("Generating report...")

    try:
        page = Page()
        artists = page.get_artists(FILM_URL)

        if format == "text":
            _generate_text_report(artists, page, output)
        elif format == "json":
            _generate_json_report(artists, page, output)
        elif format == "csv":
            _generate_csv_report(artists, page, output)

        if output:
            click.secho(f"✓ Report written to {output}", fg="green")

    except Exception as e:
        click.secho(f"✗ Error generating report: {e}", fg="red", err=True)
        if ctx.obj.get("verbose", 0) > 0:
            logging.exception("Full traceback:")
        raise


def _generate_text_report(artists, page, output):
    """Generate a text format report."""
    lines = []
    lines.append("=" * 60)
    lines.append("UBUWEB ARCHIVE REPORT")
    lines.append("=" * 60)
    lines.append(f"Total Artists: {len(artists)}")
    lines.append("")

    total_works = 0
    errors = 0
    for artist in artists:
        try:
            works = page.get_artist_works(artist)
            total_works += len(works)
            lines.append(f"{artist.name}")
            lines.append(f"  URL: {artist.url}")
            lines.append(f"  Works: {len(works)}")
            lines.append("")
        except Exception:
            logging.error(
                f"Failed to get works for artist: {artist.name}", exc_info=True
            )
            errors += 1
            lines.append(f"{artist.name} [ERROR]")
            lines.append(f"  URL: {artist.url}")
            lines.append("  Works: Unable to retrieve")
            lines.append("")

    lines.append("=" * 60)
    lines.append(f"Total Works: {total_works}")
    if errors > 0:
        lines.append(f"Errors: {errors} artist(s) failed")
    lines.append("=" * 60)

    report_text = "\n".join(lines)

    if output:
        with open(output, "w") as f:
            f.write(report_text)
    else:
        click.echo(report_text)


def _generate_json_report(artists, page, output):
    """Generate a JSON format report."""
    import json

    data = {"total_artists": len(artists), "artists": [], "errors": 0}

    total_works = 0
    for artist in artists:
        try:
            works = page.get_artist_works(artist)
            total_works += len(works)

            artist_data = {
                "name": artist.name,
                "url": artist.url,
                "work_count": len(works),
                "works": [{"name": work.name, "url": work.url} for work in works],
            }
            data["artists"].append(artist_data)
        except Exception:
            logging.error(
                f"Failed to get works for artist: {artist.name}", exc_info=True
            )
            data["errors"] += 1
            artist_data = {
                "name": artist.name,
                "url": artist.url,
                "work_count": None,
                "error": "Failed to retrieve works",
            }
            data["artists"].append(artist_data)

    data["total_works"] = total_works

    json_output = json.dumps(data, indent=2)

    if output:
        with open(output, "w") as f:
            f.write(json_output)
    else:
        click.echo(json_output)


def _generate_csv_report(artists, page, output):
    """Generate a CSV format report."""
    import csv
    import io

    if output:
        with open(output, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Artist Name", "Artist URL", "Work Name", "Work URL"])
            for artist in artists:
                try:
                    works = page.get_artist_works(artist)
                    for work in works:
                        writer.writerow([artist.name, artist.url, work.name, work.url])
                except Exception:
                    logging.error(
                        f"Failed to get works for artist: {artist.name}", exc_info=True
                    )
                    writer.writerow(
                        [artist.name, artist.url, "ERROR", "Failed to retrieve works"]
                    )
    else:
        output_buffer = io.StringIO()
        writer = csv.writer(output_buffer)
        writer.writerow(["Artist Name", "Artist URL", "Work Name", "Work URL"])
        for artist in artists:
            try:
                works = page.get_artist_works(artist)
                for work in works:
                    writer.writerow([artist.name, artist.url, work.name, work.url])
            except Exception:
                logging.error(
                    f"Failed to get works for artist: {artist.name}", exc_info=True
                )
                writer.writerow(
                    [artist.name, artist.url, "ERROR", "Failed to retrieve works"]
                )
        click.echo(output_buffer.getvalue())


@cli.command()
@click.argument("artist_name", required=False)
@click.pass_context
def random(ctx, artist_name):
    """
    Download a random work from the archive.

    If ARTIST_NAME is provided, downloads a random work from that artist.
    Otherwise, downloads a random work from a random artist.

    Examples:

        ubu random

        ubu random "Chantal Akerman"
    """
    page = Page()
    artists = page.get_artists(FILM_URL)

    if artist_name:
        # Find the specified artist
        matching_artists = [a for a in artists if artist_name.lower() in a.name.lower()]

        if not matching_artists:
            click.secho(
                f"✗ No artist found matching '{artist_name}'", fg="red", err=True
            )
            raise click.Abort()

        if len(matching_artists) > 1:
            click.echo(f"Found {len(matching_artists)} matching artists:")
            for i, artist in enumerate(matching_artists, 1):
                click.echo(f"  {i}. {artist.name}")

            try:
                choice = click.prompt("Select artist number", type=int)
                if choice < 1 or choice > len(matching_artists):
                    click.secho("✗ Selection out of range", fg="red", err=True)
                    raise click.Abort()
                selected_artist = matching_artists[choice - 1]
            except click.Abort:
                raise
            except KeyboardInterrupt:
                click.secho("\n✗ Cancelled", fg="red", err=True)
                raise click.Abort()
        else:
            selected_artist = matching_artists[0]

        click.echo(f"Downloading random work from: {selected_artist.name}")
        download_random_work_from([selected_artist])
    else:
        click.echo("Downloading random work from random artist...")
        download_random_work_from(artists)

    click.secho("✓ Download complete!", fg="green")


def main():
    """Entry point for the CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
