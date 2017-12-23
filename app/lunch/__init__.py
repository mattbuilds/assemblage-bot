from ..services import SlackParser
from .models import SlackUser, LunchVote, LunchVoteOptions
from .. import db

class LunchParser(SlackParser):
	def __init__(self, input):
		SlackParser.__init__(self, input)
		self.__handle_user()

	def __handle_user(self):
		if not SlackUser.query.filter_by(user_id=self.user_id).count():
			user = SlackUser(user_id=self.user_id)
			db.session.add(user)
			db.session.commit()

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


class Lunch():
	def __init__(self):
		pass
