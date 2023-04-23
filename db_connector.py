import sqlite3 as sl


class Database:
    def __init__(self, file=None):
        if file is None:
            self.connection = sl.connect("data.db")
        else:
            self.connection = sl.connect(file)
        self._create_table()
        self.cash_types = ["deposit", "delivery", "revenue"]

    def _create_table(self):
        self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS INVENTORY (
                        id INTEGER primary key,
                        date TEXT,
                        brand TEXT,
                        count INTEGER,
                        cash_id TEXT
                    );
                    """)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS CASH (
                id INTEGER primary key,
                date TEXT,
                value FLOAT(10, 2),
                type TEXT
        )
        """)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS BRAND (
                id INTEGER primary key,
                brand_name TEXT,
                bottles_in_crate INTEGER
            )
        """)
        self.connection.commit()

        # function to change the bottle count in inventory ( used for deliveries and taking inventory)
    def change_inventory_abs(self, date_string, brand_id, bottle_count, cash_id=""):
        self.connection.execute("INSERT INTO INVENTORY (date, brand, count, cash_id) values(?, ?, ?, ?)",
                                (date_string, brand_id, bottle_count, cash_id))
        self.connection.commit()

    def delete_all_tables(self):
        self.connection.execute("DROP TABLE BRAND")
        self.connection.execute("DROP TABLE CASH")
        self.connection.execute("DROP TABLE INVENTORY")

        # select all elements with name {string} and return the id of the first
    def get_brand_id_from_name(self, string):
        return self.connection.execute("""SELECT * FROM BRAND WHERE brand_name = ?""", (string,)).fetchone()[0]

        # amount: positive=cost; type can be: deposit, delivery or revenue
    def add_cashflow(self, date_string, amount, cash_type):
        if cash_type not in self.cash_types:
            raise ValueError("cash_type is not a viable type")
        self.connection.execute("INSERT INTO CASH (date, value, type) VALUES (?, ?, ?)",
                                (
                                    date_string,
                                    amount,
                                    cash_type
                                ))

    def add_brand(self, brand_name, bottle_count):
        self.connection.execute("INSERT INTO BRAND (brand_name, bottles_in_crate) VALUES (?, ?)",
                                (brand_name, bottle_count)
                                )

    def get_brands(self):
        return self.connection.execute("SELECT brand_name, bottles_in_crate FROM BRAND").fetchall()





