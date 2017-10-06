from flask import Flask, jsonify
from bs4 import BeautifulSoup
import urllib2
app = Flask(__name__)

@app.route('/aaron/libor', methods=['GET'])
def get_libor():
	r = urllib2.urlopen('http://www.wsj.com/mdc/public/page/2_3020-libor.html?mod=mdc_bnd_pglnk')
	html = r.read()
	soup = BeautifulSoup(html)
	
	table = soup.find("table", {"class":"mdcTable"})
	rows = table.findChildren(['tr'])

	capture = False
	libor_list = []
	for row in rows:
		cells = row.findChildren(['td'])
		libor_row = []
		for cell in cells:
			value = cell.string
			if value == 'Libor Rates (USD)':
				capture = True
			if value is None or value == "\\n":
				capture = False
			if capture == True:
				libor_row.append(value)
		if libor_row:
			libor_list.append(libor_row)

	titles = libor_list[0]

	colors = ['439FE0','ff5050']

	resp = {'response_type':'in_channel'}
	resp['attachments'] = []
	for lrow in libor_list[1:]:
		print  lrow[0]
		if lrow[0] == 'Libor 1 Month' or lrow[0] == 'Libor 1 Year':
			try:
				attch_row = {
					'title' : lrow[0],
					'fields' : [
						{
							"title": titles[1],
							"value": lrow[1],
							"short": True
						},
						{
							"title": titles[2],
							"value": lrow[2],
							"short": True
						},
						{
							"title": "52 Week " + titles[3],
							"value": lrow[3],
							"short": True
						},
						{
							"title": "52 Week " + titles[4],
							"value": lrow[4],
							"short": True
						}
					],
					'color' : colors.pop()
				}
				resp['attachments'].append(attch_row)
			except Exception, e:
				pass

	resp['text'] = titles[0]
	return jsonify(resp)
