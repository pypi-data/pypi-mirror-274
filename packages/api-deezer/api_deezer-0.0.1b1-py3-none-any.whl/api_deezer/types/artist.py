from pydantic import BaseModel


class Artist(BaseModel):
	id: int
	name: str
	link: str
	share: str
	picture: str
	picture_small: str
	picture_medium: str
	picture_big: str
	picture_xl: str
	nb_album: int
	nb_fan: int
	radio: bool
	tracklist: str
	type: str