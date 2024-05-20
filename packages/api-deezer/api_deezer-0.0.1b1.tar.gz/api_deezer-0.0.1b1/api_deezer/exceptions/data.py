class Error_Data_404(Exception):
	def __init__(
		self,
		link: str,
		type_link: str,
		message: str = 'No Data info for \'{link}\' for type \'{type_link}\''
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