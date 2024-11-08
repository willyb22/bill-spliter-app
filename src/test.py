import os, sys

from config import root_dir
module_path = os.path.join(
    root_dir,
    'src/'
)
if module_path not in sys.path:
    sys.path.append(module_path)

from config import db_config
from handler.handler import DataHandler

data_handler = DataHandler(db_config)

if __name__=="__main__":
    data_handler.cursor.execute("""select * from descriptions;""")

    rows = data_handler.cursor.fetchall()
    for row in rows:
        print(row)