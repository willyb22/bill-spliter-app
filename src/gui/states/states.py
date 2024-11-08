from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from .states_data_handler import StatesDataHandler
from .states_table import StatesTable

class StatesWidget(QWidget):
    def __init__(self, data_handler, state):
        super().__init__()
        self.state = state

        self.date_handler = StatesDataHandler(data_handler, self.state)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Debt:'))

        self.states_table = StatesTable(self.date_handler, self.state)
        layout.addWidget(self.states_table)

        self.setLayout(layout)

