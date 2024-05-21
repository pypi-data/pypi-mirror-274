import shutil
from datetime import datetime

# Backup file
def backup_file(file_path):
    backup_path = f"{file_path}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    shutil.copy2(file_path, backup_path)
    return backup_path