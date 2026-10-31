"""
CircuitVault - Database Unit Tests
Version: 0.1.0

Tests:
    - Database initialization
    - Table creation
    - Component storage
    - Device storage
    - Project storage
    - Sensor readings
    - Dashboard statistics
    - Foreign key constraints
    - Transaction rollback
    - Data validation
"""

import sqlite3

import pytest


# ============================================================
# DATABASE INITIALIZATION TESTS
# ============================================================

def test_database_file_created(test_database):
    """Verify that SQLite creates the database file."""

    assert test_database.database_path.exists()


def test_database_tables_created(test_database):
    """Verify that all required database tables exist."""

    expected_tables = {
        "components",
        "devices",
        "projects",
        "project_components",
        "sensor_readings",
    }

    with test_database.get_connection() as connection:

        cursor = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
        """)

        actual_tables = {
            row["name"]
            for row in cursor.fetchall()
        }

    assert expected_tables.issubset(actual_tables)


def test_database_initialization_is_repeatable(test_database):
    """Verify that initialization can run multiple times."""

    test_database.initialize_database()
    test_database.initialize_database()

    assert test_database.database_path.exists()


# ============================================================
# COMPONENT TESTS
# ============================================================

def test_insert_component(test_database):
    """Verify that components can be inserted."""

    with test_database.get_connection() as connection:

        connection.execute("""
            INSERT INTO components (
                name,
                category,
                manufacturer,
                part_number,
                quantity
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            "MPU6050",
            "Sensor",
            "InvenSense",
            "GY-521",
            3
        ))

    with test_database.get_connection() as connection:

        component = connection.execute("""
            SELECT *
            FROM components
            WHERE name = ?
        """, ("MPU6050",)).fetchone()

    assert component is not None
    assert component["name"] == "MPU6050"
    assert component["category"] == "Sensor"
    assert component["quantity"] == 3


def test_component_quantity_cannot_be_negative(test_database):
    """Verify that component quantities cannot be negative."""

    with pytest.raises(sqlite3.IntegrityError):

        with test_database.get_connection() as connection:

            connection.execute("""
                INSERT INTO components (
                    name,
                    category,
                    quantity
                )
                VALUES (?, ?, ?)
            """, (
                "ESP32-S3",
                "Microcontroller",
                -5
            ))


def test_component_name_is_required(test_database):
    """Verify that a component requires a name."""

    with pytest.raises(sqlite3.IntegrityError):

        with test_database.get_connection() as connection:

            connection.execute("""
                INSERT INTO components (
                    category,
                    quantity
                )
                VALUES (?, ?)
            """, (
                "Sensor",
                2
            ))


# ============================================================
# DEVICE TESTS
# ============================================================

def test_insert_device(test_database):
    """Verify that devices can be registered."""

    with test_database.get_connection() as connection:

        connection.execute("""
            INSERT INTO devices (
                name,
                device_type,
                hostname,
                ip_address,
                status
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            "Robot Pi",
            "Raspberry Pi",
            "robotpi.local",
            "192.168.1.20",
            "Online"
        ))

    with test_database.get_connection() as connection:

        device = connection.execute("""
            SELECT *
            FROM devices
            WHERE name = ?
        """, ("Robot Pi",)).fetchone()

    assert device is not None
    assert device["device_type"] == "Raspberry Pi"
    assert device["status"] == "Online"


def test_device_default_status(test_database):
    """Verify that new devices default to Offline."""

    with test_database.get_connection() as connection:

        connection.execute("""
            INSERT INTO devices (
                name,
                device_type
            )
            VALUES (?, ?)
        """, (
            "ESP32 Sensor Node",
            "ESP32"
        ))

    with test_database.get_connection() as connection:

        device = connection.execute("""
            SELECT status
            FROM devices
            WHERE name = ?
        """, ("ESP32 Sensor Node",)).fetchone()

    assert device["status"] == "Offline"


def test_invalid_device_status(test_database):
    """Verify that invalid device statuses are rejected."""

    with pytest.raises(sqlite3.IntegrityError):

        with test_database.get_connection() as connection:

            connection.execute("""
                INSERT INTO devices (
                    name,
                    device_type,
                    status
                )
                VALUES (?, ?, ?)
            """, (
                "Test Device",
                "ESP32",
                "Unknown"
            ))


# ============================================================
# PROJECT TESTS
# ============================================================

def test_insert_project(test_database):
    """Verify that projects can be stored."""

    with test_database.get_connection() as connection:

        connection.execute("""
            INSERT INTO projects (
                name,
                description
            )
            VALUES (?, ?)
        """, (
            "ESP32 Flight Controller",
            "Flight controller prototype"
        ))

    with test_database.get_connection() as connection:

        project = connection.execute("""
            SELECT *
            FROM projects
            WHERE name = ?
        """, ("ESP32 Flight Controller",)).fetchone()

    assert project is not None
    assert project["status"] == "Active"


def test_project_component_relationship(test_database):
    """Verify that components can be assigned to projects."""

    with test_database.get_connection() as connection:

        component_id = connection.execute("""
            INSERT INTO components (
                name,
                category,
                quantity
            )
            VALUES (?, ?, ?)
        """, (
            "MPU6050",
            "Sensor",
            3
        )).lastrowid

        project_id = connection.execute("""
            INSERT INTO projects (
                name
            )
            VALUES (?)
        """, (
            "Flight Controller",
        )).lastrowid

        connection.execute("""
            INSERT INTO project_components (
                project_id,
                component_id,
                quantity_used
            )
            VALUES (?, ?, ?)
        """, (
            project_id,
            component_id,
            2
        ))

    with test_database.get_connection() as connection:

        relationship = connection.execute("""
            SELECT quantity_used
            FROM project_components
            WHERE project_id = ?
              AND component_id = ?
        """, (
            project_id,
            component_id
        )).fetchone()

    assert relationship is not None
    assert relationship["quantity_used"] == 2


# ============================================================
# SENSOR READING TESTS
# ============================================================

def test_insert_sensor_reading(test_database):
    """Verify that sensor readings can be stored."""

    with test_database.get_connection() as connection:

        device_id = connection.execute("""
            INSERT INTO devices (
                name,
                device_type
            )
            VALUES (?, ?)
        """, (
            "ESP32-S3",
            "ESP32"
        )).lastrowid

        connection.execute("""
            INSERT INTO sensor_readings (
                device_id,
                sensor_name,
                metric,
                value,
                unit
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            device_id,
            "MPU6050",
            "acceleration_x",
            0.12,
            "g"
        ))

    with test_database.get_connection() as connection:

        reading = connection.execute("""
            SELECT *
            FROM sensor_readings
            WHERE device_id = ?
        """, (device_id,)).fetchone()

    assert reading is not None
    assert reading["sensor_name"] == "MPU6050"
    assert reading["value"] == pytest.approx(0.12)
    assert reading["unit"] == "g"
    assert reading["timestamp"] is not None


