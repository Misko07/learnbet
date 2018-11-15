from datetime import timedelta
import pandas as pd
import pymongo
import json


def connect_db(remote=False):
    """
    Connects to learnbet database and returns the database object.

    If remote=True this method will connect to the live database on the aws server.
    Work carefully with it, db is live.
    """

    if remote:
        print("Connecting to remote db..")
        with open("db_credentials_remote.json", "r") as file:
            db_config = json.load(file)
    else:
        with open("db_credentials.json", "r") as file:
            db_config = json.load(file)

    uri = 'mongodb://%s:%s@%s/%s' % \
          (db_config['username'],
           db_config['password'],
           db_config['DB_IP'],
           db_config['DB_name'])

    client = pymongo.MongoClient(uri)
    db = client.get_database()

    return db


def create_odds_df(m_dict):
    """
    Create a dataframe for total goals and winner odds.

    :param match: A diction ary, as retrieved from the db
    :return: Pandas dataframe with columns: ['datetime', '1', '2', '0', 'over2_5', 'under2_5', 'bookie']
    """

    if m_dict is None:
        return None

    winners = m_dict['all_odds']['winner'].copy()
    goals = m_dict['all_odds']['total_goals'].copy()
    winner_dates = [item['datetime'] for item in winners]
    goals_dates = [item['datetime'] for item in goals]

    # A list of distinct datetimes for both winner and total_goals
    dates_unique = winner_dates.copy()
    for goal_date in goals_dates:
        found = False
        for date in dates_unique:
            if abs(date - goal_date) < timedelta(minutes=3):
                found = True
                break
        if not found:
            dates_unique.append(goal_date)

    # Go through all unique dates
    rows = []
    for date in dates_unique:

        winner_odds_list = None
        for winner_list in winners:
            if abs(winner_list['datetime'] - date) < timedelta(minutes=3):
                winner_odds_list = winner_list['odds']

        goals_odds_list = None
        for goals_list in goals:
            if abs(goals_list['datetime'] - date) < timedelta(minutes=3):
                goals_odds_list = goals_list['odds']

        # Now we have two lists of winner and goals odds for the same datetime

        # Create a list of unique bookies on that datetime
        bookies_unique = [item['bookie'] for item in winner_odds_list]
        for goals_odd in goals_odds_list:
            if goals_odd['bookie'] not in bookies_unique:
                bookies_unique.append(goals_odd['bookie'])

        # Go through bookies in the unuque list
        for bookie in bookies_unique:
            row = {'datetime': date, '1': None, '2': None, '0': None, 'over2_5': None, 'under2_5': None,
                   'bookie': bookie}

            # If bookie found in goals_odds_list add some data to row
            for goals_odd in goals_odds_list:
                if bookie == goals_odd['bookie']:
                    row['over2_5'] = goals_odd['over2_5']
                    row['under2_5'] = goals_odd['under2_5']
                    break

            # If bookie found in winner_odds_list add some data to row
            for winner_odd in winner_odds_list:
                if bookie == winner_odd['bookie']:
                    row['1'] = winner_odd['1']
                    row['2'] = winner_odd['2']
                    row['0'] = winner_odd['0']
                    break

            # Append line to the list of lines
            rows.append(row)

    df = pd.DataFrame(rows, columns=['datetime', '1', '0', '2', 'over2_5', 'under2_5', 'bookie'])
    df['over2_5'] = df['over2_5'].astype('float32')
    df['under2_5'] = df['under2_5'].astype('float32')
    df['1'] = df['1'].astype('float32')
    df['0'] = df['0'].astype('float32')
    df['2'] = df['2'].astype('float32')
    df['bookie'] = df['bookie'].astype('str')
    return df


def get_scheduled_matches():
    db = connect_db(remote=True)
    ms = db.matches.find({ "$query": {'status': 'scheduled'}, "$orderby": {"match_datetime": 1}})
    match_list = []
    for m in ms:
        del m['odds_link']
        del m['all_odds']
        del m['result']
        del m['team_home_last6']
        del m['team_away_last6']
        del m['_id']
        match_list.append(m)
    return match_list


if __name__ == "__main__":
    ms = get_scheduled_matches()
    print(len(ms))
    print(ms[:2])

    # db = connect_db(remote=True)
    # m = db.matches.find_one({'team_home': "Atalanta", 'team_away': "Inter Milan"})
    # res = create_odds_df(m)
    # print(res.head(5))
