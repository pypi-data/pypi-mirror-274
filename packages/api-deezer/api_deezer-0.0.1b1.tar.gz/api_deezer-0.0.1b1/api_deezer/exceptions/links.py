class Invalid_Link(Exception):
	def __init__(
		self,
		link: str,
		type_link: str,
		message: str = 'Invalid link \'{link}\' for type \'{type_link}\''
	):
		self.link = link
		self.type = type_link
		self.message = message

		super().__init__(
			self.message.format(
				link = link,
				type_link = type_link
			)
		)

class Error_Making_Link(Exception):
	def __init__(
		self,
		link: str,
		type_link: str,
		message: str = 'Something went bad during url crafting \'{link}\' for type \'{type_link}\''
	):
		self.link = link
		self.type = type_link
		self.message = message

		super().__init__(
			self.message.format(
				link = link,
				type_link = type_link
			)
		)