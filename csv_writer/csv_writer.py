import csv


def write_daily_stats(db):
    daily_stats = db.select_daily_stats()
    with open('daily_stats.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['Date', 'Max', 'Min', 'Avg'])
        for stats in daily_stats:
            writer.writerow(stats)


def write_highest_earthquakes(db, limit):
    highest_earthquakes = db.select_highest(limit)
    with open('highest_earthquakes.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['Date', 'Magnitude', 'Location'])
        for earthquake in highest_earthquakes:
            writer.writerow(earthquake)
