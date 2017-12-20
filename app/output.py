class SlackOutput():
	""" Prepares and formats the JSON output to be consumed by the Slack API

	Attributes:
		colors: that will be displayed in the Slack UI
		row_titles: list of row titles to look for to be outputed
	"""
	def __init__(self):
		self.colors = ['439FE0','ff5050']
		self.row_titles = ['Libor 1 Month', 'Libor 1 Year']

	def generate(self, titles, rows):
		self.__set_initial_response(titles)
		for lrow in rows:
			if lrow[0] in self.row_titles:
					attch_row = {
						'title' : lrow[0],
						'fields' : [],
						'color' : self.colors.pop()
					}
					for key in range(1,5):
						attch_row['fields'].append(self.__get_field(titles, lrow, key))
					
					self.response['attachments'].append(attch_row)
		return self.response

	def __get_field(self, titles, row, key):
		if key in [3, 4]:
			addition = "52 Week "
		else:
			addition = ""

		field = {
			"title": addition + titles[key],
			"value": row[key],
			"short": True
		}
		return field

	def __set_initial_response(self, titles):
		"""Returns a dictionary of the output formatted for Slacks API"""
		self.response = {
			'response_type':'in_channel', 
			'attachments' : [],
			'text' : titles[0]
		}