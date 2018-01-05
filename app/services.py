"""Services are the base classes for handling Slack. They give the ability
to parse, call the slack API, and format output for Slack to consume
"""

import json
import requests
from . import app
from .errors import TokenError

class SlackParser():
    """The base class used to parse data from an incoming slack command."""
    def __init__(self, data):
        """Authenticates, sets the user, channel, data, and splits text"""
        self.__authenticate(data)
        self.user_id = self.__parse_user_id(data)
        self.channel_id = self.__parse_channel_id(data)
        self.data = data
        if 'text' in data:
            self.text = data['text'].split(", ")

    def __authenticate(self, data):
        """Authenticates based on the token and SLACK_TOKEN in the cfg file"""
        if 'token' not in data:
            raise TokenError("Invalid Token")
        if data['token'] != app.config['SLACK_TOKEN']:
            raise TokenError("Invalid Token")

    def __parse_user_id(self, data):
        """The user_id can be sent 2 ways, tries both and returns the id"""
        if 'user_id' in data:
            return data['user_id']
        if 'user' in data:
            return data['user']['id']
        return None

    def __parse_channel_id(self, data):
        """The channel_id can be sent 2 ways, tries both and returns the id"""
        if 'channel_id' in data:
            return data['channel_id']
        if 'channel' in data:
            return data['channel']['id']
        return None

    def get(self):
        """Returns the parsed text"""
        return self.text

class SlackApi():
    """Used to call the slack API"""
    def __init__(self):
        """Sets the basic headers for all API calls"""
        self.headers = {
            'Authorization': 'Bearer ' + app.config['SLACK_BEARER']
        }

    def __call(self, headers, method, data):
        """Builds the Slack API request and calls the API"""
        url = 'https://slack.com/api/'+method
        req = requests.post(
            url=url,
            data=data,
            headers=headers
        )
        return req

    def __json_call(self, method, data):
        """Formats an API call to use JSON"""
        headers = self.headers
        headers['Content-type'] = 'application/json'
        data = json.dumps(data)
        return self.__call(headers, method, data)

    def __form_call(self, method, data):
        """Formats an API call to use form"""
        return self.__call(self.headers, method, data)

    def get_group_info(self, data):
        """API call to get an individual channels info"""
        return self.__form_call('channels.info', data)

    def get_channel_users(self, channel):
        """A function to get all the users of a channel"""
        data = {
            'token' : app.config['SLACK_BEARER'],
            'channel' : channel
        }

        group = self.__form_call('groups.info', data)
        group_dict = group.json()
        if not group_dict['ok']:
            channel = self.get_group_info(data)
            channel_dict = channel.json()
            return channel_dict['channel']['members']
        return group_dict['group']['members']

    def send_message(self, data):
        """An API call to send individual messages to a user"""
        return self.__json_call('chat.postEphemeral', data)

    def update_message(self, data):
        """Update an existing message"""
        return self.__json_call('chat.update', data)

    def send_group_message(self, data):
        """Post a message for the entire channel/group"""
        return self.__json_call('chat.postMessage', data)

class SlackOutput():
    """Used to create output that Slack can use either through a return or
    sent as an API call
    """
    def __init__(self, text=None, response_type=None):
        """Sets the most fundamental pieces of the output, the text
        and the response type.
        Defaults response type to 'in_channel'
        """
        self.response = {}
        if text:
            self.response['text'] = text
        if response_type is not None:
            self.response['response_type'] = response_type
        self.response.setdefault('response_type', 'in_channel')

    def set_channel(self, channel):
        """Set the channel of where to send the response"""
        self.response['channel'] = channel

    def set_attachments(self):
        """Set's the attachments section to an empty list"""
        self.response['attachments'] = []

    def add_attachment(self, title, text):
        """Append one attachment to the attachments list"""
        attachment = {
            'title': title,
            'text': text
        }
        self.response['attachments'].append(attachment)

    def update_text(self, text):
        """Update the text section"""
        self.response['text'] = text

    def update_response_type(self, response_type):
        """Update the response type"""
        self.response['response_type'] = response_type
