"""
CircuitVault - Pytest Configuration
Version: 0.1.0

Shared pytest fixtures for:
    - SQLite Database
    - Components Repository and GUI
    - Devices Repository and GUI
    - Sensors Repository and GUI
    - Projects Repository and GUI

All database tests use isolated temporary SQLite databases.
"""

import pytest

# ============================================================
# DATABASE
# ============================================================

from database.database import DatabaseManager

# ============================================================
# REPOSITORIES
# ============================================================

from database.component_repository import ComponentRepository
from database.device_repository import DeviceRepository
from database.sensor_repository import SensorRepository
from database.project_repository import ProjectRepository

# ============================================================
# APPLICATION PAGES
# ============================================================

from app.pages.components_page import ComponentsPage
from app.pages.devices_page import DevicesPage
from app.pages.sensors_page import SensorsPage
from app.pages.projects_page import ProjectsPage


# ============================================================
# DATABASE FIXTURES
# ============================================================

@pytest.fixture
def test_database(tmp_path):
    """
    Create a temporary SQLite database.

    Each test receives its own isolated database.
    """

    database_path = tmp_path / "test_circuitvault.db"

    database = DatabaseManager(
        database_path=database_path
    )

    database.initialize_database()

    return database


# ============================================================
# COMPONENT FIXTURES
# ============================================================

@pytest.fixture
def component_repository(test_database):
    """Create a component repository using the test database."""

    return ComponentRepository(
        database=test_database
    )


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
def registered_component(
    component_repository,
    sample_component,
):
    """
    Insert a sample component.

    Returns the component's database ID.
    """

    return component_repository.add_component(
        sample_component
    )


@pytest.fixture
def components_page(
    qtbot,
    component_repository,
    monkeypatch,
):
    """
    Create a Components page using the temporary database.

    Patch the default repository before constructing the page
    so its initial refresh cannot access the real inventory.
    """

    monkeypatch.setattr(
        "app.pages.components_page.ComponentRepository",
        lambda: component_repository,
    )

    page = ComponentsPage()

    qtbot.addWidget(page)

    return page


# ============================================================
# DEVICE FIXTURES
# ============================================================

@pytest.fixture
def device_repository(test_database):
    """Create a device repository using the test database."""

    return DeviceRepository(
        database=test_database
    )


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
def registered_device(
    device_repository,
    sample_device,
):
    """
    Register a device.

    Returns the device's database ID.
    """

    return device_repository.add_device(
        sample_device
    )


@pytest.fixture
def devices_page(
    qtbot,
    device_repository,
):
    """Create a Devices page using the temporary database."""

    page = DevicesPage(
        repository=device_repository
    )

    qtbot.addWidget(page)

    return page


# ============================================================
# SENSOR FIXTURES
# ============================================================

@pytest.fixture
def sensor_repository(test_database):
    """Create a sensor repository using the test database."""

    return SensorRepository(
        database=test_database
    )


@pytest.fixture
def sample_reading(registered_device):
    """
    Return an MPU6050 sensor measurement.

    The reading belongs to a registered test device.
    """

    return {
        "device_id": registered_device,
        "sensor_name": "MPU6050",
        "metric": "Acceleration X",
        "value": 0.12,
        "unit": "g",
    }


@pytest.fixture
def registered_reading(
    sensor_repository,
    sample_reading,
):
    """
    Insert a sensor measurement.

    Returns the reading's database ID.
    """

    return sensor_repository.add_reading(
        sample_reading
    )


@pytest.fixture
def sensors_page(
    qtbot,
    sensor_repository,
):
    """Create a Sensors page using the temporary database."""

    page = SensorsPage(
        repository=sensor_repository
    )

    qtbot.addWidget(page)

    return page


# ============================================================
# PROJECT FIXTURES
# ============================================================

@pytest.fixture
def project_repository(test_database):
    """Create a project repository using the test database."""

    return ProjectRepository(
        database=test_database
    )


@pytest.fixture
def sample_project():
    """Return sample electronics project information."""

    return {
        "name": "ESP32-S3 Flight Controller",
        "description": (
            "Indoor flight controller prototype using "
            "ESP32-S3 and MPU6050 sensors."
        ),
        "status": "Active",
    }


@pytest.fixture
def registered_project(
    project_repository,
    sample_project,
):
    """
    Create a project.

    Returns the project's database ID.
    """

    return project_repository.add_project(
        sample_project
    )


@pytest.fixture
def projects_page(
    qtbot,
    project_repository,
):
    """Create a Projects page using the temporary database."""

    page = ProjectsPage(
        repository=project_repository
    )

    qtbot.addWidget(page)

    return page