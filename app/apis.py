"""Routes and functoins for API calls

All slackbot API/controller functions will be placed here.
"""

import random
import json
from flask import request, jsonify
from . import app
from .services import SlackParser, SlackOutput
from .poll import PollParser, PollOutput

@app.route('/message', methods=['POST'])
def handle_interactive_message():
    """Takes the vote from a poll and does the following:
    - Tally's the vote
    - Sends an update to the 'results' message with udated votes
    """
    payload = json.loads(request.form['payload'])
    parser = PollParser(payload)

    #Add vote to db
    vote = parser.tally_vote()

    #Update results
    results = PollOutput("Results")
    results.create_result_attachments(vote.poll_id)
    results.response['ts'] = parser.get_results_message_ts(vote.poll_id)
    parser.update_message(results.response)
    return "Thanks for voting."

@app.route('/poll', methods=['POST'])
def create_poll():
    """Creates a poll from a slack slash command

    Will take and parse the incoming text and then create a poll. After a poll
    has been created, a poll message will go to each member of the chat as
    well as a channel message that has the results of the pll
    """
    parser = PollParser(request.form)

    #Create poll and send request
    output = PollOutput(parser.get_title())
    poll = parser.add_vote_to_db()
    output.create_button_message(parser.get(), poll.id)
    parser.create_vote(output.response, poll.id)

    #Poll Results Message
    results = PollOutput("Results")
    results.create_result_attachments(poll.id)
    response = parser.send_results(results.response)
    parser.log_results_message_ts(poll.id, response['ts'])

    return ('', 200)

@app.route('/random', methods=['GET', 'POST'])
def get_random():
    """A slack slash command that will parse a string based on ', ' and
    select a random element from the parsed string
    """
    choices = SlackParser(request.form).get()
    selected = random.choice(choices)
    output = SlackOutput(text=selected)
    return jsonify(output.response)
