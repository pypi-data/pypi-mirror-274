from typing import Any

from requests import get as req_get

from .types import (
	Track, Album,
	Playlist, Artist, Chart
)

from .decorators.links import check_link


class API:
	__API_URL = 'https://api.deezer.com/'


	@check_link(type_link = 'track')
	def get_track_JSON(self, link: str) -> None:
		'''

		Function for getting Track's infos in JSON format

		'''


	def get_track(self, link: str) -> Track:
		res = self.get_track_JSON(link)

		return Track.model_validate(res)  # https://docs.pydantic.dev/latest/concepts/models/#helper-functions


	@check_link(type_link = 'album')
	def get_album_JSON(self, link: str) -> None:
		'''

		Function for getting Album's infos in JSON format

		'''


	def get_album(self, link: str) -> Album:
		res = self.get_album_JSON(link)

		return Album.model_validate(res)


	@check_link(type_link = 'artist')
	def get_artist_JSON(self, link: str) -> None:
		'''

		Function for getting Artist's infos in JSON format

		'''


	def get_artist(self, link: str) -> Artist:
		res = self.get_artist_JSON(link)

		return Artist.model_validate(res)


	@check_link(type_link = 'playlist')
	def get_playlist_JSON(self, link: str) -> None:
		'''

		Function for getting Playlist's infos in JSON format

		'''


	def get_playlist(self, link: str) -> Playlist:
		res = self.get_playlist_JSON(link)

		return Playlist.model_validate(res)


	def get_chart_JSON(self) -> dict[str, Any]:
		'''

		Function for getting Chart's infos in JSON format

		'''

		method = 'chart'
		url = f'{self.__API_URL}{method}'

		return req_get(url).json()


	def get_chart(self) -> Chart:
		res = self.get_chart_JSON()

		return Chart.model_validate(res)


	def search(self, q: str, obj: bool = True) -> dict[str, Any]:
		method = 'search'
		url = f'{self.__API_URL}{method}?q={q}'
		res = req_get(url).json()

		return res