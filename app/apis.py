import random
from flask import request, Flask, jsonify
from . import app, db
from .helpers import get_libor_page, parse_libor_page
from .services import SlackParser, LiborOutput, SlackOutput
from .lunch import LunchParser

@app.route('/test', methods=['GET', 'POST'])
def testing():
	LunchParser(request.form)
	return ("Hi")

def create_lunch_vote():
	parser = LunchParser(request.form)
	parser.create_vote()

@app.route('/lunch', methods=['GET', 'POST'])
def create_lunch_poll():
	SlackParser(request.form)
	output = SlackOutput("Testing")
	output.set_attachments()
	for key, value in request.form.items():
		output.add_attachment(key, value)
	return jsonify(output.response)

@app.route('/random', methods=['GET', 'POST'])
def get_random():
	choices = SlackParser(request.form).get()
	selected = random.choice(choices)

	output = SlackOutput(text=selected)
	return jsonify(output.response)

@app.route('/libor', methods=['GET'])
def get_libor():
	html = get_libor_page()
	titles, rows = parse_libor_page(html)

	output = LiborOutput()

	resp = output.generate(titles, rows)

	return jsonify(resp)
