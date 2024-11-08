from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QCompleter

from PyQt5.QtCore import Qt, QStringListModel, QSortFilterProxyModel, QRegExp, pyqtSignal

class SubstringFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def filterAcceptsRow(self, source_row, source_parent):
        # Get the item text from the model
        model = self.sourceModel()
        item_text = model.data(model.index(source_row, 0), Qt.DisplayRole)
        
        # Check if the filter text is a substring (any position match)
        if self.filterRegExp().indexIn(item_text) >= 0:
            return True
        return False

class ParticipantInputText(QWidget):
    stateChanged = pyqtSignal()
    def __init__(self, data_handler, state):
        super().__init__()
        self.data_handler = data_handler
        self.state = state
        self.state['changed']['participant_input'] = self.stateChanged
        self.initUI()

        self.stateChanged.connect(self.update_recommendations)

    def initUI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel('Name :'))

        self.input_text = QLineEdit()
        self.input_text.setPlaceholderText('New Participant ...')

        self.data_handler.get_participant(is_active=False)
        self.refresh_completer()

        layout.addWidget(self.input_text)
        self.setLayout(layout)

    def refresh_completer(self):
        recommendations = list(self.state['inactive'].values())  # Convert to list if necessary

        # Create a QStringListModel with recommendations
        recommendation_model = QStringListModel(recommendations)

        # Set up the custom filtering model to allow substring matching
        filter_model = SubstringFilterProxyModel()
        filter_model.setSourceModel(recommendation_model)

        # Create a QCompleter with the custom filter model
        completer = QCompleter(filter_model, self.input_text)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        # Connect text changes to update the filter, allowing matches at any position
        self.input_text.textChanged.connect(
            lambda text: filter_model.setFilterRegExp(
                QRegExp(f".*{text}.*", Qt.CaseInsensitive, QRegExp.RegExp)
            )
        )

        # Set the completer for the input text
        self.input_text.setCompleter(completer)

    def update_recommendations(self):
        self.refresh_completer()
    


