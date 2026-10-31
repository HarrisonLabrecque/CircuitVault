"""
CircuitVault - Sensor Repository Tests
Version: 0.1.0

Tests:
    - Register sensor readings
    - Retrieve readings
    - Update readings
    - Delete readings
    - Search readings
    - Validate measurements
    - Device relationships
    - Database persistence
"""

import sqlite3

import pytest

from database.sensor_repository import SensorRepository


# ============================================================
# CREATE OPERATIONS
# ============================================================

def test_add_reading(sensor_repository, sample_reading):
    """Verify that a sensor measurement can be stored."""

    reading_id = sensor_repository.add_reading(sample_reading)

    assert reading_id > 0

    reading = sensor_repository.get_reading(reading_id)

    assert reading is not None
    assert reading["sensor_name"] == "MPU6050"
    assert reading["metric"] == "Acceleration X"
    assert reading["value"] == pytest.approx(0.12)


def test_add_multiple_readings(sensor_repository, sample_reading):
    """Verify that multiple measurements can be stored."""

    sensor_repository.add_reading(sample_reading)

    second = sample_reading.copy()
    second["metric"] = "Gyroscope X"
    second["value"] = 1.5
    second["unit"] = "°/s"

    sensor_repository.add_reading(second)

    assert len(sensor_repository.get_all_readings()) == 2


def test_add_reading_without_unit(sensor_repository, sample_reading):
    """Verify that units are optional."""

    reading = sample_reading.copy()
    reading.pop("unit")

    reading_id = sensor_repository.add_reading(reading)

    stored = sensor_repository.get_reading(reading_id)

    assert stored["unit"] == ""


# ============================================================
# READ OPERATIONS
# ============================================================

def test_get_all_readings(sensor_repository, sample_reading):
    """Verify that all measurements can be retrieved."""

    sensor_repository.add_reading(sample_reading)

    readings = sensor_repository.get_all_readings()

    assert len(readings) == 1
    assert readings[0]["sensor_name"] == "MPU6050"


def test_get_nonexistent_reading(sensor_repository):
    """Verify that missing measurements return None."""

    assert sensor_repository.get_reading(9999) is None


def test_reading_has_device_name(sensor_repository, sample_reading):
    """Verify that readings include their associated device name."""

    sensor_repository.add_reading(sample_reading)

    readings = sensor_repository.get_all_readings()

    assert readings[0]["device_name"] == "Robot Pi"


def test_reading_has_timestamp(sensor_repository, sample_reading):
    """Verify that SQLite assigns a timestamp."""

    reading_id = sensor_repository.add_reading(sample_reading)

    reading = sensor_repository.get_reading(reading_id)

    assert reading["timestamp"] is not None
    assert reading["timestamp"] != ""


def test_get_registered_devices(
    sensor_repository,
    registered_device,
):
    """Verify that registered devices can be retrieved."""

    devices = sensor_repository.get_registered_devices()

    assert len(devices) == 1
    assert devices[0]["id"] == registered_device
    assert devices[0]["name"] == "Robot Pi"


# ============================================================
# UPDATE OPERATIONS
# ============================================================

def test_update_reading(sensor_repository, sample_reading):
    """Verify that an existing measurement can be updated."""

    reading_id = sensor_repository.add_reading(sample_reading)

    updated = sample_reading.copy()
    updated["metric"] = "Acceleration Y"
    updated["value"] = 0.25

    result = sensor_repository.update_reading(
        reading_id,
        updated,
    )

    assert result is True

    reading = sensor_repository.get_reading(reading_id)

    assert reading["metric"] == "Acceleration Y"
    assert reading["value"] == pytest.approx(0.25)


def test_update_nonexistent_reading(
    sensor_repository,
    sample_reading,
):
    """Verify that updating a missing measurement returns False."""

    result = sensor_repository.update_reading(
        9999,
        sample_reading,
    )

    assert result is False


def test_update_preserves_timestamp(
    sensor_repository,
    sample_reading,
):
    """Verify that editing preserves the original timestamp."""

    reading_id = sensor_repository.add_reading(sample_reading)

    original = sensor_repository.get_reading(reading_id)

    updated = sample_reading.copy()
    updated["value"] = 0.5

    sensor_repository.update_reading(reading_id, updated)

    modified = sensor_repository.get_reading(reading_id)

    assert modified["timestamp"] == original["timestamp"]


# ============================================================
# DELETE OPERATIONS
# ============================================================

def test_delete_reading(sensor_repository, sample_reading):
    """Verify that measurements can be deleted."""

    reading_id = sensor_repository.add_reading(sample_reading)

    result = sensor_repository.delete_reading(reading_id)

    assert result is True
    assert sensor_repository.get_reading(reading_id) is None


