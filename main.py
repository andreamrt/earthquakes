from earthquakes import get_earthquakes
import argparse


def check_positive(value):
    try:
        int_value = int(value)
        if int_value <= 0:
            raise argparse.ArgumentTypeError("%s is an invalid positive integer value. The number of days must be > 0" % value)
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError("%s is not a positive integer value" % value)


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--days', dest='days', type=check_positive, help='number of days to analyze, must be > 0', required=True)
parser.add_argument('--no-cache', dest='cache', action='store_true', help='do not use cached data', default=False)
args = parser.parse_args()

# days = args.days
days = 1
result = get_earthquakes(days)
print(result)
# print("The largest earthquake of last {} days had magnitude {} and was located at {} on {}".format(days, mag, place, time))