# ============================================================
# DASHBOARD STATISTICS TESTS
# ============================================================

def test_empty_dashboard_statistics(test_database):
    """Verify that an empty database returns zero statistics."""

    statistics = test_database.get_dashboard_statistics()

    assert statistics == {
        "total_components": 0,
        "known_devices": 0,
        "online_devices": 0,
        "sensor_readings": 0
    }


def test_dashboard_statistics_with_data(test_database):
    """Verify that dashboard statistics reflect stored data."""

    with test_database.get_connection() as connection:

        connection.execute("""
            INSERT INTO components (
                name,
                category,
                quantity
            )
            VALUES (?, ?, ?)
        """, (
            "MPU6050",
            "Sensor",
            3
        ))

        online_device_id = connection.execute("""
            INSERT INTO devices (
                name,
                device_type,
                status
            )
            VALUES (?, ?, ?)
        """, (
            "Robot Pi",
            "Raspberry Pi",
            "Online"
        )).lastrowid

        connection.execute("""
            INSERT INTO devices (
                name,
                device_type,
                status
            )
            VALUES (?, ?, ?)
        """, (
            "ESP32 Node",
            "ESP32",
            "Offline"
        ))

        connection.execute("""
            INSERT INTO sensor_readings (
                device_id,
                sensor_name,
                metric,
                value
            )
            VALUES (?, ?, ?, ?)
        """, (
            online_device_id,
            "Temperature Sensor",
            "temperature",
            24.5
        ))

    statistics = test_database.get_dashboard_statistics()

    assert statistics["total_components"] == 1
    assert statistics["known_devices"] == 2
    assert statistics["online_devices"] == 1
    assert statistics["sensor_readings"] == 1


# ============================================================
# FOREIGN KEY TESTS
# ============================================================

def test_foreign_key_enforcement(test_database):
    """Verify that invalid device references are rejected."""

    with pytest.raises(sqlite3.IntegrityError):

        with test_database.get_connection() as connection:

            connection.execute("""
                INSERT INTO sensor_readings (
                    device_id,
                    sensor_name,
                    metric,
                    value
                )
                VALUES (?, ?, ?, ?)
            """, (
                9999,
                "MPU6050",
                "acceleration_x",
                0.5
            ))


def test_foreign_key_cascade_delete(test_database):
    """Verify that deleting a device removes its readings."""

    with test_database.get_connection() as connection:

        device_id = connection.execute("""
            INSERT INTO devices (
                name,
                device_type
            )
            VALUES (?, ?)
        """, (
            "Test ESP32",
            "ESP32"
        )).lastrowid

        connection.execute("""
            INSERT INTO sensor_readings (
                device_id,
                sensor_name,
                metric,
                value
            )
            VALUES (?, ?, ?, ?)
        """, (
            device_id,
            "MPU6050",
            "acceleration_x",
            0.25
        ))

    with test_database.get_connection() as connection:

        connection.execute("""
            DELETE FROM devices
            WHERE id = ?
        """, (device_id,))

    with test_database.get_connection() as connection:

        remaining = connection.execute("""
            SELECT COUNT(*)
            FROM sensor_readings
        """).fetchone()[0]

    assert remaining == 0


# ============================================================
# TRANSACTION TESTS
# ============================================================

def test_transaction_rollback(test_database):
    """Verify that failed transactions are rolled back."""

    with pytest.raises(sqlite3.IntegrityError):

        with test_database.get_connection() as connection:

            connection.execute("""
                INSERT INTO components (
                    name,
                    category,
                    quantity
                )
                VALUES (?, ?, ?)
            """, (
                "Valid Component",
                "Sensor",
                2
            ))

            connection.execute("""
                INSERT INTO components (
                    name,
                    category,
                    quantity
                )
                VALUES (?, ?, ?)
            """, (
                "Invalid Component",
                "Sensor",
                -10
            ))

    with test_database.get_connection() as connection:

        count = connection.execute("""
            SELECT COUNT(*)
            FROM components
        """).fetchone()[0]

    assert count == 0