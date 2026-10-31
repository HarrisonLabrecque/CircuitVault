"""
CircuitVault - Device Repository Tests
Version: 0.1.0

Tests:
    - Device registration
    - Device retrieval
    - Device updates
    - Device deletion
    - Device searching
    - Device counts
    - Device validation
    - Database persistence
"""

import pytest

from database.device_repository import (
    DeviceRepository,
)


# ============================================================
# CREATE OPERATIONS
# ============================================================

def test_add_device(device_repository, sample_device):
    """Verify that a device can be registered."""

    device_id = device_repository.add_device(sample_device)

    assert device_id > 0

    device = device_repository.get_device(device_id)

    assert device is not None
    assert device["name"] == "Robot Pi"
    assert device["device_type"] == "Raspberry Pi"
    assert device["status"] == "Offline"


def test_add_multiple_devices(device_repository, sample_device):
    """Verify that multiple devices can be registered."""

    device_repository.add_device(sample_device)

    second = sample_device.copy()
    second["name"] = "ESP32 Node"
    second["device_type"] = "ESP32"
    second["ip_address"] = "192.168.1.21"

    device_repository.add_device(second)

    devices = device_repository.get_all_devices()

    assert len(devices) == 2


def test_add_device_without_optional_fields(device_repository):
    """Verify that optional fields can be omitted."""

    device_id = device_repository.add_device({
        "name": "Arduino Uno",
        "device_type": "Arduino",
    })

    device = device_repository.get_device(device_id)

    assert device["name"] == "Arduino Uno"
    assert device["hostname"] == ""
    assert device["ip_address"] == ""
    assert device["status"] == "Offline"


# ============================================================
# READ OPERATIONS
# ============================================================

def test_get_all_devices(device_repository, sample_device):
    """Verify that all devices can be retrieved."""

    device_repository.add_device(sample_device)

    devices = device_repository.get_all_devices()

    assert len(devices) == 1
    assert devices[0]["name"] == "Robot Pi"


def test_get_nonexistent_device(device_repository):
    """Verify that missing devices return None."""

    assert device_repository.get_device(9999) is None


def test_devices_sorted_by_name(device_repository):
    """Verify alphabetical ordering."""

    device_repository.add_device({
        "name": "Zeta Controller",
        "device_type": "ESP32",
    })

    device_repository.add_device({
        "name": "Arduino Uno",
        "device_type": "Arduino",
    })

    devices = device_repository.get_all_devices()

    assert [device["name"] for device in devices] == [
        "Arduino Uno",
        "Zeta Controller",
    ]


# ============================================================
# UPDATE OPERATIONS
# ============================================================

def test_update_device(device_repository, sample_device):
    """Verify that device information can be updated."""

    device_id = device_repository.add_device(sample_device)

    updated = sample_device.copy()
    updated["name"] = "Robot Pi 4B"
    updated["status"] = "Online"

    result = device_repository.update_device(
        device_id,
        updated,
    )

    assert result is True

    device = device_repository.get_device(device_id)

    assert device["name"] == "Robot Pi 4B"
    assert device["status"] == "Online"


def test_update_nonexistent_device(
    device_repository,
    sample_device,
):
    """Verify that updating a missing device returns False."""

    result = device_repository.update_device(
        9999,
        sample_device,
    )

    assert result is False


# ============================================================
# DELETE OPERATIONS
# ============================================================

def test_delete_device(device_repository, sample_device):
    """Verify that a registered device can be deleted."""

    device_id = device_repository.add_device(sample_device)

    result = device_repository.delete_device(device_id)

    assert result is True
    assert device_repository.get_device(device_id) is None


def test_delete_nonexistent_device(device_repository):
    """Verify that deleting a missing device returns False."""

    assert device_repository.delete_device(9999) is False


# ============================================================
# SEARCH OPERATIONS
# ============================================================

