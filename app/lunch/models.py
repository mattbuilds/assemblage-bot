from app import db
from datetime import datetime

class SlackUser(db.Model):
	__tablename__ = 'slack_user'

	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.String(60))
	choices = db.relationship('LunchVoteChoice', backref='slack_user', lazy=True)

class LunchVote(db.Model):
	_tablename__ = 'lunch_vote'

	id = db.Column(db.Integer, primary_key = True)
	created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	options = db.relationship('LunchVoteOptions', backref='lunch_vote', lazy=True)
	choices = db.relationship('LunchVoteChoice', backref='lunch_vote', lazy=True)

class LunchVoteOptions(db.Model):
	__tablename__ = 'lunch_vote_options'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), nullable=False)
	choices = db.relationship('LunchVoteChoice', backref='options', 
		lazy=True)
	lunch_vote_id = db.Column(db.Integer, db.ForeignKey('lunch_vote.id'), 
		nullable=False)


class LunchVoteChoice(db.Model):
	__tablename__ = 'lunch_vote_choice'

	id = db.Column(db.Integer, primary_key=True)
	lunch_vote_id = db.Column(db.Integer, db.ForeignKey('lunch_vote.id'), 
		nullable=False)
	lunch_vote_options_id = db.Column(db.Integer, 
		db.ForeignKey('lunch_vote_options.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('slack_user.id'), nullable=False)


