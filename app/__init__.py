from flask import Flask, render_template, request, redirect, jsonify, after_this_request
from flask_cors import CORS
from app.trajectory import *
from app.esp import *

esp_addr = ''
data = {}
app = Flask(__name__, 
			static_url_path='', 
			static_folder='static',
			template_folder="templates")
CORS(app)

@app.route('/esp')
def esp():
	return esp_simulation()

@app.route('/api/esp')
def api_esp():
	global data
	data = esp_parse(esp_addr)
	return jsonify(data)



@app.route('/time')
def time():
	global data
	data = esp_parse(esp_addr)
	return render_template('time.html', time=data['time'])



@app.route('/api/tracking/<int:norad>')
def api_tracking_prn(norad):
	res = jsonify(get_trajectory(norad))
	res.headers.add("Access-Control-Allow-Origin", "*")
	return res

@app.route('/tracking/<int:norad>')
def tracking_norad(norad):
	return render_template('tracking.html', norad=norad)

@app.route('/tracking')
def tracking():
	global data
	if (not data):
		data = esp_parse(esp_addr)
	prn_norad = get_norad(data)
	print (prn_norad)
	return render_template('tracking_menu.html', prn_norad=prn_norad)



@app.route('/settings', methods = ['POST', 'GET'])
def settings():
	global esp_addr
	if request.method == 'POST':
		esp_addr = request.form['ip']
		return redirect('/')
	else:
		return render_template('settings.html')

@app.route('/')
def home():
	global esp_addr
	if (esp_addr == ''):
		return redirect('/settings')
	return render_template('index.html')
