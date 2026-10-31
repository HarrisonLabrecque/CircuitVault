"""
CircuitVault - Final Integration Tests
Version: 0.1.0

Tests:
    - Main window initialization
    - Sidebar navigation
    - Page refreshing
    - Shared SQLite database
    - Dashboard statistics
    - Component/project relationships
    - Device/sensor relationships
    - Foreign-key cascade behavior
    - Database persistence

All database tests use an isolated temporary SQLite database.
"""

import sqlite3

import pytest

from PySide6.QtWidgets import QWidget

import app.main_window as main_window_module

from database.component_repository import ComponentRepository
from database.device_repository import DeviceRepository
from database.sensor_repository import SensorRepository
from database.project_repository import ProjectRepository


# ============================================================
# MAIN WINDOW FIXTURES
# ============================================================

class IntegrationTestPage(QWidget):
    """Lightweight page used to test navigation."""

    def __init__(self):
        super().__init__()
        self.refresh_count = 0

    def refresh_metrics(self):
        self.refresh_count += 1

    def refresh_components(self):
        self.refresh_count += 1

    def refresh_devices(self):
        self.refresh_count += 1

    def refresh_readings(self):
        self.refresh_count += 1

    def refresh_projects(self):
        self.refresh_count += 1


@pytest.fixture
def main_window(qtbot, monkeypatch):
    """
    Create MainWindow with isolated test pages.

    Navigation uses the real MainWindow implementation.
    Database-backed pages are replaced to prevent access
    to the application's production database.
    """

    page_classes = [
        "DashboardPage",
        "ComponentsPage",
        "DevicesPage",
        "SensorsPage",
        "ProjectsPage",
    ]

    for class_name in page_classes:
        monkeypatch.setattr(
            main_window_module,
            class_name,
            IntegrationTestPage,
        )

    window = main_window_module.MainWindow()

    qtbot.addWidget(window)

    return window


# ============================================================
# MAIN WINDOW INITIALIZATION
# ============================================================

def test_main_window_created(main_window):
    assert main_window is not None

    assert main_window.windowTitle() == "CircuitVault"


def test_main_window_has_five_pages(main_window):
    assert main_window.pages.count() == 5


def test_main_window_has_five_navigation_buttons(main_window):
    assert len(main_window.navigation_buttons) == 5


def test_dashboard_is_default_page(main_window):
    assert main_window.pages.currentIndex() == 0


def test_dashboard_refreshes_on_startup(main_window):
    assert main_window.dashboard_page.refresh_count >= 1


# ============================================================
# NAVIGATION
# ============================================================

@pytest.mark.parametrize(
    "page_index",
    [0, 1, 2, 3, 4],
)
def test_navigation_to_each_page(main_window, page_index):
    main_window.navigate_to(page_index)

    assert main_window.pages.currentIndex() == page_index


@pytest.mark.parametrize(
    "page_index, page_attribute",
    [
        (0, "dashboard_page"),
        (1, "components_page"),
        (2, "devices_page"),
        (3, "sensors_page"),
        (4, "projects_page"),
    ],
)
def test_navigation_refreshes_selected_page(
    main_window,
    page_index,
    page_attribute,
):
    page = getattr(main_window, page_attribute)

    before = page.refresh_count

    main_window.navigate_to(page_index)

    assert page.refresh_count == before + 1


def test_navigation_updates_active_button(main_window):
    main_window.navigate_to(4)

    for index, button in enumerate(
        main_window.navigation_buttons
    ):
        assert button.property("active") == (index == 4)


def test_navigation_rejects_invalid_index(main_window):
    main_window.navigate_to(2)

    main_window.navigate_to(999)

    assert main_window.pages.currentIndex() == 2


def test_navigation_between_all_pages(main_window):
    for index in [0, 1, 2, 3, 4, 0]:
        main_window.navigate_to(index)

        assert main_window.pages.currentIndex() == index


# ============================================================
# SHARED DATABASE
# ============================================================

def test_repositories_share_database(
    test_database,
):
    component_repository = ComponentRepository(
        database=test_database
    )

    device_repository = DeviceRepository(
        database=test_database
    )

    sensor_repository = SensorRepository(
        database=test_database
    )

    project_repository = ProjectRepository(
        database=test_database
    )

    assert component_repository.database is test_database
    assert device_repository.database is test_database
    assert sensor_repository.database is test_database
    assert project_repository.database is test_database


def test_database_tables_exist(test_database):
    expected_tables = {
        "components",
        "devices",
        "projects",
        "project_components",
        "sensor_readings",
    }

    with test_database.get_connection() as connection:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

    existing_tables = {row["name"] for row in rows}

    assert expected_tables.issubset(existing_tables)


def test_foreign_keys_enabled(test_database):
    with test_database.get_connection() as connection:
        result = connection.execute(
            "PRAGMA foreign_keys"
        ).fetchone()[0]

    assert result == 1


# ============================================================
# DASHBOARD STATISTICS
# ============================================================

def test_initial_dashboard_statistics(test_database):
    statistics = test_database.get_dashboard_statistics()

    assert statistics["total_components"] == 0
    assert statistics["known_devices"] == 0
    assert statistics["online_devices"] == 0
    assert statistics["sensor_readings"] == 0


def test_dashboard_statistics_after_component_creation(
    test_database,
    component_repository,
    sample_component,
):
    component_repository.add_component(sample_component)

    statistics = test_database.get_dashboard_statistics()

    assert statistics["total_components"] == 1


