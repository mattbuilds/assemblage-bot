from flask import Flask, jsonify
from bs4 import BeautifulSoup
from .services import get_libor_page, parse_libor_page
from .output import SlackOutput
app = Flask(__name__)

@app.route('/libor', methods=['GET'])
def get_libor():
	html = get_libor_page()
	titles, rows = parse_libor_page(html)

	output = SlackOutput()

	resp = output.generate(titles, rows)
	
	return jsonify(resp)
