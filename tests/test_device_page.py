"""
CircuitVault - Devices Page GUI Tests
Version: 0.1.0

Tests:
    - Page initialization
    - Device table
    - Device searching
    - Selection controls
    - Device dialog
    - Add device
    - Edit device
    - Delete device
    - Refresh
    - Device counts
"""

from PySide6.QtWidgets import (
    QDialog,
    QMessageBox,
)

from app.dialogs.device_dialog import DeviceDialog


# ============================================================
# PAGE INITIALIZATION
# ============================================================

def test_devices_page_created(devices_page):
    """Verify that the Devices page initializes."""

    assert devices_page is not None
    assert devices_page.devices_table is not None


def test_devices_table_columns(devices_page):
    """Verify the number of device table columns."""

    assert devices_page.devices_table.columnCount() == 8


def test_empty_devices_table(devices_page):
    """Verify that an empty database displays no devices."""

    assert devices_page.devices_table.rowCount() == 0


def test_action_buttons_disabled_initially(devices_page):
    """Verify that actions require a selected device."""

    assert not devices_page.edit_button.isEnabled()
    assert not devices_page.delete_button.isEnabled()


# ============================================================
# DEVICE TABLE
# ============================================================

def test_device_appears_in_table(
    devices_page,
    device_repository,
    sample_device,
):
    """Verify that registered devices appear in the table."""

    device_repository.add_device(sample_device)

    devices_page.refresh_devices()

    assert devices_page.devices_table.rowCount() == 1

    assert (
        devices_page.devices_table.item(0, 1).text()
        == "Robot Pi"
    )


def test_multiple_devices_displayed(
    devices_page,
    device_repository,
    sample_device,
):
    """Verify that multiple devices are displayed."""

    device_repository.add_device(sample_device)

    second = sample_device.copy()
    second["name"] = "ESP32 Node"

    device_repository.add_device(second)

    devices_page.refresh_devices()

    assert devices_page.devices_table.rowCount() == 2


def test_device_status_displayed(
    devices_page,
    device_repository,
    sample_device,
):
    """Verify that device status appears in the table."""

    device = sample_device.copy()
    device["status"] = "Online"

    device_repository.add_device(device)

    devices_page.refresh_devices()

    assert (
        devices_page.devices_table.item(0, 6).text()
        == "Online"
    )


def test_device_ip_displayed(
    devices_page,
    device_repository,
    sample_device,
):
    """Verify that device IP addresses are displayed."""

    device_repository.add_device(sample_device)

    devices_page.refresh_devices()

    assert (
        devices_page.devices_table.item(0, 4).text()
        == "192.168.1.20"
    )


# ============================================================
# SEARCH FUNCTIONALITY
# ============================================================

def test_search_devices(
    devices_page,
    device_repository,
    sample_device,
):
    """Verify that searching filters device records."""

    device_repository.add_device(sample_device)

    second = sample_device.copy()
    second["name"] = "ESP32 Node"
    second["device_type"] = "ESP32"
    second["hostname"] = "esp32.local"
    second["ip_address"] = "192.168.1.21"
    second["mac_address"] = ""
    second["status"] = "Online"

    device_repository.add_device(second)

    devices_page.refresh_devices()

    devices_page.search_input.setText("Robot Pi")

    assert devices_page.devices_table.rowCount() == 1

    assert (
        devices_page.devices_table.item(0, 1).text()
        == "Robot Pi"
    )


def test_clear_search(
    devices_page,
    device_repository,
    sample_device,
):
    """Verify that clearing search restores device records."""

    device_repository.add_device(sample_device)

    devices_page.search_input.setText("Nonexistent")

    assert devices_page.devices_table.rowCount() == 0

    devices_page.search_input.clear()

    assert devices_page.devices_table.rowCount() == 1


