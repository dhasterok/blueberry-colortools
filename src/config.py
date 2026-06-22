from pathlib import Path
from PyQt6.QtGui import QFont

# __file__ holds the full path to the current Python file
BASEDIR = Path(__file__).resolve().parent.parent

# Path to the resources directory
RESOURCE_PATH = BASEDIR / 'resources'

# Path to the icons directory
ICONPATH = RESOURCE_PATH / 'icons'

# # Path to the stylesheet directory
# STYLE_PATH = RESOURCE_PATH / 'styles'

def default_font():
    # set default font for application
    font = QFont()
    font.setPointSize(11)
    font.setStyleStrategy(QFont.StyleStrategy.PreferDefault)

    return font

# def load_stylesheet(filename):
#     replacements = {
#         '{icon_path}': str(ICONPATH.as_posix()),  # Ensure forward slashes
#     }
#     with open(STYLE_PATH / filename, "r", encoding="utf-8") as file:
#         stylesheet = file.read()
#     for key, value in replacements.items():
#         stylesheet = stylesheet.replace(key, value)
#     return stylesheet

# def get_top_parent(widget: QWidget):
#     """Walks up the parent chain until a QMainWindow or Workspace is found.
    