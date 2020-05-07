import json
from datetime import datetime

import requests

USGS_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query?starttime={}&format=geojson&limit=20000'


def get_earthquakes(start_date):
    """Fetch the most recent 20000 earthquakes from a given starting date

    Parametes:
        - start_date: the starting date
    """

    URL = USGS_URL.format(start_date)
    events = json.loads(requests.get(URL).text)
    results = []

    for event in events['features']:
        try:
            magnitude = float(event['properties']['mag'])
            place = event['properties']['place']
            # timestamp is saved in millisecond format
            time = str(datetime.fromtimestamp(event['properties']['time'] / 1000).date())

            results.append([magnitude, place, time])
        except TypeError:
            # ignore entries that lead to errors
            pass
    return results
