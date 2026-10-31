"""
CircuitVault - Sensors Page GUI Tests
Version: 0.1.0

Tests:
    - Page initialization
    - Sensor readings table
    - Search functionality
    - Selection controls
    - Sensor reading dialog
    - Add, edit, and delete operations
    - Refresh and count display
"""

from PySide6.QtWidgets import QDialog, QMessageBox

from app.dialogs.sensor_reading_dialog import SensorReadingDialog


# ============================================================
# PAGE INITIALIZATION
# ============================================================

def test_sensors_page_created(sensors_page):
    """Verify that the Sensors page initializes."""

    assert sensors_page is not None
    assert sensors_page.readings_table is not None


def test_readings_table_columns(sensors_page):
    """Verify the number of sensor table columns."""

    assert sensors_page.readings_table.columnCount() == 7


def test_empty_readings_table(sensors_page):
    """Verify that an empty database displays no readings."""

    assert sensors_page.readings_table.rowCount() == 0


def test_action_buttons_disabled_initially(sensors_page):
    """Verify that editing and deletion require a selection."""

    assert not sensors_page.edit_button.isEnabled()
    assert not sensors_page.delete_button.isEnabled()


# ============================================================
# TABLE DISPLAY
# ============================================================

def test_reading_appears_in_table(
    sensors_page,
    sensor_repository,
    sample_reading,
):
    """Verify that stored readings appear in the table."""

    sensor_repository.add_reading(sample_reading)

    sensors_page.refresh_readings()

    assert sensors_page.readings_table.rowCount() == 1

    assert (
        sensors_page.readings_table.item(0, 2).text()
        == "MPU6050"
    )


def test_multiple_readings_displayed(
    sensors_page,
    sensor_repository,
    sample_reading,
):
    """Verify that multiple readings appear in the table."""

    sensor_repository.add_reading(sample_reading)

    second = sample_reading.copy()
    second["metric"] = "Gyroscope X"
    second["value"] = 1.5

    sensor_repository.add_reading(second)

    sensors_page.refresh_readings()

    assert sensors_page.readings_table.rowCount() == 2


def test_device_name_displayed(
    sensors_page,
    sensor_repository,
    sample_reading,
):
    """Verify that the associated device name is displayed."""

    sensor_repository.add_reading(sample_reading)

    sensors_page.refresh_readings()

    assert (
        sensors_page.readings_table.item(0, 1).text()
        == "Robot Pi"
    )


def test_measurement_value_displayed(
    sensors_page,
    sensor_repository,
    sample_reading,
):
    """Verify that measurement values are displayed."""

    sensor_repository.add_reading(sample_reading)

    sensors_page.refresh_readings()

    value = float(
        sensors_page.readings_table.item(0, 4).text()
    )

    assert value == 0.12


# ============================================================
# SEARCH FUNCTIONALITY
# ============================================================

def test_search_sensor_name(
    sensors_page,
    sensor_repository,
    sample_reading,
):
    """Verify that searching filters sensor names."""

    sensor_repository.add_reading(sample_reading)

    second = sample_reading.copy()
    second["sensor_name"] = "BME280"
    second["metric"] = "Temperature"
    second["unit"] = "°C"

    sensor_repository.add_reading(second)

    sensors_page.refresh_readings()
    sensors_page.search_input.setText("MPU6050")

    assert sensors_page.readings_table.rowCount() == 1

    assert (
        sensors_page.readings_table.item(0, 2).text()
        == "MPU6050"
    )


def test_search_by_metric(
    sensors_page,
    sensor_repository,
    sample_reading,
):
    """Verify searching by measurement type."""

    sensor_repository.add_reading(sample_reading)

    sensors_page.search_input.setText("Acceleration")

    assert sensors_page.readings_table.rowCount() == 1


def test_clear_search(
    sensors_page,
    sensor_repository,
    sample_reading,
):
    """Verify that clearing search restores readings."""

    sensor_repository.add_reading(sample_reading)

    sensors_page.search_input.setText("Nonexistent")

    assert sensors_page.readings_table.rowCount() == 0

    sensors_page.search_input.clear()

    assert sensors_page.readings_table.rowCount() == 1


# ============================================================
# SELECTION CONTROLS
# ============================================================

