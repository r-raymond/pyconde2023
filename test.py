from __future__ import print_function

import argparse
import re
import sys

# This regex excludes the lines in the Worker that look like
# event.data['url'] + "/static/vendor/immutable.min.js"
RESTR = r'(?<!] \+ ")/static/'
REPLACE_WITH = "https://cdn.rawgit.com/jiffyclub/snakeviz/v0.4.2/snakeviz/static/"


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description=(
            "Prepare an HTML file from SnakeViz for use as a static page. "
            "The modified HTML is printed to stdout."
        )
    )
    parser.add_argument(
        "htmlfile",
        type=argparse.FileType("r"),
        help="HTML to convert to a static page.",
    )
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    html = args.htmlfile.read()
    print(re.sub(RESTR, REPLACE_WITH, html))


if __name__ == "__main__":
    sys.exit(main())
