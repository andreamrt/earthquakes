import requests
from datetime import datetime, timedelta
import json

USGS_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query?starttime={}&format=geojson&limit=20000'


def get_earthquakes(days_past):
    # get the date of today - days_past days at 00 AM
    start_date = (datetime.now() + timedelta(days=-days_past)).strftime("%Y-%m-%d")
    URL = USGS_URL.format(start_date)
    events = json.loads(requests.get(URL).text)
    results = []

    for event in events['features']:
        try:
            magnitude = float(event['properties']['mag'])
            place = event['properties']['place']
            time = str(datetime.fromtimestamp(event['properties']['time'] / 1000).date())

            results.append([magnitude, place, time])
        except TypeError:
            pass
    return results
