from database.dbmanager import DatabaseManager
from earthquakes import get_earthquakes
import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-p', '--populate', dest='populate', action='store_true', help='populate database')
group.add_argument('-d', '--delete', dest='delete', action='store_true', help='clear database')
args = parser.parse_args()

db = DatabaseManager('earthquakes.db')

if args.populate:
    earthquakes = get_earthquakes(14)
    db.add_elements(earthquakes)

# TODO: else?
if args.delete:
    db.clear()
