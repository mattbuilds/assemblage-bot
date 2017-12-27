from ..services import SlackParser, SlackOutput
from .models import SlackUser, LunchVote, LunchVoteOptions
from .. import db

class LunchParser(SlackParser):
	def __init__(self, input):
		SlackParser.__init__(self, input)
		self.__handle_user()
		if 'actions' in input:
			self.choice = self.__get_selection(input)

	def __handle_user(self):
		if not SlackUser.query.filter_by(user_id=self.user_id).count():
			user = SlackUser(user_id=self.user_id)
			db.session.add(user)
			db.session.commit()

	def __get_selection(self, input):
		return input['actions'][0]['value']

	def create_vote(self):
		#Get Users in Channel
		#Create Users in DB
		self.__add_vote_to_db()
		#Send Form to Users

	def __add_vote_to_db(self):
		lunch_vote = LunchVote()
		db.session.add(lunch_vote)
		for option in self.text:
			lunch_option = LunchOption(lunch_vote=lunch_vote, name=option)
			db.session.add(lunch_option)
		db.session.commit()


class LunchOutput(SlackOutput):
	def __init__(self, text=None, responder_type=None):
		SlackOutput.__init__(self, text, responder_type)
		self.set_attachments()
		self.actions = []

	def create_response_message(self, choice):
		attachment = {
			"title" : "Choose a lunch to order",
			"text" :" You have selected " + choice,
			"fallback": "Something went wrong, you can't pick lunch",
			"callback_id":"lunch_order",
			"attachment_type":"default"
		}
		self.response['attachments'].append(attachment)

	def create_button_message(self, choices):
		for choice in choices:
			self.add_button(choice)
		attachment = {
			"title" : "Choose a lunch to order",
			"fallback": "Something went wrong, you can't pick lunch",
			"callback_id":"lunch_order",
			"attachment_type":"default",
			"actions":self.actions
		}
		self.response['attachments'].append(attachment)

	def add_button(self, button):
		action = {
			'name':'lunch',
			'text': button,
			'type': "button",
			'value': button
		}
		self.actions.append(action)


