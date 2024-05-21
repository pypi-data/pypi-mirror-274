#!/usr/bin/env python3
#
#  __main__.py
"""
Generate HTML Redirect File.
"""
#
#  Copyright © 2015, 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#
#  HTML output based on https://stackoverflow.com/a/5411601/
#  By https://stackoverflow.com/users/665261/billy-moon
#  CC BY-SA 3.0
#

# stdlib
import argparse
import pathlib
import sys

# this package
from create_redirect import create_redirect

__all__ = ("main", )


def main() -> int:  # noqa: D103
	parser = argparse.ArgumentParser(description="Generate HTML Redirect File.")
	parser.add_argument("redirect_url", help="The URL to redirect to")
	parser.add_argument(
			"output", nargs='?', default="redirect.html", help="Path of the file to create", type=pathlib.Path
			)

	args = parser.parse_args()

	redirect_url = args.redirect_url

	if not redirect_url.startswith("http"):
		url = f"http://{redirect_url}"
	else:
		url = redirect_url

	output = create_redirect(redirect_url)

	if str(args.output) == '-':
		print(output)
	else:
		output_file: pathlib.Path = args.output
		output_file.write_text(output, encoding="UTF-8")

		print(f"Successfully wrote file '{str(output_file)}' with url '{url}'")

	return 0


if __name__ == "__main__":
	sys.exit(main())
