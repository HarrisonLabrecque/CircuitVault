"""
CircuitVault - Sensor Reading Dialog
Version: 0.1.0

Form for creating and editing sensor measurements.
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QLineEdit,
    QDoubleSpinBox,
    QDialogButtonBox,
    QMessageBox,
)

from database.sensor_repository import SensorRepository


MEASUREMENT_TYPES = [
    "Acceleration X",
    "Acceleration Y",
    "Acceleration Z",
    "Gyroscope X",
    "Gyroscope Y",
    "Gyroscope Z",
    "Temperature",
    "Humidity",
    "Pressure",
    "Distance",
    "Voltage",
    "Current",
    "Light Intensity",
    "Other",
]


class SensorReadingDialog(QDialog):
    """Dialog for adding or editing sensor readings."""

    def __init__(self, repository, reading=None, parent=None):
        super().__init__(parent)

        self.repository = repository
        self.reading = reading

        self.setWindowTitle(
            "Edit Sensor Reading" if reading else "Add Sensor Reading"
        )
        self.setMinimumWidth(450)

        self.setup_ui()

        if reading:
            self.load_reading(reading)

    def setup_ui(self):
        """Build the sensor reading form."""

        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.device_input = QComboBox()

        for device in self.repository.get_registered_devices():
            label = (
                f"{device['name']} "
                f"({device['device_type']}, ID: {device['id']})"
            )

            self.device_input.addItem(
                label,
                userData=device["id"],
            )

        self.sensor_input = QLineEdit()
        self.sensor_input.setPlaceholderText(
            "e.g. MPU6050"
        )

        self.metric_input = QComboBox()
        self.metric_input.setEditable(True)
        self.metric_input.addItems(MEASUREMENT_TYPES)

        self.value_input = QDoubleSpinBox()
        self.value_input.setRange(-1_000_000_000, 1_000_000_000)
        self.value_input.setDecimals(6)
        self.value_input.setSingleStep(0.1)

        self.unit_input = QLineEdit()
        self.unit_input.setPlaceholderText(
            "e.g. g, °C, m/s²"
        )

        form_layout.addRow("Device *", self.device_input)
        form_layout.addRow("Sensor Name *", self.sensor_input)
        form_layout.addRow("Measurement *", self.metric_input)
        form_layout.addRow("Value *", self.value_input)
        form_layout.addRow("Unit", self.unit_input)

        main_layout.addLayout(form_layout)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(
            self.validate_and_accept
        )
        self.buttons.rejected.connect(self.reject)

        main_layout.addWidget(self.buttons)

    def load_reading(self, reading):
        """Populate the form with existing measurement data."""

        index = self.device_input.findData(
            reading["device_id"]
        )

        if index >= 0:
            self.device_input.setCurrentIndex(index)

        self.sensor_input.setText(
            reading["sensor_name"]
        )

        metric = reading["metric"]

        if self.metric_input.findText(metric) == -1:
            self.metric_input.addItem(metric)

        self.metric_input.setCurrentText(metric)

        self.value_input.setValue(
            float(reading["value"])
        )

        self.unit_input.setText(
            reading.get("unit") or ""
        )

    def get_reading_data(self):
        """Return the form data as a dictionary."""

        return {
            "device_id": self.device_input.currentData(),
            "sensor_name": self.sensor_input.text().strip(),
            "metric": self.metric_input.currentText().strip(),
            "value": self.value_input.value(),
            "unit": self.unit_input.text().strip(),
        }

    def validate_and_accept(self):
        """Validate the form before saving."""

        try:
            SensorRepository.validate_reading(
                self.get_reading_data()
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Validation Error",
                str(error),
            )
            return

        self.accept()