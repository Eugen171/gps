import ephem
import numpy as np
import math
import spacetrack.operators as op

import requests
from bs4 import BeautifulSoup

from datetime import datetime, date, timedelta
from spacetrack import SpaceTrackClient

username = 'Jhenyaik3d@yandex.ru'
password = 'Donttouchthis!7'

def get_norad(data):
	out = []
	html_text = requests.get('https://www.n2yo.com/satellites/?c=20').text
	soup = BeautifulSoup(html_text, 'lxml')
	table = soup.find(id='categoriestab')
	table = table.find_all('tr')[1:-1]
	for row in table:
		cols = row.find_all('td')
		prn = int(cols[5].text)
		nor = int(cols[1].text)
		if (prn in data['prn']):
			out.append({'prn': prn, 'norad': nor})
	return (out)

if __name__ == '__main__':
	print (get_norad ({
		"prn": [14, 23, 18],
		"time": "time",
		"rec": "rec",
	}))

def get_spacetrack_tle(sat_id, username, password, latest=False):
	st = SpaceTrackClient(identity=username, password=password)
	data = st.tle_latest(norad_cat_id=sat_id, orderby='epoch desc', limit=1, format='tle')
	if not data:
		return 0, 0
	tle_1 = data[0:69]
	tle_2 = data[70:139]
	return tle_1, tle_2
 
def create_orbital_track(sat_id, step_minutes):
	# TODO find NORAD id by PRN
	tle_1, tle_2 = get_spacetrack_tle(sat_id, username, password, True)
	if not tle_1 or not tle_2:
		return ([])
	num_timestamp = 1440 // 5
	utc_hh = np.zeros((num_timestamp, 1))
	utc_mm = np.zeros((num_timestamp, 1))
	utc_ss = np.zeros((num_timestamp, 1))
	coordinates = []
	p = [];

	i = 0
	minutes = 0
	while minutes < 1440:
		utc_hour = int(minutes // 60)
		utc_minutes = int((minutes - (utc_hour * 60)) // 1)
		utc_seconds = int(round((minutes - (utc_hour * 60) - utc_minutes) * 60))
		utc_hh[i] = utc_hour
		utc_mm[i] = utc_minutes
		utc_ss[i] = utc_seconds

		now = datetime.now()
		utc_string = str(utc_hour) + '-' + str(utc_minutes) + '-' + str(utc_seconds)
		utc_time = datetime(now.year, now.month, now.day, utc_hour, utc_minutes, utc_seconds)

		tle_rec = ephem.readtle('GPS', tle_1, tle_2);
		tle_rec.compute(utc_time);

		longitude = tle_rec.sublong * 180 / math.pi
		latitude  = tle_rec.sublat * 180 / math.pi
		n = [longitude, latitude]
		if (p and n[0] > p[0]):
			coordinates.append([p, n])
		p = n;
		i += 1
		minutes += step_minutes
	return {
		"type": "FeatureCollection",
		"features": [
			{
				"type": "Feature",
				"properties": {
					"id": 0
				},
				"geometry": {
					"type": "Point",
					"coordinates": [65.390625, 61.60639637138628],
				},
			},
			{
				"type": "Feature",
				"properties": {
					"id": 1
				},
				"geometry": {
					"type": "MultiLineString",
					"coordinates": coordinates,
				},
			},
		],
	}


def get_trajectory(data):
	# TODO get norad by prn and paste here --+
	#                          v-------------+
	# return create_orbital_track(prn, 5)
	features = []
	for i in range(0, len(data['satellites'])):
		features.append({
			"type": "Feature",
			"properties": {
				"id": i,
			},
			"geometry": {
				"type": "Point",
				"coordinates": [
					data['satellites'][i]["lon"],
					data['satellites'][i]["lat"],
				],
			},
		})

	return {
		"type": "FeatureCollection",
		"features": features,
	}