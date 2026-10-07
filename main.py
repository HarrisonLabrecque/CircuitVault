import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow


def main():
    """Start the CircuitVault application."""

    app = QApplication(sys.argv)

    # Application information
    app.setApplicationName("CircuitVault")
    app.setApplicationVersion("0.1.0")

    # Load the CircuitVault stylesheet
    stylesheet_path = Path(__file__).parent / "styles" / "main.qss"

    with stylesheet_path.open("r", encoding="utf-8") as stylesheet:
        app.setStyleSheet(stylesheet.read())

    # Create and display the main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()