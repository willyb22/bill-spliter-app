from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem

class ParticipantTable(QWidget):
    def __init__(self, data_handler, state):
        super().__init__()
        self.data_handler = data_handler
        self.state = state

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        # Create an empty table with 3 columns
        self.table = QTableWidget(0, 2)  # Start with 0 rows
        self.table.setHorizontalHeaderLabels(["Name", "Action"])

        # Set a fixed height so the table shows only a certain number of rows
        row_height = self.table.verticalHeader().defaultSectionSize()
        visible_rows = 10
        self.table.setFixedHeight(row_height * visible_rows + self.table.horizontalHeader().height())
        row_width = self.table.horizontalHeader().defaultSectionSize()
        visible_columns = 2
        self.table.setFixedWidth(row_width * visible_columns + self.table.horizontalHeader().height())

        # Add the table to the layout
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.fill_table()

    def add_row(self, id, name):
        # Insert a new row at the end of the table
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Set Name columns
        self.table.setItem(row_position, 0, QTableWidgetItem(name))

        # Create a delete button for the new row
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda _, r=row_position: self.remove_row(r, id))
        self.table.setCellWidget(row_position, 1, delete_button)
        # print(self.state)

    def fill_table(self):
        self.data_handler.get_participant(is_active=True)

        for id, name in self.state['active'].items():
            self.add_row(id, name)

    def remove_row(self, row, id):
        self.data_handler.remove_participant(id)

        self.table.removeRow(row)
        # print(self.state)