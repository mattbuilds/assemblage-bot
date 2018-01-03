import random
import json
import time
from flask import request, Flask, jsonify
from . import app, db
from .services import SlackParser, SlackOutput, SlackApi
from .poll import PollParser, PollOutput

@app.route('/message', methods=['POST'])
def handle_interactive_message():
	payload = json.loads(request.form['payload'])
	sp = PollParser(payload)

	#Add vote to db
	vote = sp.tally_vote()

	#Update results
	poll_results = sp.get_poll_results(vote.poll_id)
	results = PollOutput("Lunch Order Results")
	results.create_result_attachments(poll_results)
	results.response['ts'] = sp.get_results_message_ts(vote.poll_id)
	sp.update_message(results.response)
	return ("Thanks for voting.")
	

@app.route('/poll', methods=['POST'])
def create_poll():
	parser = PollParser(request.form)

	#Create poll and send request
	output = PollOutput("Lunch Order")
	poll = parser.add_vote_to_db()
	output.create_button_message(parser.get(), poll.id)
	parser.create_vote(output.response, poll.id)

	#Poll Results Message
	poll_results = parser.get_poll_results(poll.id)
	results = PollOutput("Lunch Order Results")
	results.create_result_attachments(poll_results)
	response = parser.send_results(results.response)
	parser.log_results_message_ts(poll.id, response['ts'])

	return ('', 200)

@app.route('/random', methods=['GET', 'POST'])
def get_random():
	choices = SlackParser(request.form).get()
	selected = random.choice(choices)
	output = SlackOutput(text=selected)
	return jsonify(output.response)
