from flask import Flask, escape, request, render_template, redirect, url_for, session
import subprocess
from dotenv import load_dotenv
import sys
import os
from os.path import join, dirname
from authenticate import authenticate, generate


app = Flask(__name__, static_folder='/Users/stephenchou/Desktop/PersonalProjects/flask/surprisify/static')
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


SECRET_KEY = os.environ.get('SESSION_SECRET')
app.secret_key = SECRET_KEY


@app.route('/')
@app.route('/home')
def home():
	print(os.environ)
	return render_template('home.html', title='Home')


@app.route('/about')
def about():

	return render_template('about.html', title='About')

@app.route('/login', methods=['GET','POST'])
def login():

	# if request.method == 'GET':
	# try:	
	tokenAuth = authenticate()

	if tokenAuth:
		session["token"] = tokenAuth
		return redirect(url_for('generate_playlist'))
	else:
		return redirect(url_for('home'));
	# except Exception as e:
	# 	return redirect(url_for('home'))

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
	
	
