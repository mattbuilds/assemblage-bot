from ..services import SlackParser, SlackOutput, SlackApi
from .models import SlackUser, Poll, PollOption, PollVote
from .. import db

class PollParser(SlackParser):
	def __init__(self, input):
		super().__init__(input)
		self.api = SlackApi()
		self.upsert_handle_user(self.user_id)
		if 'actions' in input:
			self.choice = self.__get_selection(input)

	def upsert_handle_user(self, user_id):
		if not SlackUser.query.filter_by(user_id=user_id).count():
			user = SlackUser(user_id=user_id)
			db.session.add(user)
			db.session.commit()

	def __get_selection(self, input):
		return input['actions'][0]['value']

	def send_results(self, message):
		message['channel'] = self.channel_id
		result = self.api.send_group_message(message)
		return result.json()

	def get_results_message_ts(self, poll_id):
		poll = Poll.query.get(poll_id)
		return poll.results_message_ts

	def log_results_message_ts(self, poll_id, ts):
		poll = Poll.query.get(poll_id)
		poll.results_message_ts = ts
		db.session.commit()

	def create_vote(self, message, poll_id):
		message['channel'] = self.channel_id

		#Get Users in Channel
		users = self.api.get_channel_users(self.channel_id)
		
		#Create Users in DB
		for user in users:
			self.upsert_handle_user(user)
			user_message = message
			user_message['user'] = user
			response = self.api.send_message(user_message)
			self.__create_poll_vote(user, poll_id, response)

	def __create_poll_vote(self, user_id, poll_id, response):
		resp_dict = response.json()
		user = SlackUser.query.filter_by(user_id = user_id).first()
		vote = PollVote(
			poll_id = poll_id,
			user_id = user.id,
			message_ts = resp_dict['message_ts']
		)
		db.session.add(vote)
		db.session.commit()
		return vote

	def get_poll_results(self, poll_id):
		poll_options = PollOption.query.filter_by(poll_id=poll_id).all()
		return poll_options

	def get_poll_users(self, poll_id):
		users = PollVote.query.filter_by(poll_id=poll_id).all()
		return users

	def tally_vote(self):
		user = SlackUser.query.filter_by(user_id = self.user_id).first()
		poll_option = PollOption.query.filter_by(
			name=self.input['actions'][0]['value'], 
			poll_id=self.input['callback_id']).first()
		vote = PollVote.query.filter_by(
			message_ts=self.input['message_ts']).first()
		vote.poll_option_id = poll_option.id
		db.session.commit()
		return vote

	def update_message(self, message):
		message['channel'] = self.channel_id
		result = self.api.update_message(message)
		return result.json()

	def add_vote_to_db(self):
		poll = Poll()
		db.session.add(poll)
		for option in self.text[1:]:
			poll_option = PollOption(poll=poll, name=option)
			db.session.add(poll_option)
		db.session.commit()
		return poll

	def get_title(self):
		return self.text[0]

	def get(self):
		return self.text[1:]

class PollOutput(SlackOutput):
	def __init__(self, text=None, responder_type=None):
		SlackOutput.__init__(self, text, responder_type)
		self.set_attachments()
		self.actions = []

	def create_result_attachments(self, poll_results):
		for option in poll_results:
			attachment = {
				"title" : option.name,
				"text" : len(option.choices),
				"callback_id":option.name,
				"attachment_type":"default"
			}
			self.response['attachments'].append(attachment)
		return self.response

	def create_button_message(self, choices, callback_id):
		for choice in choices:
			self.add_button(choice)
		attachment = {
			"title" : "Select an item from below",
			"fallback": "Something went wrong, you can't pick lunch",
			"callback_id": callback_id,
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