def test_delete_nonexistent_reading(sensor_repository):
    """Verify that deleting a missing reading returns False."""

    assert sensor_repository.delete_reading(9999) is False


# ============================================================
# SEARCH OPERATIONS
# ============================================================

@pytest.mark.parametrize(
    "search_text",
    [
        "Robot Pi",
        "MPU6050",
        "Acceleration",
        "g",
    ],
)
def test_search_reading_fields(
    sensor_repository,
    sample_reading,
    search_text,
):
    """Verify searching by device, sensor, metric, and unit."""

    sensor_repository.add_reading(sample_reading)

    results = sensor_repository.search_readings(search_text)

    assert len(results) == 1
    assert results[0]["sensor_name"] == "MPU6050"


def test_search_case_insensitive(
    sensor_repository,
    sample_reading,
):
    """Verify case-insensitive searching."""

    sensor_repository.add_reading(sample_reading)

    results = sensor_repository.search_readings("mpu6050")

    assert len(results) == 1


def test_search_no_matches(sensor_repository, sample_reading):
    """Verify that unmatched searches return an empty list."""

    sensor_repository.add_reading(sample_reading)

    results = sensor_repository.search_readings(
        "Nonexistent Sensor"
    )

    assert results == []


def test_empty_search_returns_all(
    sensor_repository,
    sample_reading,
):
    """Verify that an empty search returns all readings."""

    sensor_repository.add_reading(sample_reading)

    results = sensor_repository.search_readings("")

    assert len(results) == 1


def test_search_literal_wildcard(
    sensor_repository,
    sample_reading,
):
    """Verify that SQL wildcards are treated literally."""

    reading = sample_reading.copy()
    reading["sensor_name"] = "Sensor_1"

    sensor_repository.add_reading(reading)

    results = sensor_repository.search_readings("_")

    assert len(results) == 1
    assert results[0]["sensor_name"] == "Sensor_1"


# ============================================================
# COUNT OPERATIONS
# ============================================================

def test_reading_count(sensor_repository, sample_reading):
    """Verify sensor measurement counting."""

    assert sensor_repository.get_reading_count() == 0

    sensor_repository.add_reading(sample_reading)

    assert sensor_repository.get_reading_count() == 1


# ============================================================
# VALIDATION
# ============================================================

@pytest.mark.parametrize(
    "invalid_name",
    ["", "   ", None],
)
def test_invalid_sensor_name(
    sensor_repository,
    sample_reading,
    invalid_name,
):
    """Verify that sensor names are required."""

    reading = sample_reading.copy()
    reading["sensor_name"] = invalid_name

    with pytest.raises(ValueError):
        sensor_repository.add_reading(reading)


def test_missing_metric(sensor_repository, sample_reading):
    """Verify that measurement types are required."""

    reading = sample_reading.copy()
    reading["metric"] = ""

    with pytest.raises(ValueError):
        sensor_repository.add_reading(reading)


@pytest.mark.parametrize(
    "invalid_value",
    [
        "invalid",
        None,
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_invalid_measurement_value(
    sensor_repository,
    sample_reading,
    invalid_value,
):
    """Verify that measurements must be finite numbers."""

    reading = sample_reading.copy()
    reading["value"] = invalid_value

    with pytest.raises(ValueError):
        sensor_repository.add_reading(reading)


def test_invalid_device_id(sensor_repository, sample_reading):
    """Verify that invalid device identifiers are rejected."""

    reading = sample_reading.copy()
    reading["device_id"] = -1

    with pytest.raises(ValueError):
        sensor_repository.add_reading(reading)


# ============================================================
# DEVICE RELATIONSHIPS
# ============================================================

def test_nonexistent_device_rejected(
    sensor_repository,
    sample_reading,
):
    """Verify foreign-key enforcement."""

    reading = sample_reading.copy()
    reading["device_id"] = 9999

    with pytest.raises(sqlite3.IntegrityError):
        sensor_repository.add_reading(reading)


def test_device_deletion_cascades_to_readings(
    sensor_repository,
    device_repository,
    registered_device,
    sample_reading,
):
    """Verify that deleting a device removes its readings."""

    sensor_repository.add_reading(sample_reading)

    assert sensor_repository.get_reading_count() == 1

    device_repository.delete_device(registered_device)

    assert sensor_repository.get_reading_count() == 0


# ============================================================
# DATABASE PERSISTENCE
# ============================================================

def test_reading_persistence(
    sensor_repository,
    test_database,
    sample_reading,
):
    """Verify that readings persist across repository instances."""

    reading_id = sensor_repository.add_reading(sample_reading)

    new_repository = SensorRepository(
        database=test_database
    )

    reading = new_repository.get_reading(reading_id)

    assert reading is not None
    assert reading["sensor_name"] == "MPU6050"