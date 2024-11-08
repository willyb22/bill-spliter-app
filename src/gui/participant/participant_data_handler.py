class ParticipantDataHandler:
    def __init__(self, data_handler, state):
        self.data_handler = data_handler
        self.state = state
        self.state['active'] = dict()
        self.state['inactive'] = dict()

    def get_participant(self, is_active=True):
        data = self.data_handler.fetch_bill.fetch_participant(is_active=is_active)
        if is_active:
            self.state['active'] = dict([(id, name) for id, name, _ in data])
        else:
            self.state['inactive'] = dict([(id, name) for id, name, _ in data])
    
    def remove_participant(self, participant_id):
        self.data_handler.add_bill.update_participant(participant_id, is_active=False)

        name = self.state['active'].pop(participant_id, None)
        self.state['inactive'][participant_id] = name
        self.emit()

    def add_participant(self, participant_name):
        participant_id = -1
        for id, name in self.state['inactive'].items():
            if name==participant_name:
                participant_id = id
                _ = self.state['inactive'].pop(participant_id)
                self.emit()
                self.data_handler.add_bill.update_participant(participant_id, is_active=True)
                break
        if participant_id==-1:
            participant_id = self.data_handler.add_bill.add_participant(name=participant_name)
        self.state['active'][participant_id] = participant_name
        
        self.emit()
        return participant_id
    
    def emit(self):
        for _, signal in self.state['changed'].items():
            signal.emit()
        

    
    
    
