from flask import Flask, render_template, request, redirect, jsonify
from app.trajectory import *
from app.esp import *

esp_addr = '';

app = Flask(__name__, 
            static_url_path='', 
            static_folder='static',
            template_folder="templates")

@app.route('/esp')
def esp():
    return esp_simulation()

@app.route('/api/esp')
def api_esp():
    return jsonify(esp_parse(esp_addr))

@app.route('/api/tracking/<int:prn>')
def api_tracking_prn(prn):
    return jsonify(trajectory.get_trajectory(prn))

@app.route('/tracking/<int:prn>')
def tracking_prn(prn):
    return render_template('tracking.html', prn=prn)

@app.route('/api/tracking')
def api_tracking():
    return "json list of sattelites" # TODO

@app.route('/tracking')
def tracking():
    return "table of sattelites" # TODO

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
