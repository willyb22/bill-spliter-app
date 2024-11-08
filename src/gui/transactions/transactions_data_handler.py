from datetime import datetime
class TransactionsDataHandler:
    def __init__(self, data_handler, state):
        self.data_handler = data_handler
        self.main_state = state
        self.state = self.main_state['transactions']

    def get_descriptions(self):
        self.state['descriptions'] = dict()
        for id, description in self.data_handler.fetch_bill.fetch_descriptions():
            self.state['descriptions'][id] = description

    def add_description(self, description, to_state=True):
        try:
            id = self.data_handler.add_bill.add_descriptions(description=description)
            if to_state:
                self.state['descriptions'][id] = description
        except Exception as e:
            print('Error when adding description :', str(e))
            id = None
        return id

    def get_transactions(self):
        self.state['transactions'] = []
        for timestamp, name, description, amount in self.data_handler.fetch_bill.fetch_transactions():
            self.state['transactions'].append({
                'timestamp': datetime.fromtimestamp(timestamp).strftime(r"%Y/%m/%d"),
                'description': description,
                'name': name,
                'amount': amount
            })

    def add_transaction(self, description_id, participant_ids, proportions, amounts):
        self.data_handler.add_bill.add_transaction(
            participants=participant_ids,
            description_id=description_id,
            proportions=proportions,
            amounts=amounts
        )
