from flask import Flask, render_template, request, redirect, jsonify
from app.trajectory import *
from app.esp import *

esp_addr = '';
data = {}
app = Flask(__name__, 
			static_url_path='', 
			static_folder='static',
			template_folder="templates")

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



@app.route('/api/tracking')
def api_tracking_prn():
	global data
	if (not data):
		data = esp_parse(esp_addr)
	ans = trajectory.get_trajectory(data)
	return jsonify(ans)

@app.route('/tracking')
def tracking():
	global data
	if (not data):
		data = esp_parse(esp_addr)
	#return render_template('tracking_menu.html', stl=data['satellites'])
	return render_template('tracking.html')



@app.route('/api/noise/<int:prn>')
def api_noise_prn(prn):
	global data
	if (not data):
		data = esp_parse(esp_addr)
	for st in data['satellites']:
		if (st['prn'] == prn):
			return str(st['nse'])
	return '0';

@app.route('/noise/<int:prn>')
def noise_prn(prn):
	return render_template('noise.html', prn=prn)

@app.route('/noise')
def noise():
	global data
	if (not data):
		data = esp_parse(esp_addr)
	return render_template('noise_menu.html', stl=data['satellites'])



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
