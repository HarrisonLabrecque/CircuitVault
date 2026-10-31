"""
CircuitVault - Components Page GUI Tests
Version: 0.1.0

Tests:
    - Components page initialization
    - Inventory table
    - Search functionality
    - Selection controls
    - Component dialog
    - Table refreshing
"""

from PySide6.QtCore import Qt

from PySide6.QtWidgets import QDialog

from app.dialogs.component_dialog import ComponentDialog


# ============================================================
# PAGE INITIALIZATION
# ============================================================

def test_components_page_created(components_page):
    """Verify that the Components page initializes."""

    assert components_page is not None

    assert components_page.components_table is not None


def test_components_table_columns(components_page):
    """Verify the number of inventory columns."""

    assert components_page.components_table.columnCount() == 8


def test_empty_components_table(components_page):
    """Verify that an empty database produces an empty table."""

    assert components_page.components_table.rowCount() == 0


# ============================================================
# TABLE DISPLAY
# ============================================================

def test_component_appears_in_table(
    components_page,
    component_repository,
    sample_component,
):
    """Verify that stored components appear in the table."""

    component_repository.add_component(sample_component)

    components_page.refresh_components()

    assert components_page.components_table.rowCount() == 1

    item = components_page.components_table.item(0, 1)

    assert item.text() == "MPU6050"


def test_multiple_components_displayed(
    components_page,
    component_repository,
    sample_component,
):
    """Verify that multiple components appear."""

    component_repository.add_component(sample_component)

    second = sample_component.copy()
    second["name"] = "ESP32-S3"

    component_repository.add_component(second)

    components_page.refresh_components()

    assert components_page.components_table.rowCount() == 2


# ============================================================
# SEARCH FUNCTIONALITY
# ============================================================

def test_search_components(
    components_page,
    component_repository,
    sample_component,
    qtbot,
):
    """Verify that the search field filters inventory records."""

    component_repository.add_component(sample_component)

    second = sample_component.copy()
    second["name"] = "ESP32-S3"
    second["category"] = "Microcontroller"

    component_repository.add_component(second)

    components_page.refresh_components()

    components_page.search_input.setText("MPU6050")

    assert components_page.components_table.rowCount() == 1

    assert (
        components_page.components_table.item(0, 1).text()
        == "MPU6050"
    )


def test_clear_search(
    components_page,
    component_repository,
    sample_component,
):
    """Verify that clearing search restores all components."""

    component_repository.add_component(sample_component)

    components_page.search_input.setText("Nonexistent")

    assert components_page.components_table.rowCount() == 0

    components_page.search_input.clear()

    assert components_page.components_table.rowCount() == 1


# ============================================================
# SELECTION CONTROLS
# ============================================================

def test_edit_delete_disabled_without_selection(components_page):
    """Verify that editing and deletion require a selection."""

    assert not components_page.edit_button.isEnabled()
    assert not components_page.delete_button.isEnabled()


def test_selection_enables_buttons(
    components_page,
    component_repository,
    sample_component,
):
    """Verify that selecting a component enables actions."""

    component_repository.add_component(sample_component)

    components_page.refresh_components()

    components_page.components_table.selectRow(0)

    assert components_page.edit_button.isEnabled()
    assert components_page.delete_button.isEnabled()


def test_selected_component_id(
    components_page,
    component_repository,
    sample_component,
):
    """Verify that the selected component ID is returned."""

    component_id = component_repository.add_component(
        sample_component
    )

    components_page.refresh_components()

    components_page.components_table.selectRow(0)

    assert (
        components_page.get_selected_component_id()
        == component_id
    )


# ============================================================
# COMPONENT DIALOG
# ============================================================

def test_component_dialog_created(qtbot):
    """Verify that the Add Component dialog initializes."""

    dialog = ComponentDialog()

    qtbot.addWidget(dialog)

    assert dialog.windowTitle() == "Add Component"


def test_component_dialog_default_values(qtbot):
    """Verify default form values."""

    dialog = ComponentDialog()

    qtbot.addWidget(dialog)

    assert dialog.name_input.text() == ""
    assert dialog.quantity_input.value() == 0


def test_component_dialog_data(qtbot):
    """Verify that form values are returned correctly."""

    dialog = ComponentDialog()

    qtbot.addWidget(dialog)

    dialog.name_input.setText("MPU6050")
    dialog.category_input.setCurrentText("Sensor")
    dialog.quantity_input.setValue(3)
    dialog.storage_input.setText("Drawer A1")

    data = dialog.get_component_data()

    assert data["name"] == "MPU6050"
    assert data["category"] == "Sensor"
    assert data["quantity"] == 3
    assert data["storage_location"] == "Drawer A1"


def test_edit_component_dialog(qtbot, sample_component):
    """Verify that editing loads existing component values."""

    dialog = ComponentDialog(component=sample_component)

    qtbot.addWidget(dialog)

    assert dialog.windowTitle() == "Edit Component"
    assert dialog.name_input.text() == "MPU6050"
    assert dialog.quantity_input.value() == 3


def test_valid_component_dialog_accepts(qtbot):
    """Verify that a valid form can be accepted."""

    dialog = ComponentDialog()

    qtbot.addWidget(dialog)

    dialog.name_input.setText("ESP32-S3")

    dialog.validate_and_accept()

    assert dialog.result() == QDialog.DialogCode.Accepted


# ============================================================
# TABLE REFRESH
# ============================================================

def test_refresh_updates_table(
    components_page,
    component_repository,
    sample_component,
):
    """Verify that refreshing reloads the inventory."""

    assert components_page.components_table.rowCount() == 0

    component_repository.add_component(sample_component)

    components_page.refresh_components()

    assert components_page.components_table.rowCount() == 1


def test_component_count_label(
    components_page,
    component_repository,
    sample_component,
):
    """Verify that the component count label updates."""

    component_repository.add_component(sample_component)

    components_page.refresh_components()

    assert "1" in components_page.count_label.text()