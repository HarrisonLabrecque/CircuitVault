"""
CircuitVault - Application Entry Point
Version: 0.1.0

Initializes:
    - QApplication
    - SQLite database
    - Application stylesheet
    - Main window

Supports:
    - Development execution
    - PyInstaller one-file executable
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
)

from app.main_window import MainWindow
from database.database import DatabaseManager


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

APP_NAME = "CircuitVault"
APP_VERSION = "0.1.0"


def get_resource_path(relative_path):
    """
    Return the path to an application resource.

    Development:
        Resources are loaded from the project directory.

    PyInstaller:
        Resources are loaded from the bundled extraction directory.
    """

    if getattr(sys, "frozen", False):
        base_dir = Path(sys._MEIPASS)
    else:
        base_dir = Path(__file__).resolve().parent

    return base_dir / relative_path


STYLESHEET_PATH = get_resource_path("styles/main.qss")


# ============================================================
# APPLICATION STARTUP
# ============================================================

def main():
    """Start the CircuitVault desktop application."""

    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)

    # --------------------------------------------------------
    # Initialize SQLite Database
    # --------------------------------------------------------

    try:
        database = DatabaseManager()
        database.initialize_database()

    except Exception as error:

        QMessageBox.critical(
            None,
            "Database Initialization Error",
            (
                "Unable to initialize CircuitVault database:\n\n"
                f"{error}"
            )
        )

        return 1

    # --------------------------------------------------------
    # Load Application Stylesheet
    # --------------------------------------------------------

    if STYLESHEET_PATH.is_file():

        try:
            with STYLESHEET_PATH.open(
                "r",
                encoding="utf-8"
            ) as stylesheet:

                app.setStyleSheet(stylesheet.read())

        except OSError as error:

            print(
                f"Unable to load CircuitVault stylesheet: {error}",
                file=sys.stderr
            )

    else:

        print(
            f"Warning: CircuitVault stylesheet not found: "
            f"{STYLESHEET_PATH}",
            file=sys.stderr
        )

    # --------------------------------------------------------
    # Create Main Window
    # --------------------------------------------------------

    window = MainWindow()

    window.show()

    return app.exec()


# ============================================================
# MAIN ENTRY POINT
# ============================================================

if __name__ == "__main__":
    sys.exit(main())