def test_search_by_ip(
    devices_page,
    device_repository,
    sample_device,
):
    """Verify searching by IP address."""

    device_repository.add_device(sample_device)

    devices_page.search_input.setText("192.168.1.20")

    assert devices_page.devices_table.rowCount() == 1


# ============================================================
# SELECTION CONTROLS
# ============================================================

def test_selection_enables_buttons(
    devices_page,
    device_repository,
    sample_device,
):
    """Verify selecting a device enables editing and deletion."""

    device_repository.add_device(sample_device)

    devices_page.refresh_devices()
    devices_page.devices_table.selectRow(0)

    assert devices_page.edit_button.isEnabled()
    assert devices_page.delete_button.isEnabled()


def test_selected_device_id(
    devices_page,
    device_repository,
    sample_device,
):
    """Verify the selected device ID is correct."""

    device_id = device_repository.add_device(sample_device)

    devices_page.refresh_devices()
    devices_page.devices_table.selectRow(0)

    assert devices_page.get_selected_device_id() == device_id


# ============================================================
# DEVICE DIALOG
# ============================================================

def test_device_dialog_created(qtbot):
    """Verify that the Add Device dialog initializes."""

    dialog = DeviceDialog()

    qtbot.addWidget(dialog)

    assert dialog.windowTitle() == "Add Device"


def test_device_dialog_defaults(qtbot):
    """Verify default dialog values."""

    dialog = DeviceDialog()

    qtbot.addWidget(dialog)

    assert dialog.name_input.text() == ""
    assert dialog.status_input.currentText() == "Offline"


def test_device_dialog_data(qtbot):
    """Verify form values are returned correctly."""

    dialog = DeviceDialog()

    qtbot.addWidget(dialog)

    dialog.name_input.setText("Robot Pi")
    dialog.type_input.setCurrentText("Raspberry Pi")
    dialog.hostname_input.setText("robotpi.local")
    dialog.ip_input.setText("192.168.1.20")
    dialog.status_input.setCurrentText("Online")

    data = dialog.get_device_data()

    assert data["name"] == "Robot Pi"
    assert data["device_type"] == "Raspberry Pi"
    assert data["hostname"] == "robotpi.local"
    assert data["ip_address"] == "192.168.1.20"
    assert data["status"] == "Online"


def test_edit_device_dialog(qtbot, sample_device):
    """Verify that existing device information loads."""

    dialog = DeviceDialog(device=sample_device)

    qtbot.addWidget(dialog)

    assert dialog.windowTitle() == "Edit Device"
    assert dialog.name_input.text() == "Robot Pi"
    assert dialog.ip_input.text() == "192.168.1.20"


def test_valid_device_dialog_accepts(qtbot):
    """Verify that a valid device form is accepted."""

    dialog = DeviceDialog()

    qtbot.addWidget(dialog)

    dialog.name_input.setText("ESP32 Node")

    dialog.validate_and_accept()

    assert dialog.result() == QDialog.DialogCode.Accepted


def test_invalid_ip_dialog_rejected(qtbot, monkeypatch):
    """Verify that an invalid IP prevents dialog acceptance."""

    dialog = DeviceDialog()

    qtbot.addWidget(dialog)

    dialog.name_input.setText("Test Device")
    dialog.ip_input.setText("999.999.999.999")

    warnings = []

    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args, **kwargs: warnings.append(args),
    )

    dialog.validate_and_accept()

    assert dialog.result() != QDialog.DialogCode.Accepted
    assert len(warnings) == 1


# ============================================================
# ADD DEVICE
# ============================================================

def test_add_device_from_page(
    devices_page,
    device_repository,
    sample_device,
    monkeypatch,
):
    """Verify that the page can add a device."""

    monkeypatch.setattr(
        DeviceDialog,
        "exec",
        lambda self: QDialog.DialogCode.Accepted,
    )

    monkeypatch.setattr(
        DeviceDialog,
        "get_device_data",
        lambda self: sample_device.copy(),
    )

    devices_page.add_device()

    assert device_repository.get_device_count() == 1
    assert devices_page.devices_table.rowCount() == 1


