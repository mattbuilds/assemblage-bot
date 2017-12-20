import requests
from bs4 import BeautifulSoup

def get_libor_page():
	url = 'http://www.wsj.com/mdc/public/page/2_3020-libor.html?mod=mdc_bnd_pglnk'
	r = requests.get(url)
	return r.text

def parse_libor_page(html):
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

	return libor_list[0], libor_list[1:]
