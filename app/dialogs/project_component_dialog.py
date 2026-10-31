"""
CircuitVault - Project Component Dialog
Version: 0.1.0
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QSpinBox,
    QDialogButtonBox,
    QLabel,
    QMessageBox,
)


class ProjectComponentDialog(QDialog):
    """Assign an inventory component to a project."""

    def __init__(self, repository, parent=None):
        super().__init__(parent)

        self.repository = repository

        self.setWindowTitle("Assign Component")
        self.setMinimumWidth(450)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.component_input = QComboBox()

        for component in self.repository.get_available_components():
            label = (
                f"{component['name']} "
                f"({component['category']}, "
                f"Stock: {component['quantity']}, "
                f"ID: {component['id']})"
            )

            self.component_input.addItem(
                label,
                userData=component["id"],
            )

        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 1_000_000)
        self.quantity_input.setValue(1)

        form.addRow("Component *", self.component_input)
        form.addRow("Quantity Used *", self.quantity_input)

        layout.addLayout(form)

        note = QLabel(
            "Assigning components does not reduce inventory stock."
        )
        note.setWordWrap(True)
        layout.addWidget(note)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(
            self.validate_and_accept
        )
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)

    def get_assignment_data(self):
        return {
            "component_id": self.component_input.currentData(),
            "quantity_used": self.quantity_input.value(),
        }

    def validate_and_accept(self):
        if self.component_input.currentData() is None:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Select an inventory component.",
            )
            return

        self.accept()