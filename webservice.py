from datetime import datetime
import plotting
import pymongo
import flask
import utils
import json


app = flask.Flask(__name__)


@app.route("/winner_odds", methods=["GET", "POST"])
def get_winner_odds():

    # Check both request.json and request.args
    # Depending on how the function is called (eg. browser get vs curl post)
    params = flask.request.json
    if params is None:
        params = flask.request.args

    if params:
        team_home = params.get("team_home")
        team_away = params.get("team_away")

    if team_home and team_away:
        db_ = utils.connect_db(remote=True)
        result = plotting.plot_odds_winner(db_, team_home, team_away)
        if result:
            return flask.render_template('winner_timeseries.html')
        return "Match %s - %s not found!" % (team_home, team_away)

    return "Match %s - %s not found!" % (team_home, team_away)


@app.route("/goals_odds", methods=["GET", "POST"])
def get_goals_odds():

    # Check both request.json and request.args
    # Depending on how the function is called (eg. browser get vs curl post)
    params = flask.request.json
    if params is None:
        params = flask.request.args

    if params:
        team_home = params.get("team_home")
        team_away = params.get("team_away")

    if team_home and team_away:
        db_ = utils.connect_db(remote=True)
        result = plotting.plot_odds_goals(db_, team_home, team_away)
        if result:
            return flask.render_template('goals_timeseries.html')
        return "Match %s - %s not found!" % (team_home, team_away)

    return "Match %s - %s not found!" % (team_home, team_away)


@app.route("/next_matches", methods=["GET", "POST"])
def get_next_matches():

    results = {}
    results['success'] = False
    ms = utils.get_scheduled_matches()
    if len(ms) > 0:
        results['success'] = True
        results['matches'] = ms
        return flask.jsonify(results)
    return "No scheduled matches."


@app.route('/teams/<team>')
def show_team_matches(team):
    # todo: retrieve all matches for <team>
    return "Team %s" % team


@app.route('/')
def index():
    return flask.render_template('webpage1.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # get_goals_odds("Croatia", "Spain")
