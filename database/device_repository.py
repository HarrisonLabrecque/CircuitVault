"""
CircuitVault - Device Repository
Version: 0.1.0

SQLite operations for registered electronic devices.
"""

import ipaddress
import sqlite3

from database.database import DatabaseManager


class DeviceRepository:
    """Manage registered devices."""

    def __init__(self, database=None):
        self.database = database or DatabaseManager()

    @staticmethod
    def validate_device(device):
        """Validate and normalize device information."""

        name = str(device.get("name") or "").strip()
        device_type = str(device.get("device_type") or "").strip()
        hostname = str(device.get("hostname") or "").strip()
        ip_address = str(device.get("ip_address") or "").strip()
        mac_address = str(device.get("mac_address") or "").strip()
        status = str(device.get("status") or "Offline").strip()

        if not name:
            raise ValueError("Device name is required.")

        if not device_type:
            raise ValueError("Device type is required.")

        if status not in ("Online", "Offline"):
            raise ValueError("Status must be Online or Offline.")

        if ip_address:
            try:
                ipaddress.ip_address(ip_address)
            except ValueError:
                raise ValueError(
                    "Enter a valid IPv4 or IPv6 address."
                ) from None

        return (
            name,
            device_type,
            hostname,
            ip_address,
            mac_address,
            status,
        )

    def add_device(self, device):
        """Insert a registered device."""

        values = self.validate_device(device)

        with self.database.get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO devices (
                    name,
                    device_type,
                    hostname,
                    ip_address,
                    mac_address,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                values,
            )

            return cursor.lastrowid

    def get_all_devices(self):
        """Return registered devices alphabetically."""

        with self.database.get_connection() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM devices
                ORDER BY name COLLATE NOCASE, id
                """
            ).fetchall()

            return [dict(row) for row in rows]

    def get_device(self, device_id):
        """Retrieve a device by ID."""

        with self.database.get_connection() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM devices
                WHERE id = ?
                """,
                (device_id,),
            ).fetchone()

            return dict(row) if row else None

    def update_device(self, device_id, device):
        """Update an existing device."""

        values = self.validate_device(device)

        with self.database.get_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE devices
                SET
                    name = ?,
                    device_type = ?,
                    hostname = ?,
                    ip_address = ?,
                    mac_address = ?,
                    status = ?
                WHERE id = ?
                """,
                (*values, device_id),
            )

            return cursor.rowcount > 0

    def delete_device(self, device_id):
        """Delete a registered device."""

        with self.database.get_connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM devices
                WHERE id = ?
                """,
                (device_id,),
            )

            return cursor.rowcount > 0

    def search_devices(self, search_text):
        """Search devices by identifying information."""

        search_text = search_text.strip()

        if not search_text:
            return self.get_all_devices()

        # Escape SQL LIKE wildcard characters so searches
        # match the user's literal text.
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
                SELECT *
                FROM devices
                WHERE name LIKE ? ESCAPE '\\'
                   OR device_type LIKE ? ESCAPE '\\'
                   OR hostname LIKE ? ESCAPE '\\'
                   OR ip_address LIKE ? ESCAPE '\\'
                   OR mac_address LIKE ? ESCAPE '\\'
                   OR status LIKE ? ESCAPE '\\'
                ORDER BY name COLLATE NOCASE, id
                """,
                (pattern,) * 6,
            ).fetchall()

            return [dict(row) for row in rows]

    def get_device_count(self):
        """Count all registered devices."""

        with self.database.get_connection() as connection:
            return connection.execute(
                "SELECT COUNT(*) FROM devices"
            ).fetchone()[0]

    def get_online_device_count(self):
        """Count devices marked Online."""

        with self.database.get_connection() as connection:
            return connection.execute(
                """
                SELECT COUNT(*)
                FROM devices
                WHERE status = ?
                """,
                ("Online",),
            ).fetchone()[0]