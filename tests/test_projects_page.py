"""
CircuitVault - Projects Page
Version: 0.1.0

Features:
    - Project CRUD operations
    - Project searching
    - Project status tracking
    - Component assignments
    - Component assignment removal
    - Project and component selection management
    - Automatic table refreshing
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
    """Manage electronics projects and component assignments."""

    # ========================================================
    # TABLE HEADERS
    # ========================================================

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

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self, parent=None, repository=None):
        super().__init__(parent)

        self.repository = repository or ProjectRepository()

        self.setup_ui()
        self.refresh_projects()

    # ========================================================
    # USER INTERFACE
    # ========================================================

    def setup_ui(self):
        """Create the Projects page interface."""

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        # ----------------------------------------------------
        # PAGE HEADER
        # ----------------------------------------------------

        title = QLabel("Projects")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Organize electronics projects and their components."
        )
        subtitle.setObjectName("pageSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # ----------------------------------------------------
        # PROJECT TOOLBAR
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # PROJECTS TABLE
        # ----------------------------------------------------

        self.projects_table = QTableWidget()

        self.projects_table.setColumnCount(
            len(self.PROJECT_HEADERS)
        )

        self.projects_table.setHorizontalHeaderLabels(
            self.PROJECT_HEADERS
        )

        self.configure_table(self.projects_table)

        main_layout.addWidget(self.projects_table, 3)

        # ----------------------------------------------------
        # PROJECT CONTROLS
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # ASSIGNED COMPONENTS SECTION
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # COMPONENT ASSIGNMENT CONTROLS
        # ----------------------------------------------------

        component_controls = QHBoxLayout()

        self.assign_button = QPushButton("+ Assign Component")
        self.assign_button.setObjectName("primaryButton")

        self.remove_button = QPushButton("Remove Assignment")
        self.remove_button.setObjectName("dangerButton")

        component_controls.addWidget(self.assign_button)
        component_controls.addWidget(self.remove_button)
        component_controls.addStretch()

        main_layout.addLayout(component_controls)

        # ----------------------------------------------------
        # INITIAL BUTTON STATES
        # ----------------------------------------------------

        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.assign_button.setEnabled(False)
        self.remove_button.setEnabled(False)

        # ----------------------------------------------------
        # SIGNAL CONNECTIONS
        # ----------------------------------------------------

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

    # ========================================================
    # TABLE CONFIGURATION
    # ========================================================

    @staticmethod
    def configure_table(table):
        """Configure table selection and display behavior."""

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

    # ========================================================
    # TABLE POPULATION
    # ========================================================

    @staticmethod
    def populate_row(table, row, values):
        """Insert a row into a table."""

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

    # ========================================================
    # PROJECT REFRESH
    # ========================================================

    def refresh_projects(self):
        """Reload project records from the database."""

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

    # ========================================================
    # SELECTION MANAGEMENT
    # ========================================================

    def get_selected_project_id(self):
        """
        Return the selected project ID.

        Uses selectedRows() instead of currentRow() to prevent
        stale selections after clearSelection().
        """

        selection_model = self.projects_table.selectionModel()

        if selection_model is None:
            return None

        selected_rows = selection_model.selectedRows()

        if not selected_rows:
            return None

        row = selected_rows[0].row()

        item = self.projects_table.item(row, 0)

        return int(item.text()) if item else None

    def get_selected_component_id(self):
        """
        Return the selected component ID.

        Returns None when no component is selected.
        """

        selection_model = self.components_table.selectionModel()

        if selection_model is None:
            return None

        selected_rows = selection_model.selectedRows()

        if not selected_rows:
            return None

        row = selected_rows[0].row()

        item = self.components_table.item(row, 0)

        return int(item.text()) if item else None

    def update_button_states(self):
        """Enable or disable actions based on selections."""

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
        """Refresh assignments when project selection changes."""

        self.refresh_project_components()
        self.update_button_states()

    # ========================================================
    # COMPONENT REFRESH
    # ========================================================

    def refresh_project_components(self):
        """Load components assigned to the selected project."""

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

    # ========================================================
    # ADD PROJECT
    # ========================================================

    def add_project(self):
        """Open the Add Project dialog."""

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

    # ========================================================
    # EDIT PROJECT
    # ========================================================

    def edit_project(self, *_args):
        """Edit the selected project."""

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

    # ========================================================
    # DELETE PROJECT
    # ========================================================

    def delete_project(self):
        """Delete the selected project after confirmation."""

        project_id = self.get_selected_project_id()

        if project_id is None:
            return

        response = QMessageBox.question(
            self,
            "Delete Project",
            (
                "Delete this project and its component assignments?\n\n"
                "Inventory components will not be deleted."
            ),
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

    # ========================================================
    # ASSIGN COMPONENT
    # ========================================================

    def assign_component(self):
        """Assign an inventory component to a project."""

        project_id = self.get_selected_project_id()

        if project_id is None:
            return

        try:
            available_components = (
                self.repository.get_available_components()
            )

            if not available_components:

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

    # ========================================================
    # REMOVE COMPONENT
    # ========================================================

    def remove_component(self):
        """Remove a component assignment from a project."""

        project_id = self.get_selected_project_id()
        component_id = self.get_selected_component_id()

        if project_id is None or component_id is None:
            return

        response = QMessageBox.question(
            self,
            "Remove Component Assignment",
            (
                "Remove this component from the project?\n\n"
                "The inventory record will remain unchanged."
            ),
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

    # ========================================================
    # RESTORE PROJECT SELECTION
    # ========================================================

    def select_project(self, project_id):
        """Select a project by its database ID."""

        for row in range(self.projects_table.rowCount()):

            item = self.projects_table.item(row, 0)

            if item is None:
                continue

            if int(item.text()) == project_id:

                self.projects_table.selectRow(row)

                return