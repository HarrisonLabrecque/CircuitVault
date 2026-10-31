"""
CircuitVault - Sensors Page
Version: 0.1.0

Features:
    - Sensor readings table
    - Add sensor readings
    - Edit sensor readings
    - Delete sensor readings
    - Search measurements
    - Refresh readings
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

from app.dialogs.sensor_reading_dialog import SensorReadingDialog
from database.sensor_repository import SensorRepository


class SensorsPage(QWidget):
    """Manage stored sensor measurements."""

    HEADERS = [
        "ID",
        "Device",
        "Sensor",
        "Measurement",
        "Value",
        "Unit",
        "Timestamp",
    ]

    def __init__(self, parent=None, repository=None):
        super().__init__(parent)

        self.repository = repository or SensorRepository()

        self.setup_ui()
        self.refresh_readings()

    def setup_ui(self):
        """Create the Sensors page interface."""

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Page header
        title = QLabel("Sensors")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Manage sensor measurements from registered devices."
        )
        subtitle.setObjectName("pageSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search sensor readings..."
        )
        self.search_input.setClearButtonEnabled(True)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setObjectName("refreshButton")

        self.add_button = QPushButton("+ Add Reading")
        self.add_button.setObjectName("primaryButton")

        toolbar.addWidget(self.search_input, 1)
        toolbar.addWidget(self.refresh_button)
        toolbar.addWidget(self.add_button)

        main_layout.addLayout(toolbar)

        # Readings table
        self.readings_table = QTableWidget()

        self.readings_table.setColumnCount(
            len(self.HEADERS)
        )

        self.readings_table.setHorizontalHeaderLabels(
            self.HEADERS
        )

        self.readings_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.readings_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.readings_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.readings_table.setAlternatingRowColors(True)
        self.readings_table.verticalHeader().setVisible(False)

        header = self.readings_table.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        header.setStretchLastSection(True)

        main_layout.addWidget(self.readings_table)

        # Bottom controls
        bottom_layout = QHBoxLayout()

        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.setObjectName("secondaryButton")

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setObjectName("dangerButton")

        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        self.count_label = QLabel("Displayed Readings: 0")

        bottom_layout.addWidget(self.edit_button)
        bottom_layout.addWidget(self.delete_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.count_label)

        main_layout.addLayout(bottom_layout)

        # Signals
        self.search_input.textChanged.connect(
            self.refresh_readings
        )

        self.refresh_button.clicked.connect(
            self.refresh_readings
        )

        self.add_button.clicked.connect(
            self.add_reading
        )

        self.edit_button.clicked.connect(
            self.edit_reading
        )

        self.delete_button.clicked.connect(
            self.delete_reading
        )

        self.readings_table.itemSelectionChanged.connect(
            self.update_button_states
        )

        self.readings_table.itemDoubleClicked.connect(
            self.edit_reading
        )

    def refresh_readings(self):
        """Reload sensor measurements from SQLite."""

        try:
            readings = self.repository.search_readings(
                self.search_input.text()
            )

            self.readings_table.setRowCount(0)

            for reading in readings:
                row = self.readings_table.rowCount()
                self.readings_table.insertRow(row)

                values = [
                    reading["id"],
                    reading["device_name"],
                    reading["sensor_name"],
                    reading["metric"],
                    reading["value"],
                    reading["unit"],
                    reading["timestamp"],
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

                    self.readings_table.setItem(
                        row,
                        column,
                        item,
                    )

            self.count_label.setText(
                f"Displayed Readings: {len(readings)}"
            )

            self.update_button_states()

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to load sensor readings:\n{error}",
            )

    def get_selected_reading_id(self):
        """Return the selected reading ID."""

        row = self.readings_table.currentRow()

        if row < 0:
            return None

        item = self.readings_table.item(row, 0)

        if item is None:
            return None

        return int(item.text())

    def update_button_states(self):
        """Enable actions when a reading is selected."""

        selected = self.get_selected_reading_id() is not None

        self.edit_button.setEnabled(selected)
        self.delete_button.setEnabled(selected)

    def add_reading(self):
        """Open the Add Sensor Reading dialog."""

        try:
            devices = self.repository.get_registered_devices()

            if not devices:
                QMessageBox.information(
                    self,
                    "No Registered Devices",
                    "Register a device on the Devices page "
                    "before adding sensor readings.",
                )
                return

            dialog = SensorReadingDialog(
                repository=self.repository,
                parent=self,
            )

            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            self.repository.add_reading(
                dialog.get_reading_data()
            )

            self.refresh_readings()

        except (sqlite3.Error, ValueError) as error:
            QMessageBox.critical(
                self,
                "Sensor Error",
                f"Unable to add sensor reading:\n{error}",
            )

    def edit_reading(self, *_args):
        """Edit the selected sensor measurement."""

        reading_id = self.get_selected_reading_id()

        if reading_id is None:
            return

        try:
            reading = self.repository.get_reading(reading_id)

            if reading is None:
                QMessageBox.warning(
                    self,
                    "Reading Not Found",
                    "The selected reading no longer exists.",
                )
                self.refresh_readings()
                return

            dialog = SensorReadingDialog(
                repository=self.repository,
                reading=reading,
                parent=self,
            )

            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            updated = self.repository.update_reading(
                reading_id,
                dialog.get_reading_data(),
            )

            if not updated:
                QMessageBox.warning(
                    self,
                    "Reading Not Found",
                    "The selected reading no longer exists.",
                )

            self.refresh_readings()

        except (sqlite3.Error, ValueError) as error:
            QMessageBox.critical(
                self,
                "Sensor Error",
                f"Unable to edit sensor reading:\n{error}",
            )

    def delete_reading(self):
        """Delete a sensor measurement after confirmation."""

        reading_id = self.get_selected_reading_id()

        if reading_id is None:
            return

        response = QMessageBox.question(
            self,
            "Delete Sensor Reading",
            "Are you sure you want to delete this reading?\n\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if response != QMessageBox.StandardButton.Yes:
            return

        try:
            self.repository.delete_reading(reading_id)
            self.refresh_readings()

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to delete sensor reading:\n{error}",
            )