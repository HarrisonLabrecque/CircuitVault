"""
CircuitVault - Component Repository
Version: 0.1.0

Handles:
    - Adding components
    - Retrieving components
    - Updating components
    - Deleting components
    - Searching components
"""

from database.database import DatabaseManager


class ComponentRepository:
    """Manage component inventory records."""

    FIELDS = (
        "name",
        "category",
        "manufacturer",
        "part_number",
        "quantity",
        "storage_location",
        "datasheet",
        "notes",
    )

    def __init__(self, database=None):
        self.database = database or DatabaseManager()

    def add_component(self, component):
        """Insert a new component and return its ID."""

        values = self._validate_component(component)

        with self.database.get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO components (
                    name,
                    category,
                    manufacturer,
                    part_number,
                    quantity,
                    storage_location,
                    datasheet,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                values,
            )

            return cursor.lastrowid

    def get_all_components(self):
        """Retrieve all components ordered by name."""

        with self.database.get_connection() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM components
                ORDER BY name COLLATE NOCASE, id
                """
            ).fetchall()

            return [dict(row) for row in rows]

    def get_component(self, component_id):
        """Retrieve one component by ID."""

        with self.database.get_connection() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM components
                WHERE id = ?
                """,
                (component_id,),
            ).fetchone()

            return dict(row) if row else None

    def update_component(self, component_id, component):
        """Update an existing component."""

        values = self._validate_component(component)

        with self.database.get_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE components
                SET
                    name = ?,
                    category = ?,
                    manufacturer = ?,
                    part_number = ?,
                    quantity = ?,
                    storage_location = ?,
                    datasheet = ?,
                    notes = ?
                WHERE id = ?
                """,
                (*values, component_id),
            )

            return cursor.rowcount > 0

    def delete_component(self, component_id):
        """Delete a component by ID."""

        with self.database.get_connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM components
                WHERE id = ?
                """,
                (component_id,),
            )

            return cursor.rowcount > 0

    def search_components(self, search_text):
        """Search component inventory records."""

        search_text = search_text.strip()

        if not search_text:
            return self.get_all_components()

        pattern = f"%{search_text}%"

        with self.database.get_connection() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM components
                WHERE name LIKE ?
                   OR category LIKE ?
                   OR manufacturer LIKE ?
                   OR part_number LIKE ?
                   OR storage_location LIKE ?
                ORDER BY name COLLATE NOCASE, id
                """,
                (pattern,) * 5,
            ).fetchall()

            return [dict(row) for row in rows]

    def get_component_count(self):
        """Return the number of component records."""

        with self.database.get_connection() as connection:
            return connection.execute(
                "SELECT COUNT(*) FROM components"
            ).fetchone()[0]

    @classmethod
    def _validate_component(cls, component):
        """Validate and normalize component data."""

        name = str(component.get("name") or "").strip()
        category = str(component.get("category") or "").strip()

        if not name:
            raise ValueError("Component name is required.")

        if not category:
            raise ValueError("Component category is required.")

        quantity = component.get("quantity", 0)

        if isinstance(quantity, bool):
            raise ValueError("Quantity must be a non-negative integer.")

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            raise ValueError(
                "Quantity must be a non-negative integer."
            ) from None

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        normalized = {
            "name": name,
            "category": category,
            "manufacturer": str(
                component.get("manufacturer") or ""
            ).strip(),
            "part_number": str(
                component.get("part_number") or ""
            ).strip(),
            "quantity": quantity,
            "storage_location": str(
                component.get("storage_location") or ""
            ).strip(),
            "datasheet": str(
                component.get("datasheet") or ""
            ).strip(),
            "notes": str(
                component.get("notes") or ""
            ).strip(),
        }

        return tuple(normalized[field] for field in cls.FIELDS)