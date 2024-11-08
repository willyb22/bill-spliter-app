import time
from .utils.functions import split_bill

class AddBill:
    def __init__(self, conn, cursor, script_dir):
        self.conn = conn
        self.cursor = cursor
        self.script_dir = script_dir
        self.store_functions()
    
    def store_functions(self):
        pass

    def add_participant(self, **args):
        query = "INSERT INTO participant (name) VALUES ('%s');"% \
            (args['name'])
        self.cursor.execute(query)
        last_id = self.cursor.lastrowid
        # Insert to states
        self.cursor.execute("SELECT id FROM participant;")
        for id, in self.cursor.fetchall():
            if id!=last_id:
                query = "INSERT INTO states (participant_id, participant_to, last_update) VALUES (%d,%d,%d)"% \
                    (id, last_id, int(time.time()))
                self.cursor.execute(query)
        self.conn.commit()
        return last_id
    
    def update_participant(self, participant_id, is_active=True):
        is_active_int = 1 if is_active else 0
        query = "UPDATE participant SET is_active=%d WHERE id=%d"%(is_active_int, participant_id)
        self.cursor.execute(query)
        
        self.conn.commit()


    def add_descriptions(self, **args):
        query = "INSERT OR IGNORE INTO descriptions (detail) VALUES ('%s')"% \
            (args['description'])
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.lastrowid

    def add_transaction(self, **args):
        query = "INSERT INTO transactions (timestamp, description) VALUES ('%s', '%s');"% \
            (
                args.get('timestamp', int(time.time())),
                args['description_id']
            )
        self.cursor.execute(query)
        transaction_id = self.cursor.lastrowid
        
        for participant_id, proportion, amount in zip(
            args['participants'],
            args['proportions'],
            args['amounts']
        ):
            query = "INSERT INTO transaction_detail (transaction_id, participant_id, proportion, amount) VALUES (%d,%d,%f,%f)"% \
                (
                    transaction_id,
                    participant_id,
                    proportion,
                    amount
                )
            self.cursor.execute(query)

        transactions = split_bill(args['proportions'], args['amounts'])
        for owe_person, owed_person, amount in transactions:
            print(args['participants'])
            participant_id = args['participants'][owe_person]
            participant_to = args['participants'][owed_person]
            if participant_id>participant_to:
                amount *= -1
                participant_id, participant_to = participant_to, participant_id
            print(owe_person, owed_person, amount)
            query = "UPDATE states SET amount = amount + %f, last_update = %d WHERE participant_id=%d AND participant_to=%d"% \
                (
                    amount,
                    int(time.time()),
                    participant_id,
                    participant_to
                )
            print(query)
            self.cursor.execute(query)

        self.conn.commit()
    