def test_selection_enables_buttons(
    sensors_page,
    sensor_repository,
    sample_reading,
):
    """Verify that selecting a reading enables actions."""

    sensor_repository.add_reading(sample_reading)

    sensors_page.refresh_readings()
    sensors_page.readings_table.selectRow(0)

    assert sensors_page.edit_button.isEnabled()
    assert sensors_page.delete_button.isEnabled()


def test_selected_reading_id(
    sensors_page,
    sensor_repository,
    sample_reading,
):
    """Verify that the selected reading ID is correct."""

    reading_id = sensor_repository.add_reading(sample_reading)

    sensors_page.refresh_readings()
    sensors_page.readings_table.selectRow(0)

    assert sensors_page.get_selected_reading_id() == reading_id


# ============================================================
# SENSOR DIALOG
# ============================================================

def test_sensor_dialog_created(
    qtbot,
    sensor_repository,
    registered_device,
):
    """Verify that the Add Reading dialog initializes."""

    dialog = SensorReadingDialog(
        repository=sensor_repository
    )

    qtbot.addWidget(dialog)

    assert dialog.windowTitle() == "Add Sensor Reading"
    assert dialog.device_input.count() == 1


def test_sensor_dialog_defaults(
    qtbot,
    sensor_repository,
    registered_device,
):
    """Verify the default sensor form values."""

    dialog = SensorReadingDialog(
        repository=sensor_repository
    )

    qtbot.addWidget(dialog)

    assert dialog.sensor_input.text() == ""
    assert dialog.value_input.value() == 0.0


def test_sensor_dialog_data(
    qtbot,
    sensor_repository,
    registered_device,
):
    """Verify that form data is returned correctly."""

    dialog = SensorReadingDialog(
        repository=sensor_repository
    )

    qtbot.addWidget(dialog)

    dialog.sensor_input.setText("MPU6050")
    dialog.metric_input.setCurrentText("Acceleration X")
    dialog.value_input.setValue(0.12)
    dialog.unit_input.setText("g")

    data = dialog.get_reading_data()

    assert data["device_id"] == registered_device
    assert data["sensor_name"] == "MPU6050"
    assert data["metric"] == "Acceleration X"
    assert data["value"] == 0.12
    assert data["unit"] == "g"


def test_edit_sensor_dialog(
    qtbot,
    sensor_repository,
    sample_reading,
):
    """Verify that editing loads existing measurement data."""

    dialog = SensorReadingDialog(
        repository=sensor_repository,
        reading=sample_reading,
    )

    qtbot.addWidget(dialog)

    assert dialog.windowTitle() == "Edit Sensor Reading"
    assert dialog.sensor_input.text() == "MPU6050"
    assert dialog.value_input.value() == 0.12


def test_valid_sensor_dialog_accepts(
    qtbot,
    sensor_repository,
    registered_device,
):
    """Verify that valid sensor data can be accepted."""

    dialog = SensorReadingDialog(
        repository=sensor_repository
    )

    qtbot.addWidget(dialog)

    dialog.sensor_input.setText("MPU6050")
    dialog.metric_input.setCurrentText("Acceleration X")
    dialog.value_input.setValue(0.12)

    dialog.validate_and_accept()

    assert dialog.result() == QDialog.DialogCode.Accepted


def test_invalid_sensor_dialog_rejected(
    qtbot,
    sensor_repository,
    registered_device,
    monkeypatch,
):
    """Verify that an empty sensor name prevents acceptance."""

    dialog = SensorReadingDialog(
        repository=sensor_repository
    )

    qtbot.addWidget(dialog)

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
# ADD READING
# ============================================================

def test_add_reading_from_page(
    sensors_page,
    sensor_repository,
    sample_reading,
    monkeypatch,
):
    """Verify that the page can add a sensor reading."""

    monkeypatch.setattr(
        SensorReadingDialog,
        "exec",
        lambda self: QDialog.DialogCode.Accepted,
    )

    monkeypatch.setattr(
        SensorReadingDialog,
        "get_reading_data",
        lambda self: sample_reading.copy(),
    )

    sensors_page.add_reading()

    assert sensor_repository.get_reading_count() == 1
    assert sensors_page.readings_table.rowCount() == 1


