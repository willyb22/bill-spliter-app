from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QComboBox
from PyQt5.QtGui import QIntValidator

class PayWindow(QDialog):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        
        self.setWindowTitle("Pay Window")
        self.setGeometry(100, 100, 300, 150)

        # Layouts
        layout = QVBoxLayout()

        owe_person, owed_person = self.user_data['owe_person'], self.user_data['owed_person']
        amount = self.user_data['amount']
        if amount<0:
            owe_person, owed_person = owed_person, owe_person
        self.user_data['pay_person'] = owe_person
        combo_layout = QHBoxLayout()
        self.options = [owe_person, owed_person]
        self.combo_box = QComboBox()
        self.combo_box.addItems(self.options)
        self.pay_to_label = QLabel(f"pay to {owed_person}")
        self.combo_box.currentIndexChanged.connect(self.on_selection_changed)
        
        combo_layout.addWidget(self.combo_box)
        combo_layout.addWidget(self.pay_to_label)
        layout.addLayout(combo_layout)

        # Input field, with a validator for positive integers
        self.input_field = QLineEdit(str(self.user_data['pay']))
        self.input_field.setPlaceholderText("Enter amount to pay ...")
        int_validator = QIntValidator(1, 1000000000, self)  # Allows positive integers only
        self.input_field.setValidator(int_validator)  # Apply validator to QLineEdit
        layout.addWidget(QLabel("Input:"))
        layout.addWidget(self.input_field)

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
        if self.input_field.hasAcceptableInput():
            # Update the final text only if OK is clicked and input is valid
            self.user_data['pay'] = int(self.input_field.text())
            self.accept()  # This will close the dialog and return Accepted
        else:
            # Show an error message or handle invalid input if needed
            self.input_field.setText("")  # Clear invalid input

    def on_selection_changed(self):
        selection = self.combo_box.currentText()
        if selection == self.user_data['owe_person']:
            self.pay_to_label.setText(f"pay to {self.user_data['owed_person']}")
        else:
            self.pay_to_label.setText(f"pay to {self.user_data['owe_person']}")
        self.user_data['pay_person'] = selection