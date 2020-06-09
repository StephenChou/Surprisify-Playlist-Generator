from flask import Flask, request, render_template, redirect, url_for, session
import os
from spotify_actions import req_auth, req_token, generate
from whitenoise import WhiteNoise

'''

App Config

'''


app = Flask(__name__)
app.secret_key = os.urandom(16)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')


if app.config['ENV'] == 'development':
    app.config.from_object('config.DevelopmentConfig')

elif app.config['ENV'] == 'testing':
    app.confgi.from_object('config.TestingConfig')

else:
    app.config.from_object('config.ProductionConfig')

'''

Views

'''


# Home view
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

# Login view


@app.route('/login', methods=['GET', 'POST'])
def login():

    AUTH_FIRST = req_auth()
    return redirect(AUTH_FIRST)

# Callback view for Spotify API


@app.route('/callback')
def callback():
    if request.args.get('error') or not request.args.get('code'):
        return redirect(url_for('home'))
    else:
        code = request.args.get('code')
        token = req_token(code)
        session['token'] = token

        return redirect(url_for('generate_playlist'))

# Generate playlist view


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

# Success landing page


@app.route('/success')
def success():
    return render_template('success.html', title='success')

# Success landing page


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


if __name__ == '__main__':
    app.run()
