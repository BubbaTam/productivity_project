from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

from config_priv import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, FLASK_SECRET_KEY
from src.utilities import time_at_start_today
from src.data import SpotifyClass
from src.utilities import save_json_file
from config import RAW_DATA_FOLDER


#FLASK_SECRET_KEY = None
#SPOTIFY_CLIENT_ID = None
#SPOTIFY_CLIENT_SECRET = None

flask_app = Flask(__name__)
flask_app.secret_key = FLASK_SECRET_KEY
flask_app.config['SESSION_COOKIE_NAME'] = "person's cookie"
TOKEN_INFO = "token_info"

@flask_app.route("/")
def login():
    """ step 1 on the authorisation code flow"""
    oauth = create_spotify_oauth()
    auth_url = oauth.get_authorize_url()
    # login to spotify to authenticate access rights to spotify recently_played api
    return redirect(auth_url)

@flask_app.route("/redirect")
def redirect_go_to():
    oauth = create_spotify_oauth()
    code = request.args.get('code')
    #save information (refresh token, access token, token_type, expires_in, scope, expires_at)
    token_info = oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    #save information (refresh token,...) to set location
    save_json_file(session[TOKEN_INFO],RAW_DATA_FOLDER,"session_details")
    return redirect(url_for('recently_played', _external=True))

@flask_app.route("/get-recently-played")
def recently_played():
    try:
        token_info = get_token()
    except:
        redirect(url_for("login", _external=False))
    sp = spotipy.Spotify(auth=token_info["access_token"])
    data = sp.current_user_recently_played(limit=50,after=time_at_start_today())
    song_dict = SpotifyClass.extract_spotify_data(data)
    return str(song_dict)


def get_token():
    """ Get new Access Token if current session access token has expired or close to expiration """
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"

    now = int(time.time())
    is_expired = session.get('token_info').get('expires_at') - now < 60
    # boolean if the token has expired or will expire in the next minute
    if is_expired:
        oauth = create_spotify_oauth()
        token_info = oauth.refresh_access_token(session.get('token_info').get('refresh_token'))
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = SPOTIFY_CLIENT_ID,
        client_secret = SPOTIFY_CLIENT_SECRET,
        redirect_uri = url_for('redirect_go_to', _external=True),
        scope = "user-read-recently-played"
    )
