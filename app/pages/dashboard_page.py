from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)

from app.widgets.metric_card import MetricCard


class DashboardPage(QWidget):
    """Home dashboard for CircuitVault."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()

    def setup_ui(self):
        """Create the dashboard interface."""

        main_layout = QVBoxLayout(self)

        # Page heading
        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Overview of your electronics inventory and connected devices."
        )

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Metric cards
        metrics_layout = QHBoxLayout()

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

        # Keep dashboard content toward the top.
        main_layout.addStretch()