def test_cancel_add_reading(
    sensors_page,
    sensor_repository,
    registered_device,
    monkeypatch,
):
    """Verify that cancelling does not create a reading."""

    monkeypatch.setattr(
        SensorReadingDialog,
        "exec",
        lambda self: QDialog.DialogCode.Rejected,
    )

    sensors_page.add_reading()

    assert sensor_repository.get_reading_count() == 0


def test_add_reading_without_devices(
    sensors_page,
    sensor_repository,
    monkeypatch,
):
    """Verify that adding requires a registered device."""

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "information",
        lambda *args, **kwargs: messages.append(args),
    )

    sensors_page.add_reading()

    assert sensor_repository.get_reading_count() == 0
    assert len(messages) == 1


# ============================================================
# EDIT READING
# ============================================================

def test_edit_reading_from_page(
    sensors_page,
    sensor_repository,
    sample_reading,
    monkeypatch,
):
    """Verify that the page can edit an existing reading."""

    reading_id = sensor_repository.add_reading(sample_reading)

    sensors_page.refresh_readings()
    sensors_page.readings_table.selectRow(0)

    updated = sample_reading.copy()
    updated["metric"] = "Acceleration Y"
    updated["value"] = 0.5

    monkeypatch.setattr(
        SensorReadingDialog,
        "exec",
        lambda self: QDialog.DialogCode.Accepted,
    )

    monkeypatch.setattr(
        SensorReadingDialog,
        "get_reading_data",
        lambda self: updated.copy(),
    )

    sensors_page.edit_reading()

    reading = sensor_repository.get_reading(reading_id)

    assert reading["metric"] == "Acceleration Y"
    assert reading["value"] == 0.5


def test_cancel_edit_reading(
    sensors_page,
    sensor_repository,
    sample_reading,
    monkeypatch,
):
    """Verify that cancelling an edit preserves the reading."""

    reading_id = sensor_repository.add_reading(sample_reading)

    sensors_page.refresh_readings()
    sensors_page.readings_table.selectRow(0)

    monkeypatch.setattr(
        SensorReadingDialog,
        "exec",
        lambda self: QDialog.DialogCode.Rejected,
    )

    sensors_page.edit_reading()

    reading = sensor_repository.get_reading(reading_id)

    assert reading["metric"] == "Acceleration X"
    assert reading["value"] == 0.12


# ============================================================
# DELETE READING
# ============================================================

def test_delete_reading_from_page(
    sensors_page,
    sensor_repository,
    sample_reading,
    monkeypatch,
):
    """Verify that confirmed deletion removes a reading."""

    sensor_repository.add_reading(sample_reading)

    sensors_page.refresh_readings()
    sensors_page.readings_table.selectRow(0)

    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
    )

    sensors_page.delete_reading()

    assert sensor_repository.get_reading_count() == 0
    assert sensors_page.readings_table.rowCount() == 0


def test_cancel_delete_reading(
    sensors_page,
    sensor_repository,
    sample_reading,
    monkeypatch,
):
    """Verify that cancelling deletion preserves the reading."""

    sensor_repository.add_reading(sample_reading)

    sensors_page.refresh_readings()
    sensors_page.readings_table.selectRow(0)

    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.No,
    )

    sensors_page.delete_reading()

    assert sensor_repository.get_reading_count() == 1


# ============================================================
# REFRESH AND COUNTS
# ============================================================

def test_refresh_readings(
    sensors_page,
    sensor_repository,
    sample_reading,
):
    """Verify that refreshing reloads measurements."""

    assert sensors_page.readings_table.rowCount() == 0

    sensor_repository.add_reading(sample_reading)

    sensors_page.refresh_readings()

    assert sensors_page.readings_table.rowCount() == 1


def test_reading_count_label(
    sensors_page,
    sensor_repository,
    sample_reading,
):
    """Verify that the displayed reading count updates."""

    sensor_repository.add_reading(sample_reading)

    sensors_page.refresh_readings()

    assert "1" in sensors_page.count_label.text()


def test_refresh_after_deletion(
    sensors_page,
    sensor_repository,
    sample_reading,
):
    """Verify deleted readings disappear after refresh."""

    reading_id = sensor_repository.add_reading(sample_reading)

    sensors_page.refresh_readings()

    assert sensors_page.readings_table.rowCount() == 1

    sensor_repository.delete_reading(reading_id)

    sensors_page.refresh_readings()

    assert sensors_page.readings_table.rowCount() == 0