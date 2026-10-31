"""
CircuitVault - Application Entry Point
Version: 0.1.0

Initializes:
    - QApplication
    - SQLite database
    - Application stylesheet
    - Main window
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

BASE_DIR = Path(__file__).resolve().parent

STYLESHEET_PATH = BASE_DIR / "styles" / "main.qss"


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

    database = DatabaseManager()

    try:
        database.initialize_database()

    except Exception as error:

        QMessageBox.critical(
            None,
            "Database Initialization Error",
            f"Unable to initialize CircuitVault database:\n{error}"
        )

        return 1

    # --------------------------------------------------------
    # Load Application Stylesheet
    # --------------------------------------------------------

    if STYLESHEET_PATH.exists():

        try:
            with STYLESHEET_PATH.open(
                "r",
                encoding="utf-8"
            ) as stylesheet:

                app.setStyleSheet(stylesheet.read())

        except OSError as error:
            print(f"Unable to load stylesheet: {error}")

    else:
        print("Warning: CircuitVault stylesheet not found.")

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