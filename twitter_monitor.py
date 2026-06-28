"""DEPRECATED: Twitter monitoring script for UbuWeb updates.

WARNING: This script is no longer functional due to Twitter/X shutting down
their free API access.

This file is kept for historical reference only.

ALTERNATIVE: Use periodic full scans with skip-existing instead:

    # Manual run
    uv run python main.py

    # Or set up a cron job for automatic updates
    0 2 * * * cd /path/to/ubuweb-mirror && uv run python main.py >> /var/log/ubuweb.log 2>&1

The skip-existing feature will efficiently download only new files.
"""

import sys
import warnings

warnings.warn(
    "twitter_monitor.py is DEPRECATED. Twitter API is no longer available. "
    "Use 'uv run python main.py' with skip-existing instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Original functionality no longer works due to Twitter API shutdown
print("ERROR: This script is deprecated and non-functional.")
print("Twitter/X has shut down their free API access.")
print()
print("Please use 'uv run python main.py' instead for incremental downloads.")
print("See TWITTER_DEPRECATION.md for details.")
sys.exit(1)
