import csv

"""Write additional information regarding earthquakes to csv files"""


def write_daily_stats(db, filename='daily_stats.csv'):
    """Write the maximum, minimum and average magnitude per day to a csv file.

    Parameters:
        - db: the database containing the information
        - filename: csv file destination
    """
    try:
        daily_stats = db.select_daily_stats()
        with open(filename, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['Date', 'Max', 'Min', 'Avg'])
            for stats in daily_stats:
                writer.writerow(stats)
    except AttributeError:
        pass


def write_highest_earthquakes(db,  start_date, limit=1,
                              filename='highest_earthquakes.csv'):
    """Write the earthquakes with highest magnitude to a csv file.
    The number of earthquakes written is determined by a limit.

    Parameters:
        - db: the database containing the information
        - limit: the number of earthquakes desired
        - start_date: starting date for the search
        - filename: csv file destination
    """
    try:
        highest_earthquakes = db.select_highest(limit, start_date)
        with open(filename, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['Date', 'Magnitude', 'Location'])
            for earthquake in highest_earthquakes:
                writer.writerow(earthquake)
    except AttributeError:
        pass
