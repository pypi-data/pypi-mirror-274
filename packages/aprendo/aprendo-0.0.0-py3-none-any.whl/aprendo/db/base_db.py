import sqlite3
from sqlite3 import Error

class BaseDB:
    def __init__(self, db_file):
        """Initialize the BaseDB class with the database file."""
        self.db_file = db_file
        self.connection = None

    def create_connection(self):
        """Create a database connection to the SQLite database specified by db_file."""
        try:
            self.connection = sqlite3.connect(self.db_file)
            print(f"Connection to {self.db_file} established.")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def execute_query(self, query, params=None):
        """Execute a single query."""
        if self.connection is None:
            print("Connection is not established.")
            return

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully.")
        except Error as e:
            print(f"Error executing query: {e}")

    def execute_read_query(self, query, params=None):
        """Execute a read query and return the results."""
        if self.connection is None:
            print("Connection is not established.")
            return

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error reading data: {e}")

    def close_connection(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print(f"Connection to {self.db_file} closed.")
