"""
CircuitVault - Pytest Configuration
Version: 0.1.0

Shared testing fixtures for:
    - Database
    - Components
    - Devices
    - Sensors
"""

import pytest

from database.database import DatabaseManager
from database.component_repository import ComponentRepository
from database.device_repository import DeviceRepository
from database.sensor_repository import SensorRepository

from app.pages.components_page import ComponentsPage
from app.pages.devices_page import DevicesPage
from app.pages.sensors_page import SensorsPage


# ============================================================
# DATABASE FIXTURES
# ============================================================

@pytest.fixture
def test_database(tmp_path):
    """Create an isolated SQLite database for each test."""

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
    """Return sample electronic component information."""

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
    """Create a Components page with an isolated repository."""

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
    """Create a Devices page using an isolated repository."""

    page = DevicesPage(repository=device_repository)

    qtbot.addWidget(page)

    return page


# ============================================================
# SENSOR FIXTURES
# ============================================================

@pytest.fixture
def sensor_repository(test_database):
    """Create a sensor repository using the test database."""

    return SensorRepository(database=test_database)


@pytest.fixture
def registered_device(device_repository, sample_device):
    """Register a device for sensor measurement tests."""

    return device_repository.add_device(sample_device)


@pytest.fixture
def sample_reading(registered_device):
    """Return a sample MPU6050 measurement."""

    return {
        "device_id": registered_device,
        "sensor_name": "MPU6050",
        "metric": "Acceleration X",
        "value": 0.12,
        "unit": "g",
    }


@pytest.fixture
def sensors_page(qtbot, sensor_repository):
    """Create a Sensors page using an isolated repository."""

    page = SensorsPage(repository=sensor_repository)

    qtbot.addWidget(page)

    return page