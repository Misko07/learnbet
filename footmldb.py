from difflib import SequenceMatcher
from pymongo import MongoClient
import datetime
import json


def connect_db():
    with open("db_credentials.json", "r") as file:
        db_config = json.load(file)
    uri = 'mongodb://%s:%s@%s/%s' % \
          (db_config['username'], db_config['password'], db_config['DB_IP'], db_config['DB_name'])
    client = MongoClient(uri)
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


def get_match(team_home, team_away, match_datetime=None):
    db_ = connect_db()
    q = _create_match_query(team_home, team_away, match_datetime)
    m = db_.matches.find_one(q)
    return m


if __name__ == '__main__':
    db_ = connect_db()

    query = _create_match_query('Atalanta', 'Inter')

    ms = db_.matches.find(query)

    for m in ms:
        print(m)