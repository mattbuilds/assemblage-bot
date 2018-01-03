from . import app
from .errors import TokenError
import requests
import json

class SlackParser():
	def __init__(self, input):
		self.__authenticate(input)
		self.user_id = self.__parse_user_id(input)
		self.channel_id = self.__parse_channel_id(input)
		self.input = input
		if 'text' in input:
			self.text = self.__split_text(input['text'])

	def __parse_channel_id(self, input):
		if 'channel_id' in input:
			return input['channel_id']
		if 'channel' in input:
			return input['channel']['id']

	def __parse_user_id(self, input):
		if 'user_id' in input:
			return input['user_id']
		if 'user' in input:
			return input['user']['id']

	def __authenticate(self, input):
		if 'token' not in input:
			raise TokenError("Invalid Token")
		if input['token'] != app.config['SLACK_TOKEN']:
			raise TokenError("Invalid Token")

	def __split_text(self, text):
		text = text.replace(', ', ' ')
		return text.split()

	def get(self):
		return self.text

class SlackApi():
	def __init__(self):
		self.headers = {
			'Authorization': 'Bearer ' + app.config['SLACK_BEARER']
		}

	def __call(self, headers, method, data):
		url = 'https://slack.com/api/'+method
		r = requests.post(
			url=url,
			data=data,
			headers=headers
		)
		return r

	def __json_call(self, method, data):
		headers = self.headers
		headers['Content-type'] = 'application/json'
		data = json.dumps(data)
		return self.__call(headers, method, data)

	def __form_call(self, method, data):
		return self.__call(self.headers, method, data)

	def get_group_info(self, data):
		return self.__form_call('channels.info', data)

	def get_channel_users(self, channel):
		data = {
			'token' : app.config['SLACK_BEARER'],
			'channel' : channel
		}

		group = self.__form_call('groups.info', data)
		group_dict = group.json()
		if not group_dict['ok']:
			channel = self.__form_call('channels.info', data)
			channel_dict = channel.json()
			return channel_dict['channel']['members']
		else:
			return group_dict['group']['members']

	def send_message(self, data):
		return self.__json_call('chat.postEphemeral', data)

	def update_message(self, data):
		return self.__json_call('chat.update', data)

	def send_group_message(self, data):
		return self.__json_call('chat.postMessage', data)

class SlackOutput():
	def __init__(self, text=None, response_type=None):
		self.response = {}
		if text:
			self.response['text'] = text
		if response_type is not None:
			self.response['response_type'] = response_type
		self.response.setdefault('response_type', 'in_channel')

	def set_channel(self, channel):
		self.response['channel'] = channel

	def set_attachments(self):
		self.response['attachments'] = []

	def add_attachment(self, title, text):
		attachment = {
			'title': title,
			'text': text
		}
		self.response['attachments'].append(attachment)

	def update_text(self, text):
		self.response['text'] = text

	def update_response_type(self, response_type):
		self.response['response_type'] = response_type

	def send_request(self):
		headers = {
			'Content-type':'application/json',
			'Authorization': 'Bearer ' + app.config['SLACK_BEARER']
		}

		r = requests.post(
			'https://slack.com/api/chat.postMessage',
			data = json.dumps(self.response),
			headers=headers
		)
		return json.loads(r.text)