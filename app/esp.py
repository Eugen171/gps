import pynmea2
import requests
import pymap3d as pm

dataarr = [
'''$GPGGA,160047.00,5545.78247,N,04909.98722,E,1,06,2.14,102.0,M,-0.6,M,,*4C
$GPGSA,A,3,23,10,15,32,18,24,,,,,,,2.98,2.14,2.07*09
$GPGSV,3,1,11,08,47,282,,10,84,116,31,14,06,352,18,15,12,042,22*7E
$GPGSV,3,2,11,18,19,117,34,21,21,295,,23,49,073,36,24,18,073,31*73
$GPGSV,3,3,11,27,50,225,20,28,00,005,,32,33,172,39*4E
$GPGLL,5545.78247,N,04909.98722,E,160047.00,A,A*60
$GPRMC,160048.00,A,5545.78249,N,04909.98723,E,0.516,,180521,,,A*74
$GPVTG,,T,,M,0.516,N,0.956,K,A*2B''',
'''$GPGGA,160048.00,5545.78249,N,04909.98723,E,1,06,2.14,101.9,M,-0.6,M,,*46
$GPGSA,A,3,23,10,15,32,18,24,,,,,,,2.98,2.14,2.07*09
$GPGSV,3,1,11,08,47,282,,10,84,116,31,14,06,352,18,15,12,042,21*7D
$GPGSV,3,2,11,18,19,117,34,21,21,295,,23,49,073,33,24,18,073,31*76
$GPGSV,3,3,11,27,50,225,18,28,00,005,,32,33,172,36*4A
$GPGLL,5545.78249,N,04909.98723,E,160048.00,A,A*60
$GPRMC,160049.00,A,5545.78242,N,04909.98755,E,0.257,,180521,,,A*7D
$GPVTG,,T,,M,0.257,N,0.476,K,A*26''',
'''$GPGGA,160049.00,5545.78242,N,04909.98755,E,1,06,2.14,101.7,M,-0.6,M,,*43
$GPGSA,A,3,23,10,15,32,18,24,,,,,,,2.98,2.14,2.07*09
$GPGSV,3,1,11,08,47,282,,10,84,116,30,14,06,352,17,15,12,042,21*73
$GPGSV,3,2,11,18,19,117,34,21,21,295,,23,49,073,34,24,18,073,31*71
$GPGSV,3,3,11,27,50,225,16,28,00,005,,32,33,172,36*44
$GPGLL,5545.78242,N,04909.98755,E,160049.00,A,A*6B
$GPRMC,160050.00,A,5545.78230,N,04909.98778,E,0.814,,180521,,,A*72
$GPVTG,,T,,M,0.814,N,1.508,K,A*22''',
'''$GPGGA,160050.00,5545.78230,N,04909.98778,E,1,06,2.14,101.6,M,-0.6,M,,*40
$GPGSA,A,3,23,10,15,32,18,24,,,,,,,2.98,2.14,2.07*09
$GPGSV,3,1,11,08,47,282,,10,84,116,29,14,06,352,17,15,12,042,20*7A
$GPGSV,3,2,11,18,19,117,36,21,21,295,,23,49,073,36,24,18,073,34*74
$GPGSV,3,3,11,27,50,225,14,28,00,005,,32,33,172,37*47
$GPGLL,5545.78230,N,04909.98778,E,160050.00,A,A*69
$GPRMC,160051.00,A,5545.78238,N,04909.98764,E,0.282,,180521,,,A*73
$GPVTG,,T,,M,0.282,N,0.522,K,A*2E''',
'''$GPGGA,160051.00,5545.78238,N,04909.98764,E,1,06,2.27,101.6,M,-0.6,M,,*44
$GPGSA,A,3,23,10,15,32,18,24,,,,,,,3.42,2.27,2.56*0B
$GPGSV,3,1,11,08,47,282,,10,84,116,30,14,06,352,17,15,12,042,21*73
$GPGSV,3,2,11,18,19,117,35,21,21,295,,23,49,073,33,24,18,073,33*75
$GPGSV,3,3,11,27,50,225,15,28,00,005,,32,33,172,35*44
$GPGLL,5545.78238,N,04909.98764,E,160051.00,A,A*6D
$GPRMC,160052.00,A,5545.78238,N,04909.98770,E,0.698,,180521,,,A*7A
$GPVTG,,T,,M,0.698,N,1.292,K,A*2C''',
]

i = -1;
def esp_simulation():
	global i, dataarr
	i += 1
	if i >= len(dataarr):
		i = 0
	return (dataarr[i])

def add_gsv(to, data):
	if (not isinstance(data, pynmea2.GSV)):
		return
	if (int(data.num_sv_in_view) > len(to)):
		to.append({
			"prn": int(data.sv_prn_num_1),
			"deg": int(data.elevation_deg_1),
			"azm": int(data.azimuth_1),
			"nse": (int(data.snr_1) if data.snr_1 else 0),
		})
	if (int(data.num_sv_in_view) > len(to)):
		to.append({
			"prn": int(data.sv_prn_num_2),
			"deg": int(data.elevation_deg_2),
			"azm": int(data.azimuth_2),
			"nse": (int(data.snr_2) if data.snr_2 else 0),
		})
	if (int(data.num_sv_in_view) > len(to)):
		to.append({
			"prn": int(data.sv_prn_num_3),
			"deg": int(data.elevation_deg_3),
			"azm": int(data.azimuth_3),
			"nse": (int(data.snr_3) if data.snr_3 else 0),
		})
	if (int(data.num_sv_in_view) > len(to)):
		to.append({
			"prn": int(data.sv_prn_num_4),
			"deg": int(data.elevation_deg_4),
			"azm": int(data.azimuth_4),
			"nse": (int(data.snr_4) if data.snr_4 else 0),
		})

def esp_parse(url, package=''):
	sv = []
	sl = []
	time = ''
	receiver = ''
	if (url == ''):
		url = "localhost:3000/esp"
	if ('http://' not in url):
		url = 'http://' + url
	if (package == ''):
		res = requests.get(url)
		if (not res):
			return ({});
		package = res.text
	for line in package.splitlines():
		try:
			data = pynmea2.parse(line)
			if isinstance(data, pynmea2.GGA):
				receiver = {"lat": float(data.lat) / 100, "lon": float(data.lon) / 100}
			if isinstance(data, pynmea2.RMC):
				time = data.timestamp
			if isinstance(data, pynmea2.GSV):
				add_gsv(sv, data)
		except pynmea2.ParseError as e:
			continue
	return ({
		"satellites": sv,
		"time": str(time),
		"receiver": receiver,
	})

if __name__ == '__main__':
	res = esp_parse('addr', dataarr[0])
	i = 0
	for i in range(0, len(res["satellites"])):
		print(i)
		print(res["satellites"][i])
		print(res["receiver"])
		az = res["satellites"][i]["azm"]
		el = res["satellites"][i]["deg"]
		obs_lat = res["receiver"]["lat"]
		obs_lon = res["receiver"]["lon"]
		aer = (az, el, 1673)
		obslla = (obs_lat, obs_lon, 8876.8)
		lla = pm.aer2geodetic(*aer, *obslla)
		print(lla[1])
		print(lla[0])
		print('')
