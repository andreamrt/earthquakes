import argparse
from datetime import datetime, timedelta
import pandas as pd

from csv_writer.csv_writer import write_daily_stats, write_highest_earthquakes
from database.dbmanager import DatabaseManager
from utils.get_earthquakes import get_earthquakes
from utils.argparse_util import check_positive_integer


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--days', dest='days', type=check_positive_integer,
                    help='Number of days to analyze, must be > 0',
                    required=True)
parser.add_argument('--no-cache', dest='cache', action='store_true',
                    help='Do not use cached data', default=False)
parser.add_argument('--no-csv', dest='csv', action='store_true',
                    help='Do not save additional information on csv files',
                    default=False)
parser.add_argument('--no-table', dest='table', action='store_true',
                    help='Do not print highest earthquakes',
                    default=False)
parser.add_argument('-tl', '--table-limit', dest='table_limit',
                    help=('Specify number of rows for the printed table. '
                          'Default value = 10'),
                    nargs='?', type=check_positive_integer, default=10)
parser.add_argument('-cl', '--csv-limit', dest='csv_limit',
                    help=('Specity number of highest earthquakes to write '
                          'to csv. Default value=10'),
                    nargs='?', type=check_positive_integer, default=10)
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
if not args.table:
    print('\n These are the {} strongest earthquakes in the past {} days:\n'
          .format(args.table_limit, args.days))

    highest_earthquakes = db.select_highest(args.table_limit, start_date)
    table = pd.DataFrame(highest_earthquakes)
    table.index += 1
    table.columns = ['Date', 'Magnitude', 'Location']
    print(table)

# write additional information to csv files
if not args.csv:
    write_daily_stats(db)
    write_highest_earthquakes(db, start_date, args.csv_limit)

db.close_connection()
