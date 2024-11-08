import os, sqlite3

from .addbill import AddBill
from .fetchbill import FetchBill

class DataHandler:
    def __init__(self, db_config):
        self.db_file = db_config['db_file']
        self.migration_dir = db_config['migration_dir']
        self.view_dir = db_config['view_dir']

        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

        self.create_tables()
        self.add_bill = AddBill(self.conn, self.cursor, self.migration_dir)
        self.fetch_bill = FetchBill(self.cursor, self.view_dir)

    def create_tables(self):
        for file in os.listdir(self.migration_dir):
            if file.endswith('.sql'):
                with open(os.path.join(
                    self.migration_dir,
                    file
                ), 'r') as sqlfile:
                    sql_script = sqlfile.read()
                self.cursor.execute(sql_script)
        

