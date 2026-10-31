"""
CircuitVault - Component Dialog
Version: 0.1.0

Provides:
    - Add component form
    - Edit component form
    - Component input validation
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QTextEdit,
    QPushButton,
    QDialogButtonBox,
    QMessageBox,
)


COMPONENT_CATEGORIES = [
    "Microcontroller",
    "Single Board Computer",
    "Sensor",
    "Motor",
    "Motor Driver",
    "Integrated Circuit",
    "Resistor",
    "Capacitor",
    "Transistor",
    "Diode",
    "Display",
    "Communication Module",
    "Power Supply",
    "Connector",
    "Other",
]


class ComponentDialog(QDialog):
    """Dialog for creating and editing components."""

    def __init__(self, component=None, parent=None):
        super().__init__(parent)

        self.component = component

        self.setWindowTitle(
            "Edit Component" if component else "Add Component"
        )

        self.setMinimumWidth(450)

        self.setup_ui()

        if component:
            self.load_component(component)

    def setup_ui(self):
        """Create component form."""

        main_layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. MPU6050")

        self.category_input = QComboBox()
        self.category_input.addItems(COMPONENT_CATEGORIES)

        self.manufacturer_input = QLineEdit()
        self.manufacturer_input.setPlaceholderText(
            "e.g. Espressif"
        )

        self.part_number_input = QLineEdit()
        self.part_number_input.setPlaceholderText(
            "e.g. ESP32-S3-WROOM-1"
        )

        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 1_000_000)

        self.storage_input = QLineEdit()
        self.storage_input.setPlaceholderText(
            "e.g. Drawer A1"
        )

        self.datasheet_input = QLineEdit()
        self.datasheet_input.setPlaceholderText(
            "https://..."
        )

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText(
            "Additional component information..."
        )
        self.notes_input.setFixedHeight(100)

        form_layout.addRow("Name *", self.name_input)
        form_layout.addRow("Category *", self.category_input)
        form_layout.addRow(
            "Manufacturer", self.manufacturer_input
        )
        form_layout.addRow(
            "Part Number", self.part_number_input
        )
        form_layout.addRow("Quantity", self.quantity_input)
        form_layout.addRow("Storage", self.storage_input)
        form_layout.addRow("Datasheet", self.datasheet_input)
        form_layout.addRow("Notes", self.notes_input)

        main_layout.addLayout(form_layout)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(self.validate_and_accept)
        self.buttons.rejected.connect(self.reject)

        main_layout.addWidget(self.buttons)

    def load_component(self, component):
        """Populate the form with existing data."""

        self.name_input.setText(component["name"])

        category = component["category"]

        if self.category_input.findText(category) == -1:
            self.category_input.addItem(category)

        self.category_input.setCurrentText(category)

        self.manufacturer_input.setText(
            component.get("manufacturer") or ""
        )

        self.part_number_input.setText(
            component.get("part_number") or ""
        )

        self.quantity_input.setValue(
            component.get("quantity", 0)
        )

        self.storage_input.setText(
            component.get("storage_location") or ""
        )

        self.datasheet_input.setText(
            component.get("datasheet") or ""
        )

        self.notes_input.setPlainText(
            component.get("notes") or ""
        )

    def validate_and_accept(self):
        """Validate required fields before saving."""

        if not self.name_input.text().strip():
            QMessageBox.warning(
                self,
                "Validation Error",
                "Component name is required.",
            )
            return

        self.accept()

    def get_component_data(self):
        """Return form values as a dictionary."""

        return {
            "name": self.name_input.text().strip(),
            "category": self.category_input.currentText(),
            "manufacturer": self.manufacturer_input.text().strip(),
            "part_number": self.part_number_input.text().strip(),
            "quantity": self.quantity_input.value(),
            "storage_location": self.storage_input.text().strip(),
            "datasheet": self.datasheet_input.text().strip(),
            "notes": self.notes_input.toPlainText().strip(),
        }