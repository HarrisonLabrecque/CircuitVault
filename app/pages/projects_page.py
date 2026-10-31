"""
CircuitVault - Projects Page
Version: 0.1.0

Features:
    - Project CRUD
    - Project search
    - Component assignments
    - Project component details
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

from app.dialogs.project_dialog import ProjectDialog
from app.dialogs.project_component_dialog import (
    ProjectComponentDialog,
)
from database.project_repository import ProjectRepository


class ProjectsPage(QWidget):
    """Project and component assignment management."""

    PROJECT_HEADERS = [
        "ID",
        "Name",
        "Status",
        "Description",
        "Component Types",
        "Assigned Quantity",
    ]

    COMPONENT_HEADERS = [
        "Component ID",
        "Name",
        "Category",
        "Inventory Quantity",
        "Assigned Quantity",
    ]

    def __init__(self, parent=None, repository=None):
        super().__init__(parent)

        self.repository = repository or ProjectRepository()

        self.setup_ui()
        self.refresh_projects()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        title = QLabel("Projects")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Organize electronics projects and their components."
        )
        subtitle.setObjectName("pageSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Project toolbar
        toolbar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search projects..."
        )
        self.search_input.setClearButtonEnabled(True)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setObjectName("refreshButton")

        self.add_button = QPushButton("+ Add Project")
        self.add_button.setObjectName("primaryButton")

        toolbar.addWidget(self.search_input, 1)
        toolbar.addWidget(self.refresh_button)
        toolbar.addWidget(self.add_button)

        main_layout.addLayout(toolbar)

        # Projects table
        self.projects_table = QTableWidget()
        self.projects_table.setColumnCount(
            len(self.PROJECT_HEADERS)
        )
        self.projects_table.setHorizontalHeaderLabels(
            self.PROJECT_HEADERS
        )

        self.configure_table(self.projects_table)
        main_layout.addWidget(self.projects_table, 3)

        # Project controls
        project_controls = QHBoxLayout()

        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.setObjectName("secondaryButton")

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setObjectName("dangerButton")

        self.count_label = QLabel("Displayed Projects: 0")

        project_controls.addWidget(self.edit_button)
        project_controls.addWidget(self.delete_button)
        project_controls.addStretch()
        project_controls.addWidget(self.count_label)

        main_layout.addLayout(project_controls)

        # Assigned components
        components_title = QLabel("Assigned Components")
        components_title.setObjectName("sectionTitle")

        main_layout.addWidget(components_title)

        self.components_table = QTableWidget()
        self.components_table.setColumnCount(
            len(self.COMPONENT_HEADERS)
        )
        self.components_table.setHorizontalHeaderLabels(
            self.COMPONENT_HEADERS
        )

        self.configure_table(self.components_table)
        main_layout.addWidget(self.components_table, 2)

        # Component assignment controls
        component_controls = QHBoxLayout()

        self.assign_button = QPushButton("+ Assign Component")
        self.assign_button.setObjectName("primaryButton")

        self.remove_button = QPushButton("Remove Assignment")
        self.remove_button.setObjectName("dangerButton")

        component_controls.addWidget(self.assign_button)
        component_controls.addWidget(self.remove_button)
        component_controls.addStretch()

        main_layout.addLayout(component_controls)

        # Initial button states
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.assign_button.setEnabled(False)
        self.remove_button.setEnabled(False)

        # Signals
        self.search_input.textChanged.connect(
            self.refresh_projects
        )

        self.refresh_button.clicked.connect(
            self.refresh_projects
        )

        self.add_button.clicked.connect(
            self.add_project
        )

        self.edit_button.clicked.connect(
            self.edit_project
        )

        self.delete_button.clicked.connect(
            self.delete_project
        )

        self.assign_button.clicked.connect(
            self.assign_component
        )

        self.remove_button.clicked.connect(
            self.remove_component
        )

        self.projects_table.itemSelectionChanged.connect(
            self.on_project_selection_changed
        )

        self.components_table.itemSelectionChanged.connect(
            self.update_button_states
        )

        self.projects_table.itemDoubleClicked.connect(
            self.edit_project
        )

    @staticmethod
    def configure_table(table):
        table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)

        header = table.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        header.setStretchLastSection(True)

    @staticmethod
    def populate_row(table, row, values):
        table.insertRow(row)

        for column, value in enumerate(values):
            item = QTableWidgetItem(
                str(value) if value is not None else ""
            )

            if column == 0:
                item.setData(
                    Qt.ItemDataRole.EditRole,
                    int(value),
                )

            table.setItem(row, column, item)

    def refresh_projects(self):
        """Reload projects and clear stale selections."""

        try:
            projects = self.repository.search_projects(
                self.search_input.text()
            )

            self.projects_table.setRowCount(0)
            self.components_table.setRowCount(0)

            for project in projects:
                row = self.projects_table.rowCount()

                self.populate_row(
                    self.projects_table,
                    row,
                    [
                        project["id"],
                        project["name"],
                        project["status"],
                        project["description"],
                        project["component_types"],
                        project["assigned_quantity"],
                    ],
                )

            self.count_label.setText(
                f"Displayed Projects: {len(projects)}"
            )

            self.update_button_states()

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to load projects:\n{error}",
            )

    def get_selected_project_id(self):
        row = self.projects_table.currentRow()

        if row < 0:
            return None

        item = self.projects_table.item(row, 0)

        return int(item.text()) if item else None

    def get_selected_component_id(self):
        row = self.components_table.currentRow()

        if row < 0:
            return None

        item = self.components_table.item(row, 0)

        return int(item.text()) if item else None

    def update_button_states(self):
        project_selected = (
            self.get_selected_project_id() is not None
        )
        component_selected = (
            self.get_selected_component_id() is not None
        )

        self.edit_button.setEnabled(project_selected)
        self.delete_button.setEnabled(project_selected)
        self.assign_button.setEnabled(project_selected)

        self.remove_button.setEnabled(
            project_selected and component_selected
        )

    def on_project_selection_changed(self):
        """Load components associated with the selected project."""

        self.refresh_project_components()
        self.update_button_states()

    def refresh_project_components(self):
        project_id = self.get_selected_project_id()

        self.components_table.setRowCount(0)

        if project_id is None:
            self.update_button_states()
            return

        try:
            components = self.repository.get_project_components(
                project_id
            )

            for component in components:
                row = self.components_table.rowCount()

                self.populate_row(
                    self.components_table,
                    row,
                    [
                        component["component_id"],
                        component["name"],
                        component["category"],
                        component["inventory_quantity"],
                        component["quantity_used"],
                    ],
                )

            self.update_button_states()

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to load assigned components:\n{error}",
            )

    def add_project(self):
        dialog = ProjectDialog(parent=self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            self.repository.add_project(
                dialog.get_project_data()
            )
            self.refresh_projects()

        except (sqlite3.Error, ValueError) as error:
            QMessageBox.critical(
                self,
                "Project Error",
                f"Unable to add project:\n{error}",
            )

    def edit_project(self, *_args):
        project_id = self.get_selected_project_id()

        if project_id is None:
            return

        try:
            project = self.repository.get_project(project_id)

            if project is None:
                self.refresh_projects()
                return

            dialog = ProjectDialog(
                project=project,
                parent=self,
            )

            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            self.repository.update_project(
                project_id,
                dialog.get_project_data(),
            )
            self.refresh_projects()

        except (sqlite3.Error, ValueError) as error:
            QMessageBox.critical(
                self,
                "Project Error",
                f"Unable to edit project:\n{error}",
            )

    def delete_project(self):
        project_id = self.get_selected_project_id()

        if project_id is None:
            return

        response = QMessageBox.question(
            self,
            "Delete Project",
            "Delete this project and its component assignments?\n\n"
            "Inventory components will not be deleted.",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if response != QMessageBox.StandardButton.Yes:
            return

        try:
            self.repository.delete_project(project_id)
            self.refresh_projects()

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to delete project:\n{error}",
            )

    def assign_component(self):
        project_id = self.get_selected_project_id()

        if project_id is None:
            return

        try:
            components = self.repository.get_available_components()

            if not components:
                QMessageBox.information(
                    self,
                    "No Inventory Components",
                    "Add components to your inventory first.",
                )
                return

            dialog = ProjectComponentDialog(
                repository=self.repository,
                parent=self,
            )

            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            data = dialog.get_assignment_data()

            self.repository.assign_component(
                project_id,
                data["component_id"],
                data["quantity_used"],
            )

            self.refresh_projects()
            self.select_project(project_id)

        except (sqlite3.Error, ValueError) as error:
            QMessageBox.critical(
                self,
                "Assignment Error",
                f"Unable to assign component:\n{error}",
            )

    def remove_component(self):
        project_id = self.get_selected_project_id()
        component_id = self.get_selected_component_id()

        if project_id is None or component_id is None:
            return

        response = QMessageBox.question(
            self,
            "Remove Component Assignment",
            "Remove this component from the project?\n\n"
            "The inventory record will remain unchanged.",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if response != QMessageBox.StandardButton.Yes:
            return

        try:
            self.repository.remove_component(
                project_id,
                component_id,
            )

            self.refresh_projects()
            self.select_project(project_id)

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to remove assignment:\n{error}",
            )

    def select_project(self, project_id):
        """Restore a project selection after refreshing."""

        for row in range(self.projects_table.rowCount()):
            item = self.projects_table.item(row, 0)

            if item and int(item.text()) == project_id:
                self.projects_table.selectRow(row)
                return