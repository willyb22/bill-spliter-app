# Import dependencies
import os, sys

from config import root_dir
module_path = os.path.join(
    root_dir,
    'src/'
)
if module_path not in sys.path:
    sys.path.append(module_path)

from gui.app import BillSplitterApp
from handler.handler import DataHandler

# Database configuration
from config import db_config
data_handler = DataHandler(db_config)

from PyQt5.QtWidgets import QApplication
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = BillSplitterApp(data_handler)
    window.show()
    sys.exit(app.exec_())