from .config import load_config, get_appdir
from .gui import initialize_gui

#if __name__ == "__main__":

# Load initial configuration
config_path = get_appdir()
config = load_config(config_path)

# Start the GUI
initialize_gui(config, config_path)
