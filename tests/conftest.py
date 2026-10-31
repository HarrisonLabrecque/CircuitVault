"""
CircuitVault - Pytest Configuration
Version: 0.1.0

Shared fixtures for:
    - SQLite database tests
    - Component repository tests
    - Components page tests
    - Device repository tests
    - Devices page tests
"""

import pytest

from database.database import DatabaseManager
from database.component_repository import ComponentRepository
from database.device_repository import DeviceRepository

from app.pages.components_page import ComponentsPage
from app.pages.devices_page import DevicesPage


@pytest.fixture
def test_database(tmp_path):
    """Create a fresh temporary SQLite database for each test."""

    database_path = tmp_path / "test_circuitvault.db"

    database = DatabaseManager(database_path=database_path)
    database.initialize_database()

    return database


# ============================================================
# COMPONENT FIXTURES
# ============================================================

@pytest.fixture
def component_repository(test_database):
    """Create a component repository using the test database."""

    return ComponentRepository(database=test_database)


@pytest.fixture
def sample_component():
    """Return a sample electronic component."""

    return {
        "name": "MPU6050",
        "category": "Sensor",
        "manufacturer": "InvenSense",
        "part_number": "GY-521",
        "quantity": 3,
        "storage_location": "Drawer A1",
        "datasheet": "https://example.com/mpu6050.pdf",
        "notes": "Six-axis accelerometer and gyroscope",
    }


@pytest.fixture
def components_page(qtbot, component_repository):
    """Create a Components page with the test repository."""

    page = ComponentsPage()

    page.repository = component_repository
    page.refresh_components()

    qtbot.addWidget(page)

    return page


# ============================================================
# DEVICE FIXTURES
# ============================================================

@pytest.fixture
def device_repository(test_database):
    """Create a device repository using the test database."""

    return DeviceRepository(database=test_database)


@pytest.fixture
def sample_device():
    """Return sample registered device information."""

    return {
        "name": "Robot Pi",
        "device_type": "Raspberry Pi",
        "hostname": "robotpi.local",
        "ip_address": "192.168.1.20",
        "mac_address": "AA:BB:CC:DD:EE:01",
        "status": "Offline",
    }


@pytest.fixture
def devices_page(qtbot, device_repository):
    """Create a Devices page using the temporary database."""

    page = DevicesPage(repository=device_repository)

    qtbot.addWidget(page)

    return page