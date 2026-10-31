"""
CircuitVault - Sensor Repository
Version: 0.1.0

SQLite operations for sensor readings.
"""

import math

from database.database import DatabaseManager


class SensorRepository:
    """Manage stored sensor measurements."""

    def __init__(self, database=None):
        self.database = database or DatabaseManager()

    @staticmethod
    def validate_reading(reading):
        """Validate and normalize sensor measurement data."""

        try:
            device_id = int(reading.get("device_id"))
        except (TypeError, ValueError):
            raise ValueError("A valid device is required.") from None

        if device_id <= 0:
            raise ValueError("A valid device is required.")

        sensor_name = str(
            reading.get("sensor_name") or ""
        ).strip()

        metric = str(
            reading.get("metric") or ""
        ).strip()

        unit = str(
            reading.get("unit") or ""
        ).strip()

        if not sensor_name:
            raise ValueError("Sensor name is required.")

        if not metric:
            raise ValueError("Measurement type is required.")

        try:
            value = float(reading.get("value"))
        except (TypeError, ValueError):
            raise ValueError("Measurement must be numeric.") from None

        if not math.isfinite(value):
            raise ValueError("Measurement must be finite.")

        return device_id, sensor_name, metric, value, unit

    def get_registered_devices(self):
        """Return available devices for sensor association."""

        with self.database.get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, name, device_type
                FROM devices
                ORDER BY name COLLATE NOCASE, id
                """
            ).fetchall()

            return [dict(row) for row in rows]

    def add_reading(self, reading):
        """Insert a sensor reading and return its ID."""

        values = self.validate_reading(reading)

        with self.database.get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO sensor_readings (
                    device_id,
                    sensor_name,
                    metric,
                    value,
                    unit
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                values,
            )

            return cursor.lastrowid

    def get_all_readings(self):
        """Retrieve readings with associated device names."""

        with self.database.get_connection() as connection:
            rows = connection.execute(
                """
                SELECT
                    sr.id,
                    sr.device_id,
                    d.name AS device_name,
                    sr.sensor_name,
                    sr.metric,
                    sr.value,
                    sr.unit,
                    sr.timestamp
                FROM sensor_readings AS sr
                JOIN devices AS d
                    ON d.id = sr.device_id
                ORDER BY sr.timestamp DESC, sr.id DESC
                """
            ).fetchall()

            return [dict(row) for row in rows]

    def get_reading(self, reading_id):
        """Retrieve one reading by ID."""

        with self.database.get_connection() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM sensor_readings
                WHERE id = ?
                """,
                (reading_id,),
            ).fetchone()

            return dict(row) if row else None

    def update_reading(self, reading_id, reading):
        """Update an existing sensor measurement."""

        values = self.validate_reading(reading)

        with self.database.get_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE sensor_readings
                SET
                    device_id = ?,
                    sensor_name = ?,
                    metric = ?,
                    value = ?,
                    unit = ?
                WHERE id = ?
                """,
                (*values, reading_id),
            )

            return cursor.rowcount > 0

    def delete_reading(self, reading_id):
        """Delete a sensor reading."""

        with self.database.get_connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM sensor_readings
                WHERE id = ?
                """,
                (reading_id,),
            )

            return cursor.rowcount > 0

    def search_readings(self, search_text):
        """Search readings by device, sensor, metric, or unit."""

        search_text = search_text.strip()

        if not search_text:
            return self.get_all_readings()

        escaped = (
            search_text
            .replace("\\", "\\\\")
            .replace("%", "\\%")
            .replace("_", "\\_")
        )

        pattern = f"%{escaped}%"

        with self.database.get_connection() as connection:
            rows = connection.execute(
                """
                SELECT
                    sr.id,
                    sr.device_id,
                    d.name AS device_name,
                    sr.sensor_name,
                    sr.metric,
                    sr.value,
                    sr.unit,
                    sr.timestamp
                FROM sensor_readings AS sr
                JOIN devices AS d
                    ON d.id = sr.device_id
                WHERE d.name LIKE ? ESCAPE '\\'
                   OR sr.sensor_name LIKE ? ESCAPE '\\'
                   OR sr.metric LIKE ? ESCAPE '\\'
                   OR sr.unit LIKE ? ESCAPE '\\'
                ORDER BY sr.timestamp DESC, sr.id DESC
                """,
                (pattern,) * 4,
            ).fetchall()

            return [dict(row) for row in rows]

    def get_reading_count(self):
        """Return the number of stored sensor readings."""

        with self.database.get_connection() as connection:
            return connection.execute(
                "SELECT COUNT(*) FROM sensor_readings"
            ).fetchone()[0]