from .base_db import BaseDB
import os
from ..nouns import Noun

class NounsDB(BaseDB):
    def __init__(self):
        """Initialize the NounsDB class with a predefined database file and data."""
        super().__init__("nouns.db")
        self.initialize_database()
        

    def initialize_database(self):
        """Initialize the database with predefined tables if it doesn't exist."""
        if not os.path.exists(self.db_file):
            self.create_connection()
            self.create_predefined_table()
            self.close_connection()
        else:
            # Ensure the connection is established if the database file already exists
            self.create_connection()

    def create_predefined_table(self):
        """Create the unified table in the database."""
        create_nouns_table_query = """
        CREATE TABLE IF NOT EXISTS nouns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            noun TEXT NOT NULL,
            translation TEXT NOT NULL
        );
        """
        self.execute_query(create_nouns_table_query)

    def insert_nouns(self, nouns : list[Noun]):
        """Insert nouns into the unified table."""
        insert_query = "INSERT INTO nouns (noun, translation) VALUES (?, ?);"
        for noun in nouns:
            self.execute_query(insert_query, (noun.word, noun.translation))

    def get_all_nouns(self):
        """Retrieve all nouns from the database."""
        select_nouns_query = "SELECT * FROM nouns;"
        return self.execute_read_query(select_nouns_query)

