from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QPushButton, QListWidget, QScrollArea, QDialog
from PyQt5.QtCore import pyqtSignal

import time
from datetime import datetime

from .transactions_data_handler import TransactionsDataHandler
from .description_section import DescriptionsSection
from .transaction_window import TransactionWindow

class TransactionsWidget(QWidget):
    stateChanged = pyqtSignal()
    def __init__(self, data_handler, state):
        super().__init__()
        self.state = state
        self.initState()
        self.data_handler = TransactionsDataHandler(data_handler, self.state)
        self.user_data = {
            'participant_ids': [],
            'description_id': -1,
            'proportions': [],
            'amounts': [],
        }
        self.initUI()

    def initState(self):
        
        self.state['transactions'] = {'changed': {'transactions': self.stateChanged}}
        self.state['states'] = {'changed': {'states_table': pyqtSignal(dict)}}

    def connectState(self):
        self.state['states']['changed']['states_table'].connect(self.handle_states_table_signal)

    def initUI(self):
        self.setFixedWidth(250)
        layout = QVBoxLayout()

        self.description_section = DescriptionsSection(self.data_handler, self.state)
        
        layout.addWidget(self.description_section)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)

        layout.addWidget(separator)
        # Transactions
        layout.addWidget(QLabel('Transactions'))
        self.transactions_display = QListWidget()
        self.transactions_display.setFixedHeight(100)
        self.transactions_display.setMinimumWidth(self.transactions_display.sizeHintForColumn(0) + 20)
        scroll_area = QScrollArea()
        # scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.transactions_display)
        
        layout.addWidget(scroll_area)

        self.add_transaction_button = QPushButton('New Transaction')
        self.add_transaction_button.clicked.connect(self.handle_add_transaction)

        layout.addWidget(self.add_transaction_button)

        self.setLayout(layout)
        self.fill_transactions()
    
    @staticmethod
    def get_transaction_str(**args):
        name = args['name']
        timestamp = args['timestamp']
        description = args['description']
        amount = args['amount']
        proportion_str = f"{args['proportion']}/{args['proportion_total']}"
        return " - ".join([name, timestamp, description, proportion_str, str(amount)]) 

    def add_to_display(self, **args):
        transaction = self.get_transaction_str(**args)
        self.transactions_display.addItem(transaction)
    
    def add_transaction(self):
        print('add transaction')
        description_id = self.user_data['description_id']
        participant_ids = self.user_data['participant_ids']
        proportions = self.user_data['proportions']
        proportion_total = sum(proportions)
        amounts = self.user_data['amounts']
        self.data_handler.add_transaction(description_id, participant_ids, proportions, amounts)

        for id, amount, proportion in zip(participant_ids, amounts, proportions):
            if amount>0:
                name = self.state['participant']['active'][id]
                timestamp = datetime.fromtimestamp(time.time()).strftime(r"%Y/%m/%d")
                description = self.state['transactions']['descriptions'][description_id]
                self.state['transactions']['transactions'].append({
                    'timestamp': timestamp,
                    'desctiption': description,
                    'name': name,
                    'amount': amount,
                    'proportion': proportion,
                    'proportion_total': proportion_total,
                })
                self.add_to_display(name=name,description=description,timestamp=timestamp,amount=amount, proportion=proportion, proportion_total=proportion_total)
        
        self.stateChanged.emit()
    
    def handle_states_table_signal(self, user_data):
        self.user_data['description_id'] = user_data['description_id']
        self.user_data['participant_ids'] = user_data['participant_ids']
        self.user_data['proportions'] = user_data['proportions']
        self.user_data['amounts'] = user_data['amounts']
        
        self.add_transaction()

    def handle_add_transaction(self):
        self.user_data['descriptions'] = self.state['transactions']['descriptions']
        self.user_data['participants'] = self.state['participant']['active']
        self.user_data['participant_ids'] = list(self.user_data['participants'].keys())
        self.user_data['proportions'] = [1]*len(self.user_data['participants'])
        self.user_data['amounts'] = [0]*len(self.user_data['participants'])

        transaction_window = TransactionWindow(self.user_data)
        if transaction_window.exec_()==QDialog.Accepted:
            if any([x>0 for x in self.user_data['amounts']]) and any([x>0 for x in self.user_data['proportions']]):
                self.add_transaction()

    def fill_transactions(self):
        self.data_handler.get_transactions()
        for transaction in self.state['transactions']['transactions']:
            if transaction['amount']!=0:
                self.add_to_display(**transaction)