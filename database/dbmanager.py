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
