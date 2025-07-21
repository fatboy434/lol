import sqlite3

class Memory:
    def __init__(self, db_name="memory.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """
        Creates the necessary tables in the database.
        """
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS short_term_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS long_term_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL
                )
            """)

    def set_short_term(self, key, value):
        """
        Sets a value in the short-term memory.
        """
        with self.conn:
            self.conn.execute("INSERT INTO short_term_memory (key, value) VALUES (?, ?)", (key, value))

    def get_short_term(self, key):
        """
        Gets a value from the short-term memory.
        """
        with self.conn:
            cursor = self.conn.execute("SELECT value FROM short_term_memory WHERE key = ?", (key,))
            result = cursor.fetchone()
            return result[0] if result else None

    def set_long_term(self, key, value):
        """
        Sets a value in the long-term memory.
        """
        with self.conn:
            self.conn.execute("INSERT INTO long_term_memory (key, value) VALUES (?, ?)", (key, value))

    def get_long_term(self, key):
        """
        Gets a value from the long-term memory.
        """
        with self.conn:
            cursor = self.conn.execute("SELECT value FROM long_term_memory WHERE key = ?", (key,))
            result = cursor.fetchone()
            return result[0] if result else None
