from unittest import TestCase

from ..api import API
from ..exceptions.data import Error_Data_404


class Test_Types_Serialization(TestCase):
	def __init__(self, methodName: str = "runTest") -> None:
		super().__init__(methodName)
		self.__api = API()

	def test_album(self):
		"""
		Test that json from album is serialized correctly
		"""

		album_links = (
			'https://api.deezer.com/album/103248', 'https://www.deezer.com/us/album/61014232',
			'https://www.deezer.com/us/album/48667542', 'https://www.deezer.com/us/album/48667541'
		)

		for album_link in album_links:
			try:
				self.__api.get_album(album_link)
			except Error_Data_404:
				pass
	
	def test_track(self):
		"""
		Test that json from track is serialized correctly
		"""

		track_links = (
			'https://api.deezer.com/track/916409', 'https://deezer.page.link/JvPGmTbTvAvQrzAq6'
		)
		
		for track_link in track_links:
			track = self.__api.get_track(track_link)
			print(track.explicit_content_lyrics)
			print(track.explicit_content_cover)


	def test_artist(self):
		"""
		Test that json from artist is serialized correctly
		"""

		artist_links = (
			'https://deezer.page.link/WaEsJEunPW7zYgSf8', 'https://api.deezer.com/artist/13',
			'https://deezer.page.link/dUjJTkNsBXphpNWb9'
		)

		for artist_link in artist_links:
			self.__api.get_artist(artist_link)

	def test_playlist(self):
		"""
		Test that json from playlist is serialized correctly
		"""

		playlist_links = (
			'https://api.deezer.com/playlist/10759081022', 'https://www.deezer.com/us/playlist/7326402184'
		)

		for playlist_link in playlist_links:
			playlist = self.__api.get_playlist(playlist_link)
			print(playlist.tracks[0].explicit_content_lyrics)


	def test_chart(self):
		"""
		Test that json from chart is serialized correctly
		"""

		self.__api.get_chart()


	def test_search(self):
		"""
		Test that json from search is serialized correctly
		"""

		self.__api.search('eminem')
		#pp(res)