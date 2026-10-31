"""
CircuitVault - Devices Page
Version: 0.1.0

Features:
    - Device inventory table
    - Add and edit devices
    - Delete devices
    - Search registered devices
    - Manual device status tracking
"""

import sqlite3

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QAbstractItemView,
    QDialog,
)

from app.dialogs.device_dialog import DeviceDialog
from database.device_repository import DeviceRepository


class DevicesPage(QWidget):
    """Registered device management page."""

    HEADERS = [
        "ID",
        "Name",
        "Device Type",
        "Hostname",
        "IP Address",
        "MAC Address",
        "Status",
        "Last Seen",
    ]

    def __init__(self, parent=None, repository=None):
        super().__init__(parent)

        self.repository = repository or DeviceRepository()

        self.setup_ui()
        self.refresh_devices()

    def setup_ui(self):
        """Create the device management interface."""

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Page header
        title = QLabel("Devices")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Manage registered electronic and embedded devices."
        )
        subtitle.setObjectName("pageSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search devices..."
        )
        self.search_input.setClearButtonEnabled(True)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setObjectName("refreshButton")

        self.add_button = QPushButton("+ Add Device")
        self.add_button.setObjectName("primaryButton")

        toolbar.addWidget(self.search_input, 1)
        toolbar.addWidget(self.refresh_button)
        toolbar.addWidget(self.add_button)

        main_layout.addLayout(toolbar)

        # Device table
        self.devices_table = QTableWidget()

        self.devices_table.setColumnCount(
            len(self.HEADERS)
        )

        self.devices_table.setHorizontalHeaderLabels(
            self.HEADERS
        )

        self.devices_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.devices_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.devices_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.devices_table.setAlternatingRowColors(True)
        self.devices_table.verticalHeader().setVisible(False)

        header = self.devices_table.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        header.setStretchLastSection(True)

        main_layout.addWidget(self.devices_table)

        # Bottom controls
        bottom_layout = QHBoxLayout()

        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.setObjectName("secondaryButton")

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setObjectName("dangerButton")

        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        self.count_label = QLabel("Registered Devices: 0")

        bottom_layout.addWidget(self.edit_button)
        bottom_layout.addWidget(self.delete_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.count_label)

        main_layout.addLayout(bottom_layout)

        # Signals
        self.search_input.textChanged.connect(
            self.refresh_devices
        )

        self.refresh_button.clicked.connect(
            self.refresh_devices
        )

        self.add_button.clicked.connect(
            self.add_device
        )

        self.edit_button.clicked.connect(
            self.edit_device
        )

        self.delete_button.clicked.connect(
            self.delete_device
        )

        self.devices_table.itemSelectionChanged.connect(
            self.update_button_states
        )

        self.devices_table.itemDoubleClicked.connect(
            self.edit_device
        )

    def refresh_devices(self):
        """Reload registered devices from SQLite."""

        try:
            search_text = self.search_input.text()

            devices = self.repository.search_devices(
                search_text
            )

            self.devices_table.setRowCount(0)

            for device in devices:
                row = self.devices_table.rowCount()
                self.devices_table.insertRow(row)

                values = [
                    device["id"],
                    device["name"],
                    device["device_type"],
                    device["hostname"],
                    device["ip_address"],
                    device["mac_address"],
                    device["status"],
                    device["last_seen"],
                ]

                for column, value in enumerate(values):
                    item = QTableWidgetItem(
                        str(value) if value is not None else ""
                    )

                    if column == 0:
                        item.setData(
                            Qt.ItemDataRole.EditRole,
                            int(value),
                        )

                    self.devices_table.setItem(
                        row,
                        column,
                        item,
                    )

            self.count_label.setText(
                f"Displayed Devices: {len(devices)}"
            )

            self.update_button_states()

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to load devices:\n{error}",
            )

    def get_selected_device_id(self):
        """Return the selected device ID."""

        row = self.devices_table.currentRow()

        if row < 0:
            return None

        item = self.devices_table.item(row, 0)

        if item is None:
            return None

        return int(item.text())

    def update_button_states(self):
        """Enable actions when a device is selected."""

        selected = self.get_selected_device_id() is not None

        self.edit_button.setEnabled(selected)
        self.delete_button.setEnabled(selected)

    def add_device(self):
        """Open the device registration dialog."""

        dialog = DeviceDialog(parent=self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            self.repository.add_device(
                dialog.get_device_data()
            )

            self.refresh_devices()

        except (sqlite3.Error, ValueError) as error:
            QMessageBox.critical(
                self,
                "Device Error",
                f"Unable to add device:\n{error}",
            )

    def edit_device(self, *_args):
        """Edit the selected registered device."""

        device_id = self.get_selected_device_id()

        if device_id is None:
            return

        try:
            device = self.repository.get_device(device_id)

            if device is None:
                QMessageBox.warning(
                    self,
                    "Device Not Found",
                    "The selected device no longer exists.",
                )
                self.refresh_devices()
                return

            dialog = DeviceDialog(
                device=device,
                parent=self,
            )

            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            updated = self.repository.update_device(
                device_id,
                dialog.get_device_data(),
            )

            if not updated:
                QMessageBox.warning(
                    self,
                    "Device Not Found",
                    "The selected device no longer exists.",
                )

            self.refresh_devices()

        except (sqlite3.Error, ValueError) as error:
            QMessageBox.critical(
                self,
                "Device Error",
                f"Unable to edit device:\n{error}",
            )

    def delete_device(self):
        """Delete a device after confirmation."""

        device_id = self.get_selected_device_id()

        if device_id is None:
            return

        response = QMessageBox.question(
            self,
            "Delete Device",
            "Delete this registered device?\n\n"
            "Associated sensor readings will also be deleted. "
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if response != QMessageBox.StandardButton.Yes:
            return

        try:
            self.repository.delete_device(device_id)
            self.refresh_devices()

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to delete device:\n{error}",
            )