@pytest.mark.parametrize(
    "search_text",
    [
        "Robot",
        "Raspberry Pi",
        "robotpi.local",
        "192.168.1.20",
        "AA:BB:CC",
        "Offline",
    ],
)
def test_search_device_fields(
    device_repository,
    sample_device,
    search_text,
):
    """Verify searching across device fields."""

    device_repository.add_device(sample_device)

    results = device_repository.search_devices(search_text)

    assert len(results) == 1
    assert results[0]["name"] == "Robot Pi"


def test_search_case_insensitive(
    device_repository,
    sample_device,
):
    """Verify case-insensitive searching."""

    device_repository.add_device(sample_device)

    results = device_repository.search_devices("robot pi")

    assert len(results) == 1


def test_search_no_matches(device_repository, sample_device):
    """Verify unmatched searches return an empty list."""

    device_repository.add_device(sample_device)

    results = device_repository.search_devices(
        "Nonexistent Device"
    )

    assert results == []


def test_empty_search_returns_all(
    device_repository,
    sample_device,
):
    """Verify that an empty search returns all devices."""

    device_repository.add_device(sample_device)

    results = device_repository.search_devices("")

    assert len(results) == 1


def test_search_literal_wildcards(device_repository):
    """Verify that SQL wildcard characters are treated literally."""

    device_repository.add_device({
        "name": "Sensor_1",
        "device_type": "ESP32",
    })

    device_repository.add_device({
        "name": "SensorX1",
        "device_type": "ESP32",
    })

    results = device_repository.search_devices("_")

    assert len(results) == 1
    assert results[0]["name"] == "Sensor_1"


# ============================================================
# DEVICE COUNTS
# ============================================================

def test_device_count(device_repository, sample_device):
    """Verify registered device counting."""

    assert device_repository.get_device_count() == 0

    device_repository.add_device(sample_device)

    assert device_repository.get_device_count() == 1


def test_online_device_count(device_repository, sample_device):
    """Verify that only Online devices are counted."""

    device_repository.add_device(sample_device)

    online = sample_device.copy()
    online["name"] = "ESP32 Online"
    online["status"] = "Online"

    device_repository.add_device(online)

    assert device_repository.get_device_count() == 2
    assert device_repository.get_online_device_count() == 1


# ============================================================
# VALIDATION
# ============================================================

@pytest.mark.parametrize(
    "invalid_name",
    ["", "   ", None],
)
def test_invalid_device_name(
    device_repository,
    sample_device,
    invalid_name,
):
    """Verify that device names are required."""

    device = sample_device.copy()
    device["name"] = invalid_name

    with pytest.raises(ValueError):
        device_repository.add_device(device)


def test_missing_device_type(device_repository, sample_device):
    """Verify that device types are required."""

    device = sample_device.copy()
    device["device_type"] = ""

    with pytest.raises(ValueError):
        device_repository.add_device(device)


@pytest.mark.parametrize(
    "invalid_ip",
    [
        "999.999.999.999",
        "192.168.1",
        "not-an-ip",
    ],
)
def test_invalid_ip_address(
    device_repository,
    sample_device,
    invalid_ip,
):
    """Verify invalid IP addresses are rejected."""

    device = sample_device.copy()
    device["ip_address"] = invalid_ip

    with pytest.raises(ValueError):
        device_repository.add_device(device)


def test_valid_ipv6_address(device_repository, sample_device):
    """Verify that IPv6 addresses are accepted."""

    device = sample_device.copy()
    device["ip_address"] = "2001:db8::1"

    device_id = device_repository.add_device(device)

    assert device_repository.get_device(device_id)[
        "ip_address"
    ] == "2001:db8::1"


def test_invalid_device_status(device_repository, sample_device):
    """Verify invalid device statuses are rejected."""

    device = sample_device.copy()
    device["status"] = "Unknown"

    with pytest.raises(ValueError):
        device_repository.add_device(device)


# ============================================================
# DATABASE PERSISTENCE
# ============================================================

def test_device_persistence(
    device_repository,
    test_database,
    sample_device,
):
    """Verify records persist across repository instances."""

    device_id = device_repository.add_device(sample_device)

    new_repository = DeviceRepository(
        database=test_database
    )

    device = new_repository.get_device(device_id)

    assert device is not None
    assert device["name"] == "Robot Pi"