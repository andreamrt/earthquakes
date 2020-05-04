from database.dbmanager import DatabaseManager
from earthquakes import get_earthquakes

db = DatabaseManager('earthquakes.db')
earthquakes = get_earthquakes(14)

db.add_elements(earthquakes)

db.clear()
