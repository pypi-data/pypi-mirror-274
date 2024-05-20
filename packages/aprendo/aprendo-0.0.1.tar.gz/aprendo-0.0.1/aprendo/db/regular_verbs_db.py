from .base_db import BaseDB
import os
from ..verbs import RegularVerb

class VerbsDB(BaseDB):
    def __init__(self):
        """Initialize the VerbsDB class with a predefined database file and data."""
        super().__init__("regular_verbs.db")
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
        create_verbs_table_query = """
        CREATE TABLE IF NOT EXISTS verbs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            verb TEXT NOT NULL,
            translation TEXT NOT NULL,
            ending TEXT NOT NULL
        );
        """
        self.execute_query(create_verbs_table_query)

    def insert_verbs(self, verbs : list[RegularVerb]):
        """Insert verbs into the unified table."""
        insert_query = "INSERT INTO verbs (verb, translation, ending) VALUES (?, ?, ?);"
        for verb in verbs:
            self.execute_query(insert_query, (verb.word, verb.translation, verb.get_ending()))

    def get_all_verbs(self):
        """Retrieve all verbs from the database."""
        select_verbs_query = "SELECT * FROM verbs;"
        return self.execute_read_query(select_verbs_query)

    def get_verbs_by_ending(self, ending):
        """Retrieve verbs by their ending."""
        select_verbs_query = "SELECT * FROM verbs WHERE ending = ?;"
        return self.execute_read_query(select_verbs_query, (ending,))
