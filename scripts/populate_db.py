import argparse
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '..')

from database.dbmanager import DatabaseManager
from utils.get_earthquakes import get_earthquakes

"""Populate or clear the database"""

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-p', '--populate', dest='populate', action='store_true', help='populate database')
group.add_argument('-d', '--delete', dest='delete', action='store_true', help='clear database')
args = parser.parse_args()

db = DatabaseManager('../database/earthquakes.db')

if args.populate:
    # calculate starting date by subtracting 2 weeks
    start_date = (datetime.now() + timedelta(days=-14)).strftime("%Y-%m-%d")
    earthquakes = get_earthquakes(start_date)
    db.add_elements(earthquakes)
    db.close_connection()

# TODO: else?
if args.delete:
    db.clear()
