import sqlite3


class DatabaseManager(object):
    def __init__(self, filename):
        self.database_file = filename
        self.connection = None
        self._create_table()

    def add_elements(self, elements):
        if not self.connection:
            self._connect()

        for element in elements:
            try:
                self._add_element(element)
            except sqlite3.IntegrityError:
                pass

        self._close_connection()

    def clear(self):
        if not self.connection:
            self._connect()

        self.connection.execute('DELETE FROM earthquakes')

        self._close_connection()

    def max_date(self):
        date = self.connection.execute('SELECT MAX(date) FROM earthquakes')
        return date.fetchall()[0][0]

    def select_highest(self, limit):
        highest_earthquakes = self.connection.execute('''SELECT date, magnitude, location FROM earthquakes
                                                      ORDER BY magnitude DESC
                                                      LIMIT ''' + str(limit))
        return highest_earthquakes.fetchall()

    def select_daily_stats(self):
        daily_stats = self.connection.execute(
            '''SELECT date, MAX(magnitude),MIN(magnitude),AVG(magnitude) FROM earthquakes GROUP BY date''')
        return daily_stats.fetchall()

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

    def _close_connection(self):
        self.connection.close()

    def _add_element(self, element):
        self.connection.execute('INSERT INTO earthquakes(magnitude, location, date) VALUES(?,?,?)',
                                (element[0], element[1], element[2]))
        self.connection.commit()