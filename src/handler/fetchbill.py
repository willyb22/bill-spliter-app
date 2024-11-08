import os
class FetchBill:
    def __init__(self, cursor, script_dir):
        self.cursor = cursor
        self.script_dir = script_dir

    def fetch_descriptions(self):
        self.cursor.execute('SELECT * FROM descriptions;')
        return self.cursor.fetchall()

    def fetch_transactions(self):
        with open(os.path.join(
            self.script_dir,
            '002_fetch_custom_transactions.sql'
        ), 'r') as sqlfile:
            sql_script = sqlfile.read()
        self.cursor.execute(sql_script)
        return self.cursor.fetchall()
    
    def fetch_participant(self, is_active=None):
        is_active_int = 1 if is_active else 0
        where_clause = "WHERE is_active=%d"%(is_active_int)
        self.cursor.execute('SELECT id, name, is_active FROM participant %s;'%(
            where_clause if is_active is not None else ''
        ))
        return self.cursor.fetchall()
    
    def fetch_states(self):
        with open(os.path.join(
            self.script_dir,
            '001_fetch_active_states.sql'
        ), 'r') as sqlfile:
            sql_script = sqlfile.read()
        self.cursor.execute(sql_script)
        return self.cursor.fetchall()