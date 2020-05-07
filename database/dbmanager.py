import sqlite3


class DatabaseManager(object):
    """Database Manager class
    responsible for:
    - creating anc closing the connection
    - adding new entries
    - selecting stored information
    """

    def __init__(self, filename):
        """Constructor.

        Parameters:
            - filename: the file where to store the database
        """
        self.database_file = filename
        self.connection = None
        self._create_table()

    def close_connection(self):
        """Close an existing connection"""
        self.connection.close()

    def add_elements(self, elements):
        """Add a list of elements to the database.

        Parameters:
            - elements: list of entries
        """

        # there must be an active connection
        if not self.connection:
            self._connect()

        for element in elements:
            try:
                self._add_element(element)
            except sqlite3.IntegrityError:
                pass

    def clear(self):
        """Clear the database"""

        # self contained: open and close connection
        if not self.connection:
            self._connect()

        self.connection.execute('DELETE FROM earthquakes')

        self.close_connection()

    def max_date(self):
        """Extract the date of the most recent earthquake"""
        if not self.connection:
            self._connect()

        date = self.connection.execute('SELECT MAX(date) FROM earthquakes')

        return date.fetchall()[0][0]

    def select_highest(self, limit):
        """Select the earthquakes with highest magnitude.

        Parameters:
            - limit: number of earthquakes to return
        """
        if not self.connection:
            self._connect()

        highest_earthquakes = self.connection.execute('''SELECT date, magnitude, location FROM earthquakes
                                                      ORDER BY magnitude DESC
                                                      LIMIT ''' + str(limit))

        return highest_earthquakes.fetchall()

    def select_daily_stats(self):
        """Select the maximum, minimum and average magnitude per day"""
        if not self.connection:
            self._connect()

        daily_stats = self.connection.execute(
            '''SELECT date, MAX(magnitude),MIN(magnitude),AVG(magnitude) FROM earthquakes GROUP BY date''')

        return daily_stats.fetchall()

    def get_filename(self):
        """Return the name of the database file"""
        return self.database_file

    def _create_table(self):
        if not self.connection:
            self._connect()

        self.connection.execute('''CREATE TABLE IF NOT EXISTS earthquakes (
                                        id INTEGER PRIMARY KEY,
                                        magnitude FLOAT,
                                        location TEXT NOT NULL,	    
                                        date DATE NOT NULL,
                                        UNIQUE (magnitude, location, date)
                                        )
                                ''')

    def _connect(self):
        self.connection = sqlite3.connect(self.database_file)

    def _add_element(self, element):
        self.connection.execute('INSERT INTO earthquakes(magnitude, location, date) VALUES(?,?,?)',
                                (element[0], element[1], element[2]))
        self.connection.commit()
