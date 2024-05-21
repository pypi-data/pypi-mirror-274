#!/usr/bin/env python3
#
#  __init__.py
"""
Python script for creating HTML redirects.
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

# stdlib
from textwrap import dedent

__all__ = ["create_redirect"]

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2015, 2019-2020 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.2.1"
__email__: str = "dominic@davis-foster.co.uk"


def create_redirect(redirect_url: str) -> str:
	"""
	Generate HTML Redirect File.

	:param redirect_url: The URL to redirect to.

	:rtype:

	.. versionadded:: 0.2.0
	"""

	if not redirect_url.startswith("http"):
		url = f"http://{redirect_url}"
	else:
		url = redirect_url

	template = """\
	<!DOCTYPE HTML>
	<html lang="en-GB">
		<head>
			<meta charset="UTF-8">
			<meta http-equiv="refresh" content="1";url='{0}'>
			<script type="text/javascript">
				window.location.href = '{0}'
			</script>
			<title>Page Redirection</title>
		</head>
		<body>
			If you are not redirected automatically, follow <a href='{0}'>this link</a>
		</body>
	</html>"""

	return dedent(template.format(url))
