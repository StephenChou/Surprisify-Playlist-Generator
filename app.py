from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import os
from spotify_actions import req_auth, req_token, generate
from flask_sqlalchemy import SQLAlchemy
from whitenoise import WhiteNoise

'''

App Config

'''


app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET')
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')

# db config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_REDIRECT_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# database
db = SQLAlchemy(app)
db.app = app


class users(db.Model):
    spotify_id = db.Column(db.String(50), primary_key=True)
    playlist_id = db.Column(db.String(40), unique=True, nullable=False)
    first_name = db.Column(db.String(20), unique=False, nullable=True)

    def __init__(self, usr_id, pl_id, f_name):
        self.spotify_id = usr_id
        self.playlist_id = pl_id
        self.first_name = f_name


'''

Views

'''


# Home view
@app.route('/')
@app.route('/home')
def home():

    # Home page
    return render_template('home.html', title='Home')


# Login view


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    # Redirect user to Spotify login page
    AUTH_FIRST = req_auth()
    return redirect(AUTH_FIRST)


# Callback view for Spotify API


@app.route('/callback')
def callback():
    if request.args.get('error') or not request.args.get('code'):

        # Prevents user from accessing page without going through authorization
        # steps properly
        return redirect(url_for('home'))
    else:
        # Get 'code' from Spotify request
        code = request.args.get('code')

        # Using 'code' provided by Spotify, request a user token from Spotify
        token = req_token(code)
        session['token'] = token

        return redirect('https://www.surprisify.me/generate_playlist')


# Generate playlist view


@app.route('/generate_playlist', methods=['GET', 'POST'])
def generate_playlist():

    if request.method == 'POST':

        # Get custom playlist name and description from jquery post request
        pl_name = session.get('pl_name')
        pl_desc = session.get('pl_desc')

        # Get user input level from post request
        level = int(float(request.form.get('level')))

        # Using token from earlier, generate playlist
        token = session.get('token')
        user_info = generate(token, level, pl_name, pl_desc)

        user_first_name = str(user_info[0])
        user_spotify_id = str(user_info[1])
        user_playlist_id = str(user_info[2])

        # Store playlist ID in session
        session['user_pl_id'] = user_playlist_id

        found_user = users.query.filter_by(spotify_id=user_spotify_id).first()

        if found_user:
            found_user.playlist_id = user_playlist_id
            db.session.commit()

        else:
            user = users(user_spotify_id, user_playlist_id, user_first_name)
            db.session.add(user)
            db.session.commit()

        return redirect(url_for('success'))

    else:
        if session.get('token'):
            session.pop('pl_name', None)
            session.pop('pl_desc', None)

            # Load playlist generator page
            return render_template('generate_playlist.html', title='generate playlist')
        else:

            # Return home if user attempts to access page without going through
            # proper authorization
            return redirect(url_for('home'))


# Update modal form (backend page)


@app.route('/update', methods=["GET", "POST"])
def update():

    if request.method == 'POST':

        # Get custom playlist name from jquery post
        pl_name = request.form.get('name')
        pl_desc = request.form.get('desc')

        # Store custom info into session
        session['pl_name'] = pl_name
        session['pl_desc'] = pl_desc

        return jsonify({'result': 'success'})

    if request.method == 'GET':
        return redirect(url_for('home'))


# Success landing page


@app.route('/success')
def success():

    if session.get('user_pl_id'):
        playlist_id = session.get('user_pl_id')
        return render_template('success.html', pl_id=playlist_id)
    else:
        return redirect(url_for('home'))


# Success landing page


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


if __name__ == '__main__':
    app.run(debug=False)
