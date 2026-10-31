"""
CircuitVault - Device Dialog
Version: 0.1.0

Form for registering and editing devices.
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDialogButtonBox,
    QMessageBox,
)

from database.device_repository import DeviceRepository


DEVICE_TYPES = [
    "Raspberry Pi",
    "ESP32",
    "Arduino",
    "Raspberry Pi Pico",
    "Microcontroller",
    "Single Board Computer",
    "Sensor Node",
    "Other",
]


class DeviceDialog(QDialog):
    """Device registration and editing dialog."""

    def __init__(self, device=None, parent=None):
        super().__init__(parent)

        self.device = device

        self.setWindowTitle(
            "Edit Device" if device else "Add Device"
        )
        self.setMinimumWidth(450)

        self.setup_ui()

        if device:
            self.load_device(device)

    def setup_ui(self):
        """Build the device form."""

        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Robot Pi")

        self.type_input = QComboBox()
        self.type_input.addItems(DEVICE_TYPES)

        self.hostname_input = QLineEdit()
        self.hostname_input.setPlaceholderText(
            "e.g. robotpi.local"
        )

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText(
            "e.g. 192.168.1.20"
        )

        self.mac_input = QLineEdit()
        self.mac_input.setPlaceholderText(
            "Optional MAC address"
        )

        self.status_input = QComboBox()
        self.status_input.addItems([
            "Offline",
            "Online",
        ])

        form_layout.addRow("Device Name *", self.name_input)
        form_layout.addRow("Device Type *", self.type_input)
        form_layout.addRow("Hostname", self.hostname_input)
        form_layout.addRow("IP Address", self.ip_input)
        form_layout.addRow("MAC Address", self.mac_input)
        form_layout.addRow("Status", self.status_input)

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

    def load_device(self, device):
        """Populate the dialog with an existing device."""

        self.name_input.setText(device["name"])

        device_type = device["device_type"]

        if self.type_input.findText(device_type) == -1:
            self.type_input.addItem(device_type)

        self.type_input.setCurrentText(device_type)

        self.hostname_input.setText(
            device.get("hostname") or ""
        )

        self.ip_input.setText(
            device.get("ip_address") or ""
        )

        self.mac_input.setText(
            device.get("mac_address") or ""
        )

        self.status_input.setCurrentText(
            device.get("status") or "Offline"
        )

    def get_device_data(self):
        """Return the device form data."""

        return {
            "name": self.name_input.text().strip(),
            "device_type": self.type_input.currentText(),
            "hostname": self.hostname_input.text().strip(),
            "ip_address": self.ip_input.text().strip(),
            "mac_address": self.mac_input.text().strip(),
            "status": self.status_input.currentText(),
        }

    def validate_and_accept(self):
        """Validate the form before accepting."""

        try:
            DeviceRepository.validate_device(
                self.get_device_data()
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Validation Error",
                str(error),
            )
            return

        self.accept()