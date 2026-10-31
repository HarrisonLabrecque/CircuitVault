"""
CircuitVault - Dashboard Page
Version: 0.1.0

Displays:
    - Total components
    - Known devices
    - Online devices
    - Sensor readings
"""

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
)

from app.widgets.metric_card import MetricCard
from database.database import DatabaseManager


# ============================================================
# DASHBOARD PAGE
# ============================================================

class DashboardPage(QWidget):
    """Main dashboard for CircuitVault."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.database = DatabaseManager()

        self.setup_ui()
        self.refresh_metrics()

    # --------------------------------------------------------
    # User Interface
    # --------------------------------------------------------

    def setup_ui(self):
        """Create the dashboard interface."""

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # ----------------------------------------------------
        # Dashboard Header
        # ----------------------------------------------------

        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()

        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Overview of your electronics inventory and connected devices."
        )

        subtitle.setObjectName("pageSubtitle")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        # Refresh button
        self.refresh_button = QPushButton("Refresh")

        self.refresh_button.setObjectName("refreshButton")

        self.refresh_button.clicked.connect(
            self.refresh_metrics
        )

        header_layout.addWidget(self.refresh_button)

        main_layout.addLayout(header_layout)

        # ----------------------------------------------------
        # Dashboard Metric Cards
        # ----------------------------------------------------

        metrics_layout = QHBoxLayout()

        metrics_layout.setSpacing(15)

        self.components_card = MetricCard(
            "Total Components"
        )

        self.devices_card = MetricCard(
            "Known Devices"
        )

        self.online_card = MetricCard(
            "Devices Online"
        )

        self.readings_card = MetricCard(
            "Sensor Readings"
        )

        metrics_layout.addWidget(self.components_card)
        metrics_layout.addWidget(self.devices_card)
        metrics_layout.addWidget(self.online_card)
        metrics_layout.addWidget(self.readings_card)

        main_layout.addLayout(metrics_layout)

        # ----------------------------------------------------
        # Future Dashboard Sections
        # ----------------------------------------------------

        section_title = QLabel("System Overview")

        section_title.setObjectName("sectionTitle")

        main_layout.addWidget(section_title)

        overview_label = QLabel(
            "Device monitoring and sensor activity will appear here "
            "in future CircuitVault versions."
        )

        overview_label.setWordWrap(True)
        overview_label.setObjectName("overviewLabel")

        main_layout.addWidget(overview_label)

        main_layout.addStretch()

    # --------------------------------------------------------
    # Dashboard Metrics
    # --------------------------------------------------------

    def refresh_metrics(self):
        """Retrieve dashboard statistics from SQLite."""

        try:
            statistics = self.database.get_dashboard_statistics()

            self.components_card.set_value(
                statistics["total_components"]
            )

            self.devices_card.set_value(
                statistics["known_devices"]
            )

            self.online_card.set_value(
                statistics["online_devices"]
            )

            self.readings_card.set_value(
                statistics["sensor_readings"]
            )

        except Exception as error:

            QMessageBox.warning(
                self,
                "Database Error",
                f"Unable to load dashboard statistics:\n{error}"
            )