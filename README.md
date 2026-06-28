# Brutal Poetry of Archiving

If [Ubuweb](https://www.ubu.com) is an archive of concrete poetry, this repository is brulist poetry. It elevates the entropic form of
freestyle anacronicsic coding of text and attempts to provide organization with sharp lines, smooth surfaces
and precision molded materlal forms. Through this reforming of the contents, many of the duplicates, broken links and typos are fixed.

The brualist form opines on the taxonomy of the primary text, providing a fresh shape for others to use
for education, entertainment and collective spaces. As a direct challenge to the author's belief that SQL databases are garbage[citation needed], it provides an interface to mirror all of Ubuweb's contents into a SQL database.

The current state of the code mirrors everything available from the film section. More sections will come online as the boutique HTML is parsed, collected, understood and re-formed into something helpful to both our human and machine counterparts.

The code functions to be aggressive but not repetitive. It only downloads new contents once. It abstracts when the primary source does not. It maps the conventions found in the psychogeography of each artist's works into objects of data to be used arbitrarily. When there is javascript to obsfucate links, it will guess right.

For more context, see this interview with [Kenneth Goldsmith](https://vimeo.com/60377169) for some of the motivation to create this work.

# Instructions for The Reader

## Installation

The project now uses [uv](https://github.com/astral-sh/uv) for fast, reliable dependency management.

### Quick Start with uv

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup the project
git clone https://github.com/lazzarello/ubuweb-mirror.git
cd ubuweb-mirror

# Install all dependencies (including dev dependencies)
uv sync

# Or install without dev dependencies
uv sync --no-dev
```

### Legacy Installation (pip)

```bash
pip install -r requirements.txt
# For development
pip install -r requirements-dev.txt
```

## Usage

### File Organization

The script now separates HTML files from audio/video content:

- **A/V Content**: Saved to `~/jellyfin/ubuweb/` (configurable via `DOWNLOAD_PATH` in `ubu/constants.py`)
- **HTML Files**: Saved to `~/tmp/ubuweb/` (configurable via `HTML_PATH` in `ubu/constants.py`)

This separation ensures that your media server directory (like Jellyfin) only contains playable A/V content, while HTML files (which are typically non-functional fragments or redirects) are stored separately for future reference.

### As a Module

You can now import and use ubu in your own scripts:

```python
import ubu

# Download all works from all artists
ubu.full_download_run()

# Or work with individual components
page = ubu.Page()
artists = page.get_artists(ubu.FILM_URL)
ubu.download_all_works_from(artists[0])
```

### As a Script

Run with uv:
```bash
# Download new files, skip existing (default)
uv run python main.py

# Force re-check all files
uv run python main.py --no-skip
```

Or with traditional Python:
```bash
python main.py
```

**Skip-Existing Feature**: The script automatically builds an index of your existing files at startup (takes ~0.02 seconds for 3000+ files) and skips files you already have. This makes incremental updates very fast - it only downloads new content added to UbuWeb.

### Running Tests

```bash
# With uv (recommended)
uv run pytest tests/ -v

# Or run the test runner directly
uv run python tests/run_tests.py

# Legacy method
python tests/run_tests.py
```

## Twitter

Note: Twitter monitoring is in a separate script now.

It's possible to enable a service to monitor @ubuweb on Twitter and extract new tweets with film contents. This requires a Twitter developer account. Put your authentication creds into the `environments.sample` file and copy it to a file named `environments` so it won't get checked into source control. Run the following

```
cp environments.sample environments
source environments
uv run python twitter_monitor.py
```

*Notes* 

* The project uses `uv` for dependency management. The `uv.lock` file ensures reproducible builds.
* The `requests-html` library will download **a headless version of the Chromium web browser** so it can render JavaScript into static HTML to be scraped. This happens once and only once upon the first `render()` call from this library.
* A meaningful quantity of pages in the primary text are broken or destroyed. There is improvisational poetry in 
  the code to describe these scenarios, though the primary text may change at any time, creating more opportunities
  for improvisation.
* Exceptions are written to `transfers.log`, along with the Artist object which caused the exception.
* Some videos are hosted on streaming sites. This text addresses many of these ideas but some are too complex for
  our language to express. The resulting primary content cannot be written.
* The youtube-dl dependency is used to download films from streaming sites. It is a large text, though the reader
  should rarely need to see the contents.
* The film archive will require aproximately 630 GB of space on your local hard disk.
* Each time the reader writes, content which has been previously written will be skipped.

## Reading

TODO: Develop some interesting ways to read through the contents. Ideas include, random artist, random work, generate an alrogithmically curated show of artist's works, etc, etc.

## Endnotes

The following list is known to be broken in a way that this text cannot yet describe.

index 215
https://www.ubu.com/film/clarke_ornette.html
this index uses Javascript to render the link to media. the
streaming video uses a service called https://criticalcommons.org/embed?m=fwqF8eomo
which is not valid in youtube-dl. Perhaps include this site in that project and make a PR?

index 15 page not found, redirect

index 9 dmca takedown, zero works.

https://www.ubu.com/film/alferi.html
has a tags with no text, so text validation fails.
This is a typo and the text is outside the closing tag for a couple nodes because, poetry.
The href tag is valid so this is possible to handle by searching for all <a> tags where `get_text()` is an empty string.

https://www.ubu.com/film/alchemists.html
There is no Artist page, I guess because The BBC Radiophonic Workshop is not good enough to be an artist.
This breaks our Page object model, which expects one Artist to have many Works. This page has no Artist
and one Work.

## TODO

* Include an ORM or something for a local SQLlite
* Build a better system to uniquely identify artists than array indexes built in the order of <a> tags in the DOM
* Refactor Page model to only accept a URL object for all methods
* Optimize requests sent to the primary source in URL class when looking up data
* Build conventions to extract the "description" for artists and works. This is untagged text floating around the DOM.  Perhaps a guess of sibling text to the <table> tag with a word count > x? It's gonna be tough!
* Develop the reading chapter
* Extend broken links and zero content pages to a model that will always represent an accurate broken state of the primary text.
* Add a system to email Kenny G (NOT the WFMU person, whew) this list of broken things. Maybe they'll fix them!
* Make a partial download system
* Optimize system to check for existing downloads concurrently. This feels like it will be difficult.
* Try out different writing algorithms rather then linear order of <a> elements in the DOM.
* Concurrent downloads!
* Add command line arguments with the `click` library
