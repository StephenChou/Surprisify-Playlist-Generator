from flask import Flask, escape, request, render_template, redirect, url_for, session
import subprocess
from dotenv import load_dotenv
import requests
import sys
import os
from os.path import join, dirname
from authenticate import req_auth, req_token, generate

app = Flask(__name__, static_folder='/Users/stephenchou/Desktop/Stephen/Programming/PersonalProjects/flask/surprisify/static')
dotenv_path = join(dirname(__file__), '.env')



SECRET_KEY = os.environ.get('SESSION_SECRET')
app.secret_key = SECRET_KEY


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', title='Home')


@app.route('/about')
def about():

	return render_template('about.html', title='About')

@app.route('/login', methods=['GET','POST'])
def login():

	AUTH_FIRST = req_auth()
	return redirect(AUTH_FIRST)

@app.route('/callback')
def callback():
	if request.args.get('error'):
		return redirect(url_for('home'))
	else:
		code = request.args.get('code')
		req_token(code)
		return 

@app.route('/generate_playlist', methods=['GET', 'POST'])
def generate_playlist():

	if request.method == 'POST':
		level = request.form['level']
		session["level"] = level
		return redirect(url_for('processing'))

	else:
		return render_template('generate_playlist.html', title='generate playlist')

@app.route('/processing', methods=['GET', 'POST'])
def processing():
	levels = int(float(session.get("level", None)))
	token = session.get("token", None)
	
	generate(token, levels)
	return redirect(url_for('success'))


@app.route('/success')
def success():
	return render_template('success.html', title='success')

if __name__ == '__main__':
	app.run(debug=True)
	app.config.from_object('config.DevelopmentConfig')
	
	
