from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class MetricCard(QFrame):
    """Reusable dashboard card for displaying a metric."""

    def __init__(self, title, value="0", parent=None):
        super().__init__(parent)

        self.setObjectName("metricCard")
        self.setMinimumHeight(130)

        # Card layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)

        # Metric title
        self.title_label = QLabel(title)
        self.title_label.setObjectName("metricTitle")

        # Metric value
        self.value_label = QLabel(str(value))
        self.value_label.setObjectName("metricValue")

        self.value_label.setAlignment(Qt.AlignLeft)

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addStretch()

    def set_value(self, value):
        """Update the value displayed by the card."""
        self.value_label.setText(str(value))