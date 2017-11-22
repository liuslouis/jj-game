
from flask import Flask, render_template, session, request, jsonify, redirect, \
    Response, url_for
from flask_login import LoginManager, UserMixin, current_user, login_user, \
    logout_user
from flask_session import Session
from flask_socketio import SocketIO, emit

from utils import format_cards
from jj import Game


app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'top-secret!'
app.config['SESSION_TYPE'] = 'filesystem' # redis
login = LoginManager(app)
Session(app)
socketio = SocketIO(app, manage_session=False)

################################################################################
# User & Session of User:
#   * Locally, every login logout --> single username in a session
#   * Globally, every login logout --> single user object in a user heap
#   * TODO: At every login, authorize the users with player handler id
################################################################################

app.current_user_ids = set([])
app.current_user_info = {}

def game_login_current_user():
    app.current_user_ids.add(current_user.id)
    if current_user.id not in app.current_user_info:
        tmp = len(app.current_user_ids)-1
        app.current_user_info[current_user.id] = [0+tmp, 2+tmp, 4+tmp]
        print('Someone Logged in:', app.current_user_info)

def game_logout_current_user():
    app.current_user_ids.remove(current_user.id)
    app.current_user_info.pop(current_user.id)
    print('Someone Logged out:', app.current_user_info)

class User(UserMixin, object):
    def __init__(self, id=None):
        self.id = id


@login.user_loader
def load_user(id):
    return User(id)


@app.route('/session', methods=['GET', 'POST'])
def session_access():
    if request.method == 'GET':
        return jsonify({
            'session': session.get('value', ''),
            'user': current_user.id
                if current_user.is_authenticated else 'anonymous'
        })
    data = request.get_json()
    if 'session' in data:
        session['value'] = data['session']
    elif 'user' in data:
        if data['user']:
            login_user(User(data['user']))
            game_login_current_user()
        else:
            game_logout_current_user()
            logout_user()
    return '', 204


@socketio.on('get-session')
def get_session():
    emit('refresh-session', {
        'session': session.get('value', ''),
        'user': current_user.id
            if current_user.is_authenticated else 'anonymous'
    })

################################################################################
# Game Play: View Section
################################################################################

#app.gamecards = ['As1', '8c4', '+j1']
app.g = Game()
@socketio.on('init')
def restart():
    app.g = Game()
    print('\nStart a new game.')
    emit('next-round', broadcast=True)


@app.route('/')
def refresh():

    is_authenticated = current_user.is_authenticated
    if not is_authenticated:
        return render_template('sessions.html', is_authenticated=is_authenticated)

    # Only authenticated user comes to the following lines
    g = app.g
    # an authenticated user is correctly logged in the game
    if current_user.id not in app.current_user_ids:
        game_login_current_user()

    info = {}
    user_playerids = app.current_user_info[current_user.id]#[0, 2, 4]
    oppo_playerids = [0, 1, 2, 3, 4, 5]
    info['user_players'] = []
    info['oppo_players'] = []
    info['round_player'] = g.get_round_player_id()
    info['round_cards'] = format_cards(g.get_table()[1])
    info['round_last'] = g.get_table()[0]

    for i in user_playerids:
        player = {}
        player['id'] = i
        player['cards'] = format_cards(g.get_cards(i))
        info['user_players'].append(player)

    for j in oppo_playerids:
        player = {}
        player['id'] = j
        player['cnt'] = g.get_ncards(j)
        info['oppo_players'].append(player)

    #print(url_for('static', filename='cards.css'))

    return render_template('sessions.html', is_authenticated=is_authenticated,
                           value=app.count, **info)

################################################################################
# Game Play: Control Section
################################################################################

app.count = 0

@app.route('/send', methods=['POST'])
def update():
    form = request.form.to_dict()

    round_player_id = int(form.pop('playerid'))
    cards = list(form.keys())
    app.count += 1

    ###
    g = app.g
    round_status = g.play(round_player_id, cards)
    ###
    return Response('success', status=200)

@socketio.on('ready4next')
def send_next():
    print('Broadcast Next Round.\n')
    emit('next-round', broadcast=True)



if __name__ == '__main__':
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    socketio.run(app, host='0.0.0.0', port=7777, log_output=False)
