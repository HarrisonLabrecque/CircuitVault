"""
CircuitVault - Project Dialog
Version: 0.1.0
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QDialogButtonBox,
    QMessageBox,
)

from database.project_repository import ProjectRepository


class ProjectDialog(QDialog):
    """Form for adding or editing a project."""

    def __init__(self, project=None, parent=None):
        super().__init__(parent)

        self.project = project

        self.setWindowTitle(
            "Edit Project" if project else "Add Project"
        )
        self.setMinimumWidth(480)

        self.setup_ui()

        if project:
            self.load_project(project)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "e.g. ESP32-S3 Flight Controller"
        )

        self.status_input = QComboBox()
        self.status_input.addItems(
            ProjectRepository.STATUSES
        )

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Describe the project's purpose..."
        )
        self.description_input.setMaximumHeight(130)

        form.addRow("Project Name *", self.name_input)
        form.addRow("Status", self.status_input)
        form.addRow("Description", self.description_input)

        layout.addLayout(form)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(
            self.validate_and_accept
        )
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)

    def load_project(self, project):
        self.name_input.setText(project["name"])
        self.status_input.setCurrentText(
            project.get("status") or "Planning"
        )
        self.description_input.setPlainText(
            project.get("description") or ""
        )

    def get_project_data(self):
        return {
            "name": self.name_input.text().strip(),
            "status": self.status_input.currentText(),
            "description": (
                self.description_input.toPlainText().strip()
            ),
        }

    def validate_and_accept(self):
        try:
            ProjectRepository.validate_project(
                self.get_project_data()
            )
        except ValueError as error:
            QMessageBox.warning(
                self,
                "Validation Error",
                str(error),
            )
            return

        self.accept()