# https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/

from __future__ import annotations

from urllib.parse import urlparse

from functools import update_wrapper

from requests import get as req_get

from typing import (
	Any, TYPE_CHECKING
)

from ..exceptions.data import Error_Data_404

from ..exceptions.links import (
	Invalid_Link, Error_Making_Link
)


if TYPE_CHECKING:
	from ..api import API


VALID_DOMAINS = (
	'deezer.page.link', 'deezer.com', 'api.deezer.com',
	'www.deezer.com',
)

NOT_VERIFY = VALID_DOMAINS[1:]
__API_URL = 'https://api.deezer.com/{type_link}/{id_media}'

# https://book.pythontips.com/en/latest/decorators.html#decorators-with-arguments


def check_link(type_link: str):
	def decorator(func: Any):
		def inner(self: API, link: str) -> dict[str, Any]:
			url_parsed = urlparse(link)

			if 'deezer.page.link' == url_parsed.netloc:
				url = req_get(link).url
				url_parsed_new = urlparse(url)
				path = url_parsed_new.path
			elif url_parsed.netloc in NOT_VERIFY:
				path = url_parsed.path
			else:
				raise Invalid_Link(link, type_link)

			if not type_link in path:
				raise Invalid_Link(link, type_link)

			id_media = path.split('/')[-1]

			if not id_media.isdigit():
				raise Error_Making_Link(link, type_link)

			c_api_url = __API_URL.format(
				type_link = type_link,
				id_media = id_media
			)

			json_data: dict[str, Any] = req_get(c_api_url).json()
			is_error: dict[str, Any] | None = json_data.get('error')

			if is_error:
				match is_error['type']:
					case 'DataException':
						raise Error_Data_404(link, type_link)
					case _:
						raise Exception(f'Error {is_error['type']} unknown. Link {link}. Report this kindly :)')

			return json_data

		update_wrapper(inner, func)

		return inner

	return decorator