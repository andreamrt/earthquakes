import argparse
from datetime import datetime, timedelta

from csv_writer.csv_writer import write_daily_stats, write_highest_earthquakes
from database.dbmanager import DatabaseManager
from utils.get_earthquakes import get_earthquakes


def check_positive_integer(value):
    """Convert a string to an integer value and check it is positive.

    Parameters:
        - value: the string to be converted and checked

    Raise:
        - ArgumentTypeError: if the value is <= 0
        - ValueError: if the value cannot be transformed in an integer
    """
    try:
        int_value = int(value)
        if int_value <= 0:
            raise argparse.ArgumentTypeError(
                ('%s is an invalid positive integer value. '
                 'The number of days must be > 0') % value)
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError(
            "%s is not a positive integer value" % value)


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--days', dest='days', type=check_positive_integer,
                    help='number of days to analyze, must be > 0',
                    required=True)
parser.add_argument('--no-cache', dest='cache', action='store_true',
                    help='do not use cached data', default=False)
parser.add_argument('--no-csv', dest='csv', action='store_true',
                    help='do not save additional information on csv files',
                    default=False)
args = parser.parse_args()

db = DatabaseManager('database/earthquakes.db')

# get the date of today - days_past days at 00 AM
start_date = search_date = (
    datetime.now() + timedelta(days=-args.days)).strftime("%Y-%m-%d")

if not args.cache:
    max_date = db.max_date()
    min_date = db.min_date()
    if max_date and min_date:
        last_cached_date = datetime.strptime(max_date, '%Y-%m-%d')
        first_cached_date = datetime.strptime(min_date, '%Y-%m-%d')
        if first_cached_date <= datetime.strptime(start_date, '%Y-%m-%d'):
            # we have some of the data already stored in the database
            search_date = last_cached_date.strftime("%Y-%m-%d")

# fetch and add missing elements
earthquakes = get_earthquakes(search_date)
db.add_elements(earthquakes)

highest_earthquake = db.select_highest(1, start_date)[0]
print(
    ('The largest earthquake of last {} days had magnitude {}\n'
     'and was located at {} on {}')
    .format(args.days,
            highest_earthquake[1],
            highest_earthquake[2],
            highest_earthquake[0])
)

# write additional information to csv files
if not args.csv:
    write_daily_stats(db)
    write_highest_earthquakes(db, start_date, 10)

db.close_connection()
