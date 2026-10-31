"""
CircuitVault - Main Window
Version: 0.1.0

Main application window and sidebar navigation.
"""

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
)

from app.pages.dashboard_page import DashboardPage
from app.pages.components_page import ComponentsPage
from app.pages.devices_page import DevicesPage


class MainWindow(QMainWindow):
    """Main CircuitVault application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CircuitVault")
        self.resize(1200, 750)

        self.setup_ui()

    def setup_ui(self):
        """Create the main application interface."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)

        title = QLabel("CircuitVault")
        title.setObjectName("appTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sidebar_layout.addWidget(title)

        self.dashboard_button = QPushButton("Dashboard")
        self.components_button = QPushButton("Components")
        self.devices_button = QPushButton("Devices")
        self.sensors_button = QPushButton("Sensors")
        self.projects_button = QPushButton("Projects")

        self.navigation_buttons = [
            self.dashboard_button,
            self.components_button,
            self.devices_button,
            self.sensors_button,
            self.projects_button,
        ]

        for button in self.navigation_buttons:
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        version_label = QLabel("CircuitVault v0.1.0")
        version_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        sidebar_layout.addWidget(version_label)

        # Application pages
        self.pages = QStackedWidget()

        self.dashboard_page = DashboardPage()
        self.components_page = ComponentsPage()
        self.devices_page = DevicesPage()

        self.sensors_page = self.create_placeholder_page(
            "Sensors"
        )
        self.projects_page = self.create_placeholder_page(
            "Projects"
        )

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.components_page)
        self.pages.addWidget(self.devices_page)
        self.pages.addWidget(self.sensors_page)
        self.pages.addWidget(self.projects_page)

        for index, button in enumerate(self.navigation_buttons):
            button.clicked.connect(
                lambda checked=False, i=index: self.navigate_to(i)
            )

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages, 1)

        self.navigate_to(0)

    def navigate_to(self, index):
        """Navigate between application pages."""

        self.pages.setCurrentIndex(index)

        for button_index, button in enumerate(
            self.navigation_buttons
        ):
            button.setProperty(
                "active",
                button_index == index
            )

            button.style().unpolish(button)
            button.style().polish(button)

        if index == 0:
            self.dashboard_page.refresh_metrics()

        elif index == 1:
            self.components_page.refresh_components()

        elif index == 2:
            self.devices_page.refresh_devices()

    def create_placeholder_page(self, page_name):
        """Create a placeholder for future functionality."""

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel(page_name)
        title.setObjectName("pageTitle")

        description = QLabel(
            f"{page_name} functionality will be added "
            "in an upcoming development phase."
        )
        description.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()

        return page