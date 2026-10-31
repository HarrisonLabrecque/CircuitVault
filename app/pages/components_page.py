"""
CircuitVault - Components Page
Version: 0.1.0

Features:
    - Component inventory table
    - Add components
    - Edit components
    - Delete components
    - Search inventory
    - Refresh inventory
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

from app.dialogs.component_dialog import ComponentDialog
from database.component_repository import ComponentRepository


class ComponentsPage(QWidget):
    """Electronics component inventory page."""

    HEADERS = [
        "ID",
        "Name",
        "Category",
        "Manufacturer",
        "Part Number",
        "Quantity",
        "Storage Location",
        "Datasheet",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

        self.repository = ComponentRepository()

        self.setup_ui()
        self.refresh_components()

    def setup_ui(self):
        """Create the components page interface."""

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # ----------------------------------------------------
        # Page Header
        # ----------------------------------------------------

        title = QLabel("Components")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Manage your electronic components and inventory."
        )
        subtitle.setObjectName("pageSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # ----------------------------------------------------
        # Toolbar
        # ----------------------------------------------------

        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search components..."
        )
        self.search_input.setClearButtonEnabled(True)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setObjectName("refreshButton")

        self.add_button = QPushButton("+ Add Component")
        self.add_button.setObjectName("primaryButton")

        toolbar_layout.addWidget(self.search_input, 1)
        toolbar_layout.addWidget(self.refresh_button)
        toolbar_layout.addWidget(self.add_button)

        main_layout.addLayout(toolbar_layout)

        # ----------------------------------------------------
        # Components Table
        # ----------------------------------------------------

        self.components_table = QTableWidget()

        self.components_table.setColumnCount(
            len(self.HEADERS)
        )

        self.components_table.setHorizontalHeaderLabels(
            self.HEADERS
        )

        self.components_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.components_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.components_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.components_table.setAlternatingRowColors(True)

        self.components_table.verticalHeader().setVisible(False)

        self.components_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.components_table.horizontalHeader().setStretchLastSection(
            True
        )

        main_layout.addWidget(self.components_table)

        # ----------------------------------------------------
        # Bottom Toolbar
        # ----------------------------------------------------

        bottom_layout = QHBoxLayout()

        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.setObjectName("secondaryButton")

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setObjectName("dangerButton")

        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        self.count_label = QLabel("Total Component Records: 0")

        bottom_layout.addWidget(self.edit_button)
        bottom_layout.addWidget(self.delete_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.count_label)

        main_layout.addLayout(bottom_layout)

        # ----------------------------------------------------
        # Signal Connections
        # ----------------------------------------------------

        self.search_input.textChanged.connect(
            self.refresh_components
        )

        self.refresh_button.clicked.connect(
            self.refresh_components
        )

        self.add_button.clicked.connect(
            self.add_component
        )

        self.edit_button.clicked.connect(
            self.edit_component
        )

        self.delete_button.clicked.connect(
            self.delete_component
        )

        self.components_table.itemSelectionChanged.connect(
            self.update_button_states
        )

        self.components_table.itemDoubleClicked.connect(
            self.edit_component
        )

    def refresh_components(self):
        """Reload components from SQLite."""

        try:
            search_text = self.search_input.text()

            components = self.repository.search_components(
                search_text
            )

            self.components_table.setRowCount(0)

            for component in components:
                row = self.components_table.rowCount()
                self.components_table.insertRow(row)

                values = [
                    component["id"],
                    component["name"],
                    component["category"],
                    component["manufacturer"],
                    component["part_number"],
                    component["quantity"],
                    component["storage_location"],
                    component["datasheet"],
                ]

                for column, value in enumerate(values):
                    item = QTableWidgetItem(
                        str(value) if value is not None else ""
                    )

                    if column in (0, 5):
                        item.setData(
                            Qt.ItemDataRole.EditRole,
                            int(value),
                        )

                    self.components_table.setItem(
                        row,
                        column,
                        item,
                    )

            self.count_label.setText(
                f"Displayed Component Records: {len(components)}"
            )

            self.update_button_states()

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to load components:\n{error}",
            )

    def get_selected_component_id(self):
        """Return the ID of the selected component."""

        selected_row = self.components_table.currentRow()

        if selected_row < 0:
            return None

        item = self.components_table.item(selected_row, 0)

        if item is None:
            return None

        return int(item.text())

    def update_button_states(self):
        """Enable actions when a component is selected."""

        has_selection = (
            self.get_selected_component_id() is not None
        )

        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

    def add_component(self):
        """Open the Add Component dialog."""

        dialog = ComponentDialog(parent=self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            self.repository.add_component(
                dialog.get_component_data()
            )

            self.refresh_components()

        except (sqlite3.Error, ValueError) as error:
            QMessageBox.critical(
                self,
                "Component Error",
                f"Unable to add component:\n{error}",
            )

    def edit_component(self, *_args):
        """Edit the selected component."""

        component_id = self.get_selected_component_id()

        if component_id is None:
            return

        try:
            component = self.repository.get_component(
                component_id
            )

            if component is None:
                QMessageBox.warning(
                    self,
                    "Component Not Found",
                    "The selected component no longer exists.",
                )
                self.refresh_components()
                return

            dialog = ComponentDialog(
                component=component,
                parent=self,
            )

            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            updated = self.repository.update_component(
                component_id,
                dialog.get_component_data(),
            )

            if not updated:
                QMessageBox.warning(
                    self,
                    "Component Not Found",
                    "The selected component no longer exists.",
                )

            self.refresh_components()

        except (sqlite3.Error, ValueError) as error:
            QMessageBox.critical(
                self,
                "Component Error",
                f"Unable to edit component:\n{error}",
            )

    def delete_component(self):
        """Delete the selected component after confirmation."""

        component_id = self.get_selected_component_id()

        if component_id is None:
            return

        response = QMessageBox.question(
            self,
            "Delete Component",
            "Are you sure you want to delete this component?\n\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if response != QMessageBox.StandardButton.Yes:
            return

        try:
            self.repository.delete_component(component_id)
            self.refresh_components()

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to delete component:\n{error}",
            )