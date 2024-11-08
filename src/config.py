import os
from dotenv import load_dotenv

load_dotenv('.env', override=True)

root_dir = os.getenv('PROJECT_DIR')

db_config = {
    'db_file': os.path.join(
        root_dir,
        os.getenv('DB_FILE')
    ),
    'migration_dir': os.path.join(
        root_dir,
        'db\\migrations'
    ),
    'view_dir': os.path.join(
        root_dir, 
        'db\\view'
    )
}