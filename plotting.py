from bokeh.plotting import figure, output_file, show, save
from bokeh.models import ColumnDataSource, DatetimeTicker
from bokeh.palettes import Paired12 as palette
from bokeh.layouts import column
from datetime import timedelta
import pandas as pd
import itertools
import utils


def plot_odds_winner(db_, team_home, team_away):
    """
    Retrieves match directly from the db, creates a dataframe of odds and plots odds over time.

    todo: creating the dataframe should be done in a different function
    """

    # Retrieve match from database
    m = db_.matches.find_one({'team_home': team_home, 'team_away': team_away})
    if m is None:
        return None

    # Create a dataframe of match odds
    df = utils.create_odds_df(m)

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

    colors = itertools.cycle(palette)

    # output to static HTML file
    title = "%s | %s - %s | %s" % (str(m['match_datetime']), m['team_home'], m['team_away'], m['result']['score'])
    output_file("templates/winner_timeseries.html", title="Odds %s - %s" %(team_home, team_away))

    f1 = figure(title="Home win | %s" % title, x_axis_type="datetime", x_axis_label='Time', y_axis_label='Odd', plot_width=900, plot_height=350)
    f2 = figure(title="Draw | %s" % title, x_axis_type="datetime", x_axis_label='Time', y_axis_label='Odd', plot_width=900, plot_height=350)
    f3 = figure(title="Away win | %s" % title, x_axis_type="datetime", x_axis_label='Time', y_axis_label='Odd', plot_width=900, plot_height=350)

    for filter_, bookie, color in zip(filters, bookies_to_plot, colors):
        source = ColumnDataSource(df[filter_])
        f1.line('datetime', '1', legend=bookie, color=color, line_width=2, source=source, alpha=0.8)
        f1.circle('datetime', '1', color=color, source=source)
        f2.line('datetime', '0', legend=bookie, color=color, line_width=2, source=source, alpha=0.8)
        f2.circle('datetime', '0',color=color, source=source)
        f3.line('datetime', '2', legend=bookie, color=color, line_width=2, source=source, alpha=0.8)
        f3.circle('datetime', '2',color=color, source=source)

    f1.xaxis.ticker = DatetimeTicker(desired_num_ticks=15)
    f2.xaxis.ticker = DatetimeTicker(desired_num_ticks=15)
    f3.xaxis.ticker = DatetimeTicker(desired_num_ticks=15)

    f1.legend.location = "top_left"
    f2.legend.location = "top_left"
    f3.legend.location = "top_left"
    save(column(f1, f2, f3))

    return True


def plot_odds_goals(db_, team_home, team_away):
    """
    Retrieves match from db, creates a dataframe of odds and plots odds over time.

    todo: creating the dataframe should be done in a different function
    """

    # Retrieve match from database
    m = db_.matches.find_one({'team_home': team_home, 'team_away': team_away})
    if m is None:
        return None

    df = utils.create_odds_df(m)

    # Filter over the following bookies
    # todo: get them from a config file
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

    colors = itertools.cycle(palette)

    # output to static HTML file
    title = "%s | %s - %s | %s" % (str(m['match_datetime']), m['team_home'], m['team_away'], m['result']['score'])
    output_file("templates/goals_timeseries.html", title="Odds %s - %s" %(team_home, team_away))

    # create a new plot with a title and axis labels
    f1 = figure(title="Over 2.5 | %s" % title, x_axis_type="datetime", x_axis_label='Time', y_axis_label='Odd', plot_width=900, plot_height=350)
    f2 = figure(title="Under 2.5 | %s" % title, x_axis_type="datetime", x_axis_label='Time', y_axis_label='Odd', plot_width=900, plot_height=350)

    for filter_, bookie, color in zip(filters, bookies_to_plot, colors):
        source = ColumnDataSource(df[filter_])
        f1.line('datetime', 'over2_5', legend=bookie, color=color, line_width=2, source=source, alpha=0.8)
        f1.circle('datetime', 'over2_5', color=color, source=source)
        f2.line('datetime', 'under2_5', legend=bookie, color=color, line_width=2, source=source, alpha=0.8)
        f2.circle('datetime', 'under2_5',color=color, source=source)

    f1.xaxis.ticker = DatetimeTicker(desired_num_ticks=15)
    f2.xaxis.ticker = DatetimeTicker(desired_num_ticks=15)
    f1.legend.location = "top_left"
    f2.legend.location = "top_left"
    save(column(f1,f2))
    return True


# def plot_odds_goals(db_, home_team, away_team):
#     """
#     Retrieves match from db, creates a dataframe of odds and plots odds over time.
#
#     """
#
#     import matplotlib.pyplot as plt
#
#     # Retrieve match from database
#     m = db_.matches.find_one({'team_home': home_team, 'team_away': away_team})
#     if m is None:
#         return "Match not found"
#
#     # Create a dataframe of match odds
#     df = pd.DataFrame()
#     winner = m['all_odds']['total_goals']
#     odds2 = []
#     for odds in winner:
#         for odd in odds['odds']:
#             odd['datetime'] = odds['datetime']
#             odds2.append(odd)
#     df = pd.DataFrame(odds2, columns=['datetime', 'over2_5', 'under2_5','bookie'])
#     df['over2_5'] = df['over2_5'].astype('float32')
#     df['under2_5'] = df['under2_5'].astype('float32')
#     df['bookie'] = df['bookie'].astype('str')
#
#     # Filter over the following bookies
#     bookies_to_plot = ['Bet 365',
#                        'Sky Bet',
#                        'Ladbrokes',
#                        "William Hill",
#                        "Marathon Bet",
#                        "Betfair Sportsbook",
#                        "SunBets",
#                        "Paddy Power",
#                        "Unibet",
#                        "Coral",
#                        "Betfred",
#                        "Bet Victor"]
#     filters = [(df.bookie == "Bet 365") | (df.bookie == "Bet365"),
#           (df.bookie == "Sky Bet") | (df.bookie == "Skybet"),
#           (df.bookie == "Ladbrokes"),
#           (df.bookie == "William Hill"),
#           (df.bookie == "Marathon Bet"),
#           (df.bookie == "Betfair Sportsbook"),
#           (df.bookie == "SunBets"),
#           (df.bookie == "Paddy Power"),
#           (df.bookie == "Unibet"),
#           (df.bookie == "Coral"),
#           (df.bookie == "Betfred"),
#           (df.bookie == "Bet Victor")]
#
#     # Plot
#     fig, ax = plt.subplots(2, 1, figsize=(15,10))
#     fig.fig_size = (22,10)
#     for filter_, bookie in zip(filters, bookies_to_plot):
#         ax[0].plot(df[filter_].datetime, df[filter_]['over2_5'], 'o-', label=bookie)
#         ax[0].set_title("Over 2.5")
#         ax[1].plot(df[filter_].datetime, df[filter_]['under2_5'], 'o-', label=bookie)
#         ax[1].set_title("Under 2.5")
#     ax[0].legend(loc='lower left')
#     ax[1].legend(loc='lower left')
#     fig.suptitle("%s | %s - %s | %s" % (str(m['match_datetime']), m['team_home'], m['team_away'], m['result']['score']), fontsize=16)
#     plt.show()
#     print("Last odds collected at: %s" % df[filter_].datetime.iloc[-1])


if __name__ == "__main__":
    db = utils.connect_db(remote=True)
    # plot_odds_goals_bokeh(db, "Atalanta", "Inter Milan")
    m = db.matches.find_one({'team_home': "Atalanta", 'team_away': "Inter Milan"})
    res = utils.create_odds_df(m)
    print(res.head(5))