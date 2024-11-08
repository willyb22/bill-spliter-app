from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, \
    QListWidget, QLabel, QScrollArea

class DescriptionsSection(QWidget):
    def __init__(self, data_handler, state):
        super().__init__()
        self.data_handler = data_handler
        self.state = state
        
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('Description:'))
        # input description
        layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('New Desctiption ...')
        self.input_button = QPushButton('Add')
        self.input_button.clicked.connect(lambda: self.add_description())

        layout.addWidget(self.input_field)
        layout.addWidget(self.input_button)
        main_layout.addLayout(layout)
        # description display
        self.description_display = QListWidget()
        self.description_display.setFixedHeight(100)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.description_display)

        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        self.fill_descriptions()

    def add_description(self, description=None, to_state=True):
        if description is None:
            description = self.input_field.text()
        if description:
            self.data_handler.add_description(description, to_state=to_state)
            self.description_display.addItem(description)

            self.input_field.clear()

    def fill_descriptions(self):
        self.data_handler.get_descriptions()
        # descriptions = list(self.state['transactions']['descriptions'].values())
        for i, description in self.state['transactions']['descriptions'].items():
            self.add_description(description, to_state=False)
            


