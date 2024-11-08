class StatesDataHandler:
    def __init__(self, data_handler, state):
        self.data_handler = data_handler
        self.main_state = state
        self.main_state['states'] = dict()
        self.state = self.main_state['states']
    
    def get_states(self):
        self.state['debt'] = []
        for id, from_id, to_id, amount in self.data_handler.fetch_bill.fetch_states():
            self.state['debt'].append({
                'state_id': id,
                'owe_id': from_id,
                'owed_id': to_id,
                'amount': amount
            })

    def get_name(self, id):
        return self.main_state['participant']['active'].get(id, "N/A")