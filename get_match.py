import footmldb as db_
import argparse
from datetime import datetime
import pprint
pp = pprint.PrettyPrinter(indent=4)


def get_match(args_):

    date_ = None
    if args_.date:
        date_ = datetime.strptime(args_.date, "%d/%m/%y")
    match = db_.get_match(args_.team_home, args_.team_away, date_)
    return match


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get match for given home and away teams.")

    # Add positional arguments
    parser.add_argument('team_home', help='Team home', type=str)
    parser.add_argument('team_away', help='Team away', type=str)

    # Add optional arguments
    parser.add_argument('-d', '--date', help="Match date dd/mm/yyyy", type=str)

    # args = parser.parse_args(['-d', '12/03/2018', 'inter', 'win'])
    args = parser.parse_args()

    match = get_match(args)
    pp.pprint(match)

