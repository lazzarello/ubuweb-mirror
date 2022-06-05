BASE_URL = "https://www.ubu.com/"
FILM_URL = "https://www.ubu.com/film/index.html"
BASE_FILM_URL = "https://www.ubu.com/film/"
DOWNLOAD_PATH = "/home/lee/Videos/ubuweb/"
ERROR_URL = "https://www.memoryoftheworld.org"
BROKEN_PAGES=[215,15,9]
'''
215
https://www.ubu.com/film/clarke_ornette.html
this index uses Javascript to render the link to media. the
streaming video uses a service called https://criticalcommons.org/embed?m=fwqF8eomo
which is not valid in youtube-dl

15 page not found, redirect

9 dmca takedown, zero works.

https://www.ubu.com/film/alferi.html
has a tags with no text, so text validation fails.
This is a typo and the text is outside the closing tag for a couple nodes. Poetry.
The href tag is valid so this is possible to handle tho...
'''
