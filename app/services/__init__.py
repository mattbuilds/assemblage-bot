class SlackParser():
	def __init__(self, text):
		self.choices = self.__split_text(text)

	def __split_text(self, text):
		text = text.replace(', ', ' ')
		return text.split()

	def get(self):
		return self.choices

class SlackOutput():
	def __init__(self, text=None, response_type=None):
		self.response = {}
		if text:
			self.response['text'] = text
		if response_type is not None:
			self.response['response_type'] = response_type
		self.response.setdefault('response_type', 'in_channel')

	def update_text(self, text):
		self.response['text'] = text

	def update_response_type(self, response_type):
		self.response['response_type'] = response_type

class LiborOutput():
	""" Prepares and formats the JSON output to be consumed by the Slack API

	Attributes:
		colors: that will be displayed in the Slack UI
		row_titles: list of row titles to look for to be outputed
	"""
	def __init__(self):
		self.colors = ['439FE0','ff5050']
		self.row_titles = ['Libor 1 Month', 'Libor 1 Year']

	def generate(self, titles, rows):
		""" Generates an output dictionary of libor rates
		Arguments:
			titles: a list of titles parsed from the HTML libor lookup
			rows: a list of rows parsed from the HTML libor lookup"""
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
		""" Creates a field dict 
		Arguments:
			titles: a list of titles parsed from the libor lookup
			row: the current row being parsed from the HTML libor lookup
			key: the column in the row to lookup
		"""
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
		""" Returns a dictionary of the output formatted for Slacks API """
		self.response = {
			'response_type':'in_channel', 
			'attachments' : [],
			'text' : titles[0]
		}