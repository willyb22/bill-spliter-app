from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QTableWidget, \
    QTableWidgetItem, QComboBox, QCompleter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator

class DescriptionOption(QComboBox):
    avoid_descriptions = ['pay debt']
    def __init__(self, descriptions, parent = None):
        super().__init__(parent)
        self.descriptions = descriptions
        self.options = [desc for desc in self.descriptions.values() if desc not in self.avoid_descriptions]

        self.addItems(self.options)
        # Create a completer with the options list
        self.completer = QCompleter(self.options)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)  # Make search case insensitive
        self.completer.setFilterMode(Qt.MatchContains)         # Enable substring matching

        # Set up a custom QLineEdit to use the completer
        self.setEditable(True)
        self.lineEdit().setCompleter(self.completer)
    
    def get_id(self):
        selected_option = self.currentText()
        for id, desc in self.descriptions.items():
            if desc==selected_option:
                return id
        return -1
    
    def check_validity(self):
        return (self.currentText() in self.options)


class TransactionTable(QTableWidget):
    def __init__(self, participants, proportions, amounts):
        super().__init__(len(participants),3)
        self.participants = participants
        self.proportions = proportions
        self.amounts = amounts

        self.setHorizontalHeaderLabels(['Name', 'Proportion', 'Amount'])
        row_height = self.verticalHeader().defaultSectionSize()
        visible_rows = len(participants)+1
        self.setFixedHeight(row_height * visible_rows + self.horizontalHeader().height())
        row_width = self.horizontalHeader().defaultSectionSize()
        visible_columns = 3
        self.setFixedWidth(row_width * visible_columns + self.horizontalHeader().height())

        self.populate_table()

    def populate_table(self):
        for row, (name, proportion, amount) in enumerate(zip(self.participants, self.proportions, self.amounts)):
            self.setItem(row, 0, QTableWidgetItem(name))

            input_proportion = QLineEdit(str(proportion))
            int_validator = QIntValidator(0, 1000000)  # Allows non negative integers only
            input_proportion.setValidator(int_validator)
            self.setCellWidget(row, 1, input_proportion)

            input_amount = QLineEdit(str(amount))
            int_validator = QIntValidator(0, 1000000000)  # Allows non negative integers only
            input_amount.setValidator(int_validator)
            self.setCellWidget(row, 2, input_amount)

    def check_validity(self):
        result = True
        for row in range(self.rowCount()):
            input_proportion = self.cellWidget(row, 1)
            result = (result and input_proportion.hasAcceptableInput())
            input_amount = self.cellWidget(row, 2)
            result = (result and input_amount.hasAcceptableInput())
        return result
    
    def get_proportions_amounts(self):
        proportions = []
        amounts = []
        for row in range(self.rowCount()):
            input_proportion = self.cellWidget(row, 1)
            proportions.append(int(input_proportion.text()))
            input_amount = self.cellWidget(row, 2)
            amounts.append(int(input_amount.text()))
        return proportions, amounts

class TransactionWindow(QDialog):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        
        self.setWindowTitle("Transaction Window")
        # self.setGeometry(100, 100, 300, 150)

        # Layouts
        layout = QVBoxLayout()

        # Description Selectable
        self.combo_box = DescriptionOption(self.user_data['descriptions'])
        
        layout.addWidget(QLabel('Description: '))
        layout.addWidget(self.combo_box)
        # Transaction Table
        participants = [self.user_data['participants'][id] for id in self.user_data['participant_ids']]
        self.table = TransactionTable(participants, self.user_data['proportions'], self.user_data['amounts'])

        layout.addWidget(self.table)

        # Buttons to confirm or cancel input
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.on_ok_clicked)  # Connect OK button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)  # Connect Cancel button directly to rejection
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def on_ok_clicked(self):
        # Check if the input is valid before accepting
        if self.table.check_validity() and self.combo_box.check_validity():
            # Update the user data if all inputs are valid
            print('on_ok_click')
            proportions, amounts = self.table.get_proportions_amounts()
            self.user_data['description_id'] = self.combo_box.get_id()
            self.user_data['proportions'] = proportions
            self.user_data['amounts'] = amounts
            self.accept()  # This will close the dialog and return Accepted
        else:
            # Show an error message or handle invalid input if needed
            self.input_field.setText("")  # Clear invalid input