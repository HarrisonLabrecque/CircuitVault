"""
CircuitVault - Database Manager
Version: 0.1.0

Handles:
    - SQLite database connections
    - Database initialization
    - Component inventory storage
    - Registered device storage
    - Project storage
    - Sensor reading storage
    - Dashboard statistics

Supports:
    - Development database storage
    - Persistent packaged application storage
    - Isolated test databases
"""

import os
import sys
import sqlite3

from pathlib import Path
from contextlib import contextmanager


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


def get_database_path():
    """
    Return the appropriate SQLite database path.

    Development:
        CircuitVault/data/circuitvault.db

    PyInstaller:
        %LOCALAPPDATA%/CircuitVault/circuitvault.db
    """

    if getattr(sys, "frozen", False):

        local_app_data = os.environ.get("LOCALAPPDATA")

        if local_app_data:

            database_dir = (
                Path(local_app_data) / "CircuitVault"
            )

        else:

            database_dir = (
                Path.home() / "CircuitVault"
            )

    else:

        database_dir = BASE_DIR / "data"

    return database_dir / "circuitvault.db"


DATABASE_PATH = get_database_path()


# ============================================================
# DATABASE MANAGER
# ============================================================

class DatabaseManager:
    """Manage the CircuitVault SQLite database."""

    def __init__(self, database_path=None):

        self.database_path = (
            Path(database_path)
            if database_path is not None
            else get_database_path()
        )

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    # --------------------------------------------------------
    # Database Connection
    # --------------------------------------------------------

    @contextmanager
    def get_connection(self):
        """Provide a SQLite connection with transaction handling."""

        connection = sqlite3.connect(
            self.database_path
        )

        connection.row_factory = sqlite3.Row

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        try:

            yield connection

            connection.commit()

        except Exception:

            connection.rollback()

            raise

        finally:

            connection.close()

    # --------------------------------------------------------
    # Database Initialization
    # --------------------------------------------------------

    def initialize_database(self):
        """Create all required database tables."""

        with self.get_connection() as connection:

            # ------------------------------------------------
            # Components Table
            # ------------------------------------------------

            connection.execute("""
                CREATE TABLE IF NOT EXISTS components (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    name TEXT NOT NULL,

                    category TEXT NOT NULL,

                    manufacturer TEXT,

                    part_number TEXT,

                    quantity INTEGER NOT NULL DEFAULT 0
                        CHECK(quantity >= 0),

                    storage_location TEXT,

                    datasheet TEXT,

                    notes TEXT,

                    created_at TEXT DEFAULT CURRENT_TIMESTAMP

                )
            """)

            # ------------------------------------------------
            # Devices Table
            # ------------------------------------------------

            connection.execute("""
                CREATE TABLE IF NOT EXISTS devices (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    name TEXT NOT NULL,

                    device_type TEXT NOT NULL,

                    hostname TEXT,

                    ip_address TEXT,

                    mac_address TEXT,

                    status TEXT NOT NULL DEFAULT 'Offline'
                        CHECK(status IN ('Online', 'Offline')),

                    last_seen TEXT,

                    created_at TEXT DEFAULT CURRENT_TIMESTAMP

                )
            """)

            # ------------------------------------------------
            # Projects Table
            # ------------------------------------------------

            connection.execute("""
                CREATE TABLE IF NOT EXISTS projects (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    name TEXT NOT NULL,

                    description TEXT,

                    status TEXT DEFAULT 'Active',

                    created_at TEXT DEFAULT CURRENT_TIMESTAMP

                )
            """)

            # ------------------------------------------------
            # Project Components Table
            # ------------------------------------------------

            connection.execute("""
                CREATE TABLE IF NOT EXISTS project_components (

                    project_id INTEGER NOT NULL,

                    component_id INTEGER NOT NULL,

                    quantity_used INTEGER NOT NULL DEFAULT 1
                        CHECK(quantity_used > 0),

                    PRIMARY KEY (project_id, component_id),

                    FOREIGN KEY (project_id)
                        REFERENCES projects(id)
                        ON DELETE CASCADE,

                    FOREIGN KEY (component_id)
                        REFERENCES components(id)
                        ON DELETE CASCADE

                )
            """)

            # ------------------------------------------------
            # Sensor Readings Table
            # ------------------------------------------------

            connection.execute("""
                CREATE TABLE IF NOT EXISTS sensor_readings (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    device_id INTEGER NOT NULL,

                    sensor_name TEXT NOT NULL,

                    metric TEXT NOT NULL,

                    value REAL NOT NULL,

                    unit TEXT,

                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (device_id)
                        REFERENCES devices(id)
                        ON DELETE CASCADE

                )
            """)

            # ------------------------------------------------
            # Database Indexes
            # ------------------------------------------------

            connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_components_category
                ON components(category)
            """)

            connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_devices_status
                ON devices(status)
            """)

            connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_sensor_readings_device_time
                ON sensor_readings(device_id, timestamp)
            """)

    # --------------------------------------------------------
    # Dashboard Statistics
    # --------------------------------------------------------

    def get_dashboard_statistics(self):
        """Return statistics for the dashboard metric cards."""

        with self.get_connection() as connection:

            total_components = connection.execute("""
                SELECT COUNT(*)
                FROM components
            """).fetchone()[0]

            known_devices = connection.execute("""
                SELECT COUNT(*)
                FROM devices
            """).fetchone()[0]

            online_devices = connection.execute("""
                SELECT COUNT(*)
                FROM devices
                WHERE status = ?
            """, ("Online",)).fetchone()[0]

            sensor_readings = connection.execute("""
                SELECT COUNT(*)
                FROM sensor_readings
            """).fetchone()[0]

        return {
            "total_components": total_components,
            "known_devices": known_devices,
            "online_devices": online_devices,
            "sensor_readings": sensor_readings
        }


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    database = DatabaseManager()

    database.initialize_database()

    statistics = database.get_dashboard_statistics()

    print(
        "CircuitVault database initialized successfully."
    )

    print(
        f"Database location: {database.database_path}"
    )

    print("\nDashboard Statistics")

    for key, value in statistics.items():

        print(f"{key}: {value}")