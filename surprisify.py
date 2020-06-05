from flask import Flask, escape, request, render_template, redirect, url_for, session
import subprocess
from dotenv import load_dotenv
import requests
import sys
import os
import json
from os.path import join, dirname
from spotify_actions import req_auth, req_token, generate

app = Flask(__name__, static_folder='/Users/stephenchou/Desktop/Stephen/Programming/PersonalProjects/flask/surprisify/static')
app.secret_key = os.environ.get('SESSION_SECRET')

#Home view
@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', title='Home')

#Login view
@app.route('/login', methods=['GET','POST'])
def login():

	AUTH_FIRST = req_auth()
	return redirect(AUTH_FIRST)

#Callback view for Spotify API
@app.route('/callback')
def callback():
	if request.args.get('error') or not request.args.get('code'):
		return redirect(url_for('home'))
	else:
		code = request.args.get('code')
		token = req_token(code)
		session['token'] = token

		return redirect(url_for('generate_playlist'))

#Generate playlist view
@app.route('/generate_playlist', methods=['GET', 'POST'])
def generate_playlist():

	if request.method == 'POST':
		levels = int(float(request.form['level']))
		token = session.get("token", None)
		generate(token, levels)

		return redirect(url_for('success'))

	else:
		if session.get('token'):
			return render_template('generate_playlist.html', title='generate playlist')
		else:
			return redirect(url_for('home'))

@app.route('/success')
def success():
	return render_template('success.html', title='success')

if __name__ == '__main__':
	app.run(debug=True)
	app.config.from_object('config.DevelopmentConfig')
	
	
