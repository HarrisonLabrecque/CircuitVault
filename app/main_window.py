from app.pages.dashboard_page import DashboardPage

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
)
from PySide6.QtCore import Qt




class MainWindow(QMainWindow):
    """Main application window for CircuitVault."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CircuitVault")
        self.resize(1200, 750)

        self.setup_ui()

    def setup_ui(self):
        """Create the main user interface."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # -------------------------
        # Sidebar
        # -------------------------

        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)

        # Application title
        title = QLabel("CircuitVault")
        title.setAlignment(Qt.AlignCenter)

        sidebar_layout.addWidget(title)

        # Navigation buttons
        self.dashboard_button = QPushButton("Dashboard")
        self.components_button = QPushButton("Components")
        self.devices_button = QPushButton("Devices")
        self.sensors_button = QPushButton("Sensors")
        self.projects_button = QPushButton("Projects")

        sidebar_layout.addWidget(self.dashboard_button)
        sidebar_layout.addWidget(self.components_button)
        sidebar_layout.addWidget(self.devices_button)
        sidebar_layout.addWidget(self.sensors_button)
        sidebar_layout.addWidget(self.projects_button)

        # Push navigation buttons toward the top.
        sidebar_layout.addStretch()

        # Version information
        version_label = QLabel("CircuitVault v0.1.0")
        version_label.setAlignment(Qt.AlignCenter)

        sidebar_layout.addWidget(version_label)

        # -------------------------
        # Page container
        # -------------------------

        self.pages = QStackedWidget()

        self.dashboard_page = DashboardPage()
        self.components_page = self.create_page("Components")
        self.devices_page = self.create_page("Devices")
        self.sensors_page = self.create_page("Sensors")
        self.projects_page = self.create_page("Projects")

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.components_page)
        self.pages.addWidget(self.devices_page)
        self.pages.addWidget(self.sensors_page)
        self.pages.addWidget(self.projects_page)

        # -------------------------
        # Navigation events
        # -------------------------

        self.dashboard_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        self.components_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        self.devices_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        self.sensors_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(3)
        )

        self.projects_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(4)
        )

        # Add sidebar and pages to main layout.
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

    def create_page(self, page_name):
        """Create a temporary placeholder page."""

        page = QWidget()

        layout = QVBoxLayout(page)

        title = QLabel(page_name)
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        return page