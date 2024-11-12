from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QDialog
from PyQt5.QtCore import pyqtSignal

from .pay_window import PayWindow
import time

class StatesTable(QWidget):
    stateChanged = pyqtSignal(dict)
    def __init__(self, data_handler, state):
        super().__init__()
        self.data_handler = data_handler
        self.state = state

        self.initUI()
        self.state['states']['changed'] = {'states_table': self.stateChanged}
        self.state['participant']['changed']['participant_input'].connect(self.refresh_table)
        self.state['transactions']['changed']['transactions'].connect(self.refresh_table)

    def initUI(self):
        layout = QVBoxLayout()

        # Create table
        self.table = QTableWidget()
        # Create an empty table with 3 columns
        self.table = QTableWidget(0, 4)  # Start with 0 rows
        self.table.setHorizontalHeaderLabels(["Owe", 'Owed', 'Amount', 'Action'])

        # Set a fixed height so the table shows only a certain number of rows
        row_height = self.table.verticalHeader().defaultSectionSize()
        visible_rows = 10
        self.table.setFixedHeight(row_height * visible_rows + self.table.horizontalHeader().height())
        row_width = self.table.horizontalHeader().defaultSectionSize()
        visible_columns = 4
        self.table.setFixedWidth(row_width * visible_columns + self.table.horizontalHeader().height())

        # Add the table to the layout
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.fill_table()

    def refresh_table(self):
        print('triggered')
        nrow = self.table.rowCount()
        for r in range(nrow-1, -1, -1):
            self.remove_row(r)
        self.fill_table()

    def remove_row(self, row):
        self.table.removeRow(row)

    def add_row(self, owe_id, owed_id, amount):
        # Insert a new row at the end of the table
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Set All Columns
        owe_person = self.data_handler.get_name(owe_id)
        self.table.setItem(row_position, 0, QTableWidgetItem(owe_person))

        owed_person = self.data_handler.get_name(owed_id)
        self.table.setItem(row_position, 1, QTableWidgetItem(owed_person))

        self.table.setItem(row_position, 2, QTableWidgetItem(str(amount)))

        # Create a delete button for the new row
        pay_button = QPushButton("Pay")
        # Open new window if the pay_button is clicked
        pay_button.clicked.connect(lambda _, r=row_position: self.open_pay_window(r, owe_id, owed_id))
        self.table.setCellWidget(row_position, 3, pay_button)
        # print(self.state)

    def fill_table(self):
        self.data_handler.get_states()
        for data in self.state['states']['debt']:
            self.add_row(data['owe_id'], data['owed_id'], data['amount'])

    def open_pay_window(self, row, owe_id, owed_id):
        debt_id = next((i for i, debt in enumerate(self.state['states']['debt']) \
                        if debt['owe_id']==owe_id and debt['owed_id']==owed_id), None)
        self.user_data = self.state['states']['debt'][debt_id]
        self.user_data['owe_person'] = self.data_handler.get_name(self.user_data['owe_id'])
        self.user_data['owed_person'] = self.data_handler.get_name(self.user_data['owed_id'])
        pay = 0
        self.user_data['pay'] = pay

        pay_window = PayWindow(self.user_data)
        if pay_window.exec_()==QDialog.Accepted and pay!=self.user_data['pay']:
            # update the data
            pay = self.user_data['pay']
            participant_ids = [self.user_data['owe_id'], self.user_data['owed_id']]
            if self.user_data['pay_person']==self.user_data['owe_person']:
                proportions = [0, 1]
                amounts = [pay, 0]
            else:
                proportions = [1, 0]
                amounts = [0, pay]
            user_data = dict()
            user_data['description_id'] = 1
            user_data['participant_ids'] = participant_ids
            user_data['proportions'] = proportions
            user_data['amounts'] = amounts

            self.stateChanged.emit(user_data)
