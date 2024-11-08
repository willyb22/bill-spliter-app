from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, \
    QLabel, QPushButton, QLineEdit


from .participant_data_handler import ParticipantDataHandler
from .participant_table import ParticipantTable
from .participant_input_text import ParticipantInputText

class ParticipantWidget(QWidget):
    def __init__(self, data_handler, state):
        super().__init__()
        
        self.main_state = state
        self.main_state['participant'] = dict()
        self.state = self.main_state['participant']
        self.state['changed'] = dict()

        self.data_handler = ParticipantDataHandler(data_handler, self.state)
        self.initUI()

    def initUI(self):
        
        main_layout = QVBoxLayout()
        # main label
        self.main_label = QLabel("Participant")

        # participant input layout
        input_layout = QHBoxLayout()
        self.input_text = ParticipantInputText(self.data_handler, self.state)
        # add button
        self.input_button = QPushButton("Add")
        input_layout.addWidget(self.input_text)
        input_layout.addWidget(self.input_button)

        # participant table
        self.participant_table = ParticipantTable(self.data_handler, self.state)
        
        # connect input button to participant table
        self.input_button.clicked.connect(self.handle_input_button)
        
        # Add all widgets to layout
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.participant_table)
        self.setLayout(main_layout)

    def handle_input_button(self):
        participant_name = self.input_text.input_text.text()
        participant_id = self.data_handler.add_participant(participant_name)
        # add row
        self.participant_table.add_row(participant_id, participant_name)
