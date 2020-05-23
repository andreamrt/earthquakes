import os
import unittest
from datetime import datetime

from csv_writer.csv_writer import write_highest_earthquakes, write_daily_stats
from database.dbmanager import DatabaseManager


class TestCsv(unittest.TestCase):
    """Test case for the correct creation of non-empty csv files"""

    def setUp(self):
        self.temporary_database = DatabaseManager('/tmp/temp.db')
        self.stats_file = '/tmp/daily_stats.csv'
        self.highest_file = '/tmp/highest_earthquakes.csv'
        self.start_date = (datetime.now()).strftime("%Y-%m-%d")
        write_daily_stats(self.temporary_database, filename=self.stats_file)
        write_highest_earthquakes(self.temporary_database, self.start_date,
                                  filename=self.highest_file)

    def test_invalid_argument(self):
        """Check invalid argument not triggering file creation"""
        stats_file = '/tmp/daily_stats_inv.csv'
        highest_file = '/tmp/highest_earthquakes_inv.csv'
        write_daily_stats(None, filename=stats_file)
        write_highest_earthquakes(None, self.start_date, filename=highest_file)
        self.assertFalse(os.path.exists('/tmp/' + stats_file))
        self.assertFalse(os.path.exists('/tmp/' + highest_file))

    def test_files_creation(self):
        """Check the creation of all the files"""
        self.assertTrue(os.path.exists('/tmp/temp.db'))
        self.assertTrue(os.path.exists(self.stats_file))
        self.assertTrue(os.path.exists(self.highest_file))

    def test_non_empty_datafiles(self):
        """Check the presence of data inside the csv files."""
        with open(self.stats_file, 'r') as csv_file:
            self.assertTrue(csv_file.read(1))
        with open(self.highest_file, 'r') as csv_file:
            self.assertTrue(csv_file.read(1))

    def tearDown(self):
        self.temporary_database.close_connection()
        os.remove(self.temporary_database.get_filename())
        os.remove(self.stats_file)
        os.remove(self.highest_file)


if __name__ == '__main__':
    unittest.main()
