from app import db
from datetime import datetime

class SlackUser(db.Model):
	__tablename__ = 'slack_user'

	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.String(60))
	choices = db.relationship('PollVote', backref='slack_user', lazy=True)

class Poll(db.Model):
	_tablename__ = 'poll'

	id = db.Column(db.Integer, primary_key = True)
	created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	channel = db.Column(db.String(60))
	results_message_ts = db.Column(db.String(128))
	options = db.relationship('PollOption', backref='poll', lazy=True)
	choices = db.relationship('PollVote', backref='poll', lazy=True)

class PollOption(db.Model):
	__tablename__ = 'poll_option'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), nullable=False)
	choices = db.relationship('PollVote', backref='options', 
		lazy=True)
	poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), 
		nullable=False)


class PollVote(db.Model):
	__tablename__ = 'poll_vote'

	id = db.Column(db.Integer, primary_key=True)
	message_ts =  db.Column(db.String(128))
	poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), 
		nullable=False)
	poll_option_id = db.Column(db.Integer, db.ForeignKey('poll_option.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('slack_user.id'), nullable=False)


