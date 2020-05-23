import csv

"""Write additional information regarding earthquakes to csv files"""


def write_daily_stats(db):
    """Write the maximum, minimum and average magnitude per day to a csv file.

    Parameters:
        - db: the database containing the information
    """
    daily_stats = db.select_daily_stats()
    with open('daily_stats.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['Date', 'Max', 'Min', 'Avg'])
        for stats in daily_stats:
            writer.writerow(stats)


def write_highest_earthquakes(db, limit=1):
    """Write the earthquakes with highest magnitude to a csv file.
    The number of earthquakes written is determined by a limit.

    Parameters:
        - db: the database containing the information
        - limit: the number of earthquakes desired
    """
    highest_earthquakes = db.select_highest(limit)
    with open('highest_earthquakes.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['Date', 'Magnitude', 'Location'])
        for earthquake in highest_earthquakes:
            writer.writerow(earthquake)
