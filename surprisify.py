from flask import Flask, escape, request, render_template, redirect, url_for, session
# from spotify_api_copy import authenticate1
import subprocess
import sys
import os
from authenticate import authenticate, generate


app = Flask(__name__, static_folder='/Users/stephenchou/Desktop/PersonalProjects/flask/surprisify/static')
app.secret_key = os.environ.get("SESSION_SECRET")

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/login', methods=['GET','POST'])
def login():

	if request.method == 'GET':
		tokenAuth = authenticate()
		session["token"] = tokenAuth
		return redirect(url_for('generate_playlist'))

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
	return '<h1>Success! Check your Spotify playlists for a generated playlist!</h1>'

if __name__ == '__main__':
	app.run(debug=True)
	
	
