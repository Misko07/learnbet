import pandas as pd


def plot_odds_goals(db_, home_team, away_team):
    """
    Retrieves match from db, creates a dataframe of odds and plots odds over time.

    todo: creating the dataframe should be done in a different function
    """

    import matplotlib.pyplot as plt

    # Retrieve match from database
    m = db_.matches.find_one({'team_home': home_team, 'team_away': away_team})
    if m is None:
        return "Match not found"

    # Create a dataframe of match odds
    df = pd.DataFrame()
    winner = m['all_odds']['total_goals']
    odds2 = []
    for odds in winner:
#         print(odds)
        for odd in odds['odds']:
            odd['datetime'] = odds['datetime']
            odds2.append(odd)
    df = pd.DataFrame(odds2, columns=['datetime', 'over2_5', 'under2_5','bookie'])
    df['over2_5'] = df['over2_5'].astype('float32')
    df['under2_5'] = df['under2_5'].astype('float32')
    df['bookie'] = df['bookie'].astype('str')

    # Filter over the following bookies
    bookies_to_plot = ['Bet 365',
                       'Sky Bet',
                       'Ladbrokes',
                       "William Hill",
                       "Marathon Bet",
                       "Betfair Sportsbook",
                       "SunBets",
                       "Paddy Power",
                       "Unibet",
                       "Coral",
                       "Betfred",
                       "Bet Victor"]
    filters = [(df.bookie == "Bet 365") | (df.bookie == "Bet365"),
          (df.bookie == "Sky Bet") | (df.bookie == "Skybet"),
          (df.bookie == "Ladbrokes"),
          (df.bookie == "William Hill"),
          (df.bookie == "Marathon Bet"),
          (df.bookie == "Betfair Sportsbook"),
          (df.bookie == "SunBets"),
          (df.bookie == "Paddy Power"),
          (df.bookie == "Unibet"),
          (df.bookie == "Coral"),
          (df.bookie == "Betfred"),
          (df.bookie == "Bet Victor")]

    # Plot
    fig, ax = plt.subplots(2, 1, figsize=(15,10))
    fig.fig_size = (22,10)
    for filter_, bookie in zip(filters, bookies_to_plot):
        ax[0].plot(df[filter_].datetime, df[filter_]['over2_5'], 'o-', label=bookie)
        ax[0].set_title("Over 2.5")
        ax[1].plot(df[filter_].datetime, df[filter_]['under2_5'], 'o-', label=bookie)
        ax[1].set_title("Under 2.5")
    ax[0].legend(loc='lower left')
    ax[1].legend(loc='lower left')
    fig.suptitle("%s | %s - %s | %s" % (str(m['match_datetime']), m['team_home'], m['team_away'], m['result']['score']), fontsize=16)
    plt.show()
    print("Last odds collected at: %s" % df[filter_].datetime.iloc[-1])


def plot_odds_winner(db_, home_team, away_team):
    """
    Retrieves match directly from the db, creates a dataframe of odds and plots odds over time.

    todo: creating the dataframe should be done in a different function
    """

    import matplotlib.pyplot as plt

    # Retrieve match from database
    m = db_.matches.find_one({'team_home': home_team, 'team_away': away_team})
    if m is None:
        return "Match not found"

    # Create a dataframe of match odds
    df = pd.DataFrame()
    winner = m['all_odds']['winner']
    odds2 = []
    for odds in winner:
#         print(odds)
        for odd in odds['odds']:
            odd['datetime'] = odds['datetime']
            odds2.append(odd)
    df = pd.DataFrame(odds2, columns=['datetime', '1', '2', '0', 'bookie'])
    df['1'] = df['1'].astype('float32')
    df['2'] = df['2'].astype('float32')
    df['0'] = df['0'].astype('float32')
    df['bookie'] = df['bookie'].astype('str')

    # Filter over the following bookies
    bookies_to_plot = ['Bet 365',
                       'Sky Bet',
                       'Ladbrokes',
                       "William Hill",
                       "Marathon Bet",
                       "Betfair Sportsbook",
                       "SunBets",
                       "Paddy Power",
                       "Unibet",
                       "Coral",
                       "Betfred",
                       "Bet Victor"]
    filters = [(df.bookie == "Bet 365") | (df.bookie == "Bet365"),
          (df.bookie == "Sky Bet") | (df.bookie == "Skybet"),
          (df.bookie == "Ladbrokes"),
          (df.bookie == "William Hill"),
          (df.bookie == "Marathon Bet"),
          (df.bookie == "Betfair Sportsbook"),
          (df.bookie == "SunBets"),
          (df.bookie == "Paddy Power"),
          (df.bookie == "Unibet"),
          (df.bookie == "Coral"),
          (df.bookie == "Betfred"),
          (df.bookie == "Bet Victor")]

    # Plot
    fig, ax = plt.subplots(3, 1, figsize=(15,10))
    fig.fig_size = (22,10)
    for filter_, bookie in zip(filters, bookies_to_plot):
        ax[0].plot(df[filter_].datetime, df[filter_]['1'], 'o-', label=bookie)
        ax[0].set_title("Home win")
        ax[1].plot(df[filter_].datetime, df[filter_]['0'], 'o-', label=bookie)
        ax[1].set_title("Draw")
        ax[2].plot(df[filter_].datetime, df[filter_]['2'], 'o-', label=bookie)
        ax[2].set_title("Away win")
    ax[0].legend(loc='lower left')
    ax[1].legend(loc='lower left')
    ax[2].legend(loc='lower left')
    fig.suptitle("%s | %s - %s | %s" % (str(m['match_datetime']), m['team_home'], m['team_away'], m['result']['score']), fontsize=16)
    plt.show()
    print("Last odds collected at: %s" % df[filter_].datetime.iloc[-1])

# plot_odds_winner("Sassuolo", "Lazio")