def test_cancel_add_device(
    devices_page,
    device_repository,
    monkeypatch,
):
    """Verify that cancelling does not create a device."""

    monkeypatch.setattr(
        DeviceDialog,
        "exec",
        lambda self: QDialog.DialogCode.Rejected,
    )

    devices_page.add_device()

    assert device_repository.get_device_count() == 0


# ============================================================
# EDIT DEVICE
# ============================================================

def test_edit_device_from_page(
    devices_page,
    device_repository,
    sample_device,
    monkeypatch,
):
    """Verify that the page can edit an existing device."""

    device_id = device_repository.add_device(sample_device)

    devices_page.refresh_devices()
    devices_page.devices_table.selectRow(0)

    updated_device = sample_device.copy()
    updated_device["name"] = "Robot Pi Updated"
    updated_device["status"] = "Online"

    monkeypatch.setattr(
        DeviceDialog,
        "exec",
        lambda self: QDialog.DialogCode.Accepted,
    )

    monkeypatch.setattr(
        DeviceDialog,
        "get_device_data",
        lambda self: updated_device.copy(),
    )

    devices_page.edit_device()

    device = device_repository.get_device(device_id)

    assert device["name"] == "Robot Pi Updated"
    assert device["status"] == "Online"


def test_cancel_edit_device(
    devices_page,
    device_repository,
    sample_device,
    monkeypatch,
):
    """Verify that cancelling an edit leaves data unchanged."""

    device_id = device_repository.add_device(sample_device)

    devices_page.refresh_devices()
    devices_page.devices_table.selectRow(0)

    monkeypatch.setattr(
        DeviceDialog,
        "exec",
        lambda self: QDialog.DialogCode.Rejected,
    )

    devices_page.edit_device()

    device = device_repository.get_device(device_id)

    assert device["name"] == "Robot Pi"
    assert device["status"] == "Offline"


# ============================================================
# DELETE DEVICE
# ============================================================

def test_delete_device_from_page(
    devices_page,
    device_repository,
    sample_device,
    monkeypatch,
):
    """Verify that confirmed deletion removes a device."""

    device_repository.add_device(sample_device)

    devices_page.refresh_devices()
    devices_page.devices_table.selectRow(0)

    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
    )

    devices_page.delete_device()

    assert device_repository.get_device_count() == 0
    assert devices_page.devices_table.rowCount() == 0


def test_cancel_delete_device(
    devices_page,
    device_repository,
    sample_device,
    monkeypatch,
):
    """Verify that cancelling deletion preserves the device."""

    device_repository.add_device(sample_device)

    devices_page.refresh_devices()
    devices_page.devices_table.selectRow(0)

    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.No,
    )

    devices_page.delete_device()

    assert device_repository.get_device_count() == 1


# ============================================================
# REFRESH AND COUNTS
# ============================================================

def test_refresh_devices(
    devices_page,
    device_repository,
    sample_device,
):
    """Verify that refreshing reloads registered devices."""

    assert devices_page.devices_table.rowCount() == 0

    device_repository.add_device(sample_device)

    devices_page.refresh_devices()

    assert devices_page.devices_table.rowCount() == 1


def test_device_count_label(
    devices_page,
    device_repository,
    sample_device,
):
    """Verify that the device count label updates."""

    device_repository.add_device(sample_device)

    devices_page.refresh_devices()

    assert "1" in devices_page.count_label.text()


def test_refresh_after_deletion(
    devices_page,
    device_repository,
    sample_device,
):
    """Verify that deleted devices disappear after refreshing."""

    device_id = device_repository.add_device(sample_device)

    devices_page.refresh_devices()

    assert devices_page.devices_table.rowCount() == 1

    device_repository.delete_device(device_id)

    devices_page.refresh_devices()

    assert devices_page.devices_table.rowCount() == 0