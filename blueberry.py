"""
Blüberry - Colormap Editor

A simple dialog to create and edit colormaps.

Author: Derrick Hasterok
Date: 2024-06-20
"""
import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QSplashScreen, QMessageBox
from src.ColormapEditor import ColormapEditorDialog
from PyQt6.QtGui import QPixmap, QIcon
from src.config import ICONPATH


class BlueberryApp(ColormapEditorDialog):
    """
    Standalone wrapper around ColormapEditorDialog.

    Adds clean-exit behaviour: intercepts the window close button (and
    Escape) so that unsaved changes trigger a Save / Discard / Cancel
    prompt before the application quits.

    Keep ColormapEditorDialog free of this logic so it can be embedded as
    a plugin in other applications without forcing a full-process exit.
    """

    def closeEvent(self, event):
        if not self.model.undo_stack.isClean():
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "The colormap has unsaved changes. What would you like to do?",
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Save,
            )
            if reply == QMessageBox.StandardButton.Save:
                # Keep the window open while the save dialog runs.
                # save_colormap() calls self.accept() on success, which
                # emits finished() → app.quit() via the signal connection
                # in main().
                event.ignore()
                self.save_colormap()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
                QApplication.quit()
            else:  # Cancel
                event.ignore()
        else:
            event.accept()
            QApplication.quit()

    def reject(self):
        # Route Escape through closeEvent so the save prompt fires there too.
        self.close()


def main():
    app = QApplication(sys.argv)

    # Keep splash alive in main scope so it isn't garbage-collected before display
    pixmap = QPixmap(str(ICONPATH / 'blueberry_splash.png'))
    splash = QSplashScreen(pixmap)
    splash.setMask(pixmap.mask())
    splash.show()
    app.processEvents()  # flush events so splash renders before the window appears
    QTimer.singleShot(3000, splash.close)

    app.setWindowIcon(QIcon(str(ICONPATH / 'blueberry_64.svg')))

    existing_maps = {}
    dialog = BlueberryApp(existing_maps, title="Blüberry")

    # Quit the event loop when the dialog is accepted (saved) or finished.
    dialog.finished.connect(app.quit)

    dialog.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
