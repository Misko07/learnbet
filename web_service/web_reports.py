import flask
from datetime import datetime
import pymongo
import json

app = flask.Flask(__name__)


def _connect_db(remote=False):
    """
    Connects to learnbet database and returns the database object.

    If remote=True this method will connect to the live database on the aws server.
    Work carefully with it, db is live.
    """

    print("Inside connect_db.")
    if remote:
        print("Connecting to remote db..")
        with open("../db_credentials_remote.json", "r") as file:
            db_config = json.load(file)
    else:
        with open("../db_credentials.json", "r") as file:
            db_config = json.load(file)

    uri = 'mongodb://%s:%s@%s/%s' % \
          (db_config['username'],
           db_config['password'],
           db_config['DB_IP'],
           db_config['DB_name'])

    client = pymongo.MongoClient(uri)
    db = client.get_database()

    return db


def _create_match_query(team_home, team_away, match_datetime=None):

    if match_datetime:
        # date_low = match_datetime + datetime.timedelta(hours=-5)
        date_high = match_datetime + datetime.timedelta(hours=24)
        return {'team_home': team_home,
                'team_away': team_away,
                '$and': [{'match_datetime': {'$gt': match_datetime}}, {'match_datetime': {'$lt': date_high}}]}
    else:
        return {'team_home': team_home, 'team_away': team_away}


def _get_match(team_home, team_away, match_datetime=None):
    db_ = _connect_db(remote=True)
    q = _create_match_query(team_home, team_away, match_datetime)
    m = db_.matches.find_one(q)
    return m


@app.route("/get_match", methods=["GET", "POST"])
def get_match():
    match = {"success": False}

    # Check both request.json and request.args
    # Depending on how the function is called (eg. browser get vs curl post)
    params = flask.request.json
    if params == None:
        params = flask.request.args

    if params:
        team_home = params.get("team_home")
        team_away = params.get("team_away")
        match = _get_match(team_home, team_away)

    if not match:
        return "Match not found"

    # Return a response in json format

    match['len_total_goals'] = len(match['all_odds']['total_goals'])
    match['len_winner'] = len(match['all_odds']['winner'])
    del match['all_odds']
    del match['_id']
    match['match_datetime'] = str(match['match_datetime'])
    # del data['match']['od']
    # return str(data['match'].keys())
    # return json.dumps(data, indent=4)
    return flask.jsonify(match)


@app.route('/teams/<team>')
def show_team_matches(team):
    # todo: retrieve all matches for <team>
    return "Team %s" % team


@app.route('/')
def index():
    return flask.render_template('webpage1.html')

app.run(host='0.0.0.0')
