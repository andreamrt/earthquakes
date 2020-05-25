import argparse
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '..')

from utils.get_earthquakes import get_earthquakes  # noqa: E402
from database.dbmanager import DatabaseManager  # noqa: E402K
from utils.argparse_util import check_positive_integer  # noqa: E402


"""Populate or clear the database"""

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-p', '--populate', dest='populate',
                   nargs='?', const=14, type=check_positive_integer,
                   help='Populate database. Default value = 14 days')
group.add_argument('-d', '--delete', dest='delete',
                   action='store_true', help='Clear database')
args = parser.parse_args()

db = DatabaseManager('../database/earthquakes.db')

if args.populate:
    # calculate starting date by subtracting 2 weeks
    start_date = (datetime.now() +
                  timedelta(days=-args.populate)).strftime("%Y-%m-%d")
    earthquakes = get_earthquakes(start_date)
    db.add_elements(earthquakes)
    db.close_connection()

# TODO: else?
if args.delete:
    db.clear()