def test_dashboard_statistics_after_device_creation(
    test_database,
    device_repository,
    sample_device,
):
    device_repository.add_device(sample_device)

    statistics = test_database.get_dashboard_statistics()

    assert statistics["known_devices"] == 1
    assert statistics["online_devices"] == 0


def test_dashboard_statistics_after_sensor_creation(
    test_database,
    sensor_repository,
    sample_reading,
):
    sensor_repository.add_reading(sample_reading)

    statistics = test_database.get_dashboard_statistics()

    assert statistics["sensor_readings"] == 1


def test_dashboard_statistics_after_device_deletion(
    test_database,
    device_repository,
    sensor_repository,
    sample_reading,
    registered_device,
):
    sensor_repository.add_reading(sample_reading)

    device_repository.delete_device(registered_device)

    statistics = test_database.get_dashboard_statistics()

    assert statistics["known_devices"] == 0
    assert statistics["sensor_readings"] == 0


# ============================================================
# COMPONENT AND PROJECT INTEGRATION
# ============================================================

def test_component_assignment_integration(
    component_repository,
    project_repository,
    registered_component,
    registered_project,
):
    project_repository.assign_component(
        registered_project,
        registered_component,
        2,
    )

    assignments = project_repository.get_project_components(
        registered_project
    )

    component = component_repository.get_component(
        registered_component
    )

    assert len(assignments) == 1
    assert assignments[0]["quantity_used"] == 2
    assert assignments[0]["name"] == component["name"]


def test_component_assignment_preserves_inventory(
    component_repository,
    project_repository,
    registered_component,
    registered_project,
):
    original = component_repository.get_component(
        registered_component
    )

    project_repository.assign_component(
        registered_project,
        registered_component,
        2,
    )

    updated = component_repository.get_component(
        registered_component
    )

    assert updated["quantity"] == original["quantity"]


def test_project_deletion_preserves_component(
    component_repository,
    project_repository,
    registered_component,
    registered_project,
):
    project_repository.assign_component(
        registered_project,
        registered_component,
        2,
    )

    project_repository.delete_project(registered_project)

    assert component_repository.get_component(
        registered_component
    ) is not None

    assert project_repository.get_project_components(
        registered_project
    ) == []


def test_component_deletion_cascades_assignment(
    component_repository,
    project_repository,
    registered_component,
    registered_project,
):
    project_repository.assign_component(
        registered_project,
        registered_component,
        2,
    )

    component_repository.delete_component(
        registered_component
    )

    assert project_repository.get_project_components(
        registered_project
    ) == []


# ============================================================
# DEVICE AND SENSOR INTEGRATION
# ============================================================

def test_sensor_reading_linked_to_device(
    sensor_repository,
    sample_reading,
):
    sensor_repository.add_reading(sample_reading)

    readings = sensor_repository.get_all_readings()

    assert len(readings) == 1
    assert readings[0]["device_name"] == "Robot Pi"
    assert readings[0]["sensor_name"] == "MPU6050"


def test_device_deletion_cascades_sensor_readings(
    device_repository,
    sensor_repository,
    sample_reading,
    registered_device,
):
    sensor_repository.add_reading(sample_reading)

    device_repository.delete_device(registered_device)

    assert sensor_repository.get_reading_count() == 0


def test_sensor_requires_registered_device(
    sensor_repository,
):
    reading = {
        "device_id": 9999,
        "sensor_name": "MPU6050",
        "metric": "Temperature",
        "value": 25.0,
        "unit": "C",
    }

    with pytest.raises(sqlite3.IntegrityError):
        sensor_repository.add_reading(reading)


# ============================================================
# CROSS-MODULE INTEGRATION
# ============================================================

def test_all_modules_store_data_together(
    test_database,
    component_repository,
    device_repository,
    sensor_repository,
    project_repository,
    sample_component,
    sample_device,
    sample_project,
):
    component_id = component_repository.add_component(
        sample_component
    )

    device_id = device_repository.add_device(
        sample_device
    )

    project_id = project_repository.add_project(
        sample_project
    )

    sensor_repository.add_reading({
        "device_id": device_id,
        "sensor_name": "MPU6050",
        "metric": "Acceleration X",
        "value": 0.12,
        "unit": "g",
    })

    project_repository.assign_component(
        project_id,
        component_id,
        2,
    )

    statistics = test_database.get_dashboard_statistics()

    assert statistics["total_components"] == 1
    assert statistics["known_devices"] == 1
    assert statistics["sensor_readings"] == 1

    assert project_repository.get_project_count() == 1

    assert len(
        project_repository.get_project_components(project_id)
    ) == 1


# ============================================================
# DATABASE PERSISTENCE
# ============================================================

def test_data_persists_across_repository_instances(
    test_database,
    component_repository,
    sample_component,
):
    component_id = component_repository.add_component(
        sample_component
    )

    second_repository = ComponentRepository(
        database=test_database
    )

    component = second_repository.get_component(
        component_id
    )

    assert component is not None
    assert component["name"] == "MPU6050"


def test_database_transaction_rollback(test_database):
    """
    Verify failed transactions do not leave partial changes.
    """

    with pytest.raises(RuntimeError):
        with test_database.get_connection() as connection:
            connection.execute(
                """
                INSERT INTO projects (name, status)
                VALUES (?, ?)
                """,
                ("Rollback Test", "Planning"),
            )

            raise RuntimeError("Simulated failure")

    with test_database.get_connection() as connection:
        count = connection.execute(
            """
            SELECT COUNT(*)
            FROM projects
            WHERE name = ?
            """,
            ("Rollback Test",),
        ).fetchone()[0]

    assert count == 0