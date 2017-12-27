import random
import json
from flask import request, Flask, jsonify
from . import app, db
from .helpers import get_libor_page, parse_libor_page
from .services import SlackParser, LiborOutput, SlackOutput
from .lunch import LunchParser, LunchOutput
from slackclient import SlackClient

@app.route('/lunch', methods=['GET', 'POST'])
def testing():
	choices = LunchParser(request.form).get()
	output = LunchOutput("Lunch Order")
	output.set_channel("#bottest")
	output.create_button_message(choices)
	response = output.send_request()
	return jsonify(response)

@app.route('/message', methods=['POST'])
def handle_interactive_message():
	payload = json.loads(request.form['payload'])
	sp = LunchParser(payload)
	output = LunchOutput("Lunch Order")
	output.create_response_message(sp.choice)
	return jsonify(output.response)

@app.route('/poll', methods=['POST'])
def create_lunch_poll():
	choices = LunchParser(request.form).get()
	output = LunchOutput("Lunch Order")
	output.set_channel("#bottest")
	output.create_button_message(choices)
	response = output.send_request()

@app.route('/random', methods=['GET', 'POST'])
def get_random():
	choices = SlackParser(request.form).get()
	selected = random.choice(choices)

	output = SlackOutput(text=selected)
	return jsonify(output.response)
