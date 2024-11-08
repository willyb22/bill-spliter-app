from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFrame

from .participant.participant import ParticipantWidget
from .states.states import StatesWidget
from .transactions.transactions import TransactionsWidget

class BillSplitterApp(QWidget):
    def __init__(self, data_handler=None):
        super().__init__()

        self.data_handler = data_handler
        self.state = dict()
        self.initUI()

    def initUI(self):
        self.move(200,100)
        main_layout = QHBoxLayout()

        # Participant Component
        self.participant_widget = ParticipantWidget(self.data_handler, self.state)

        # Transactions Component
        self.transactions_widget = TransactionsWidget(self.data_handler, self.state)

        # States Component
        self.states_widget = StatesWidget(self.data_handler, self.state)
        
        # Connecting state
        self.transactions_widget.connectState()

        # Add all components to to main_layout
        main_layout.addWidget(self.participant_widget)
        main_layout.addWidget(self.create_separator())
        main_layout.addWidget(self.states_widget)
        main_layout.addWidget(self.create_separator())
        main_layout.addWidget(self.transactions_widget)

        self.setLayout(main_layout)
        self.setWindowTitle("Bill Splitter")
    
    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)  # Set the shape of the frame to a vertical line
        separator.setFrameShadow(QFrame.Sunken)
        return separator

if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = BillSplitterApp()
    window.show()
    sys.exit(app.exec_())
