"""
CircuitVault - Project Repository
Version: 0.1.0

SQLite operations for projects and their components.
"""

import sqlite3

from database.database import DatabaseManager


class ProjectRepository:
    """Manage projects and component assignments."""

    STATUSES = ("Planning", "Active", "On Hold", "Completed")

    def __init__(self, database=None):
        self.database = database or DatabaseManager()

    @classmethod
    def validate_project(cls, project):
        name = str(project.get("name") or "").strip()
        description = str(
            project.get("description") or ""
        ).strip()
        status = str(
            project.get("status") or "Planning"
        ).strip()

        if not name:
            raise ValueError("Project name is required.")

        if status not in cls.STATUSES:
            raise ValueError("Invalid project status.")

        return name, description, status

    def add_project(self, project):
        values = self.validate_project(project)

        with self.database.get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO projects (name, description, status)
                VALUES (?, ?, ?)
                """,
                values,
            )
            return cursor.lastrowid

    def get_all_projects(self):
        with self.database.get_connection() as connection:
            rows = connection.execute(
                """
                SELECT
                    p.*,
                    COUNT(pc.component_id) AS component_types,
                    COALESCE(
                        SUM(pc.quantity_used), 0
                    ) AS assigned_quantity
                FROM projects AS p
                LEFT JOIN project_components AS pc
                    ON pc.project_id = p.id
                GROUP BY p.id
                ORDER BY p.name COLLATE NOCASE, p.id
                """
            ).fetchall()

            return [dict(row) for row in rows]

    def get_project(self, project_id):
        with self.database.get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM projects WHERE id = ?",
                (project_id,),
            ).fetchone()

            return dict(row) if row else None

    def update_project(self, project_id, project):
        values = self.validate_project(project)

        with self.database.get_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE projects
                SET name = ?, description = ?, status = ?
                WHERE id = ?
                """,
                (*values, project_id),
            )

            return cursor.rowcount > 0

    def delete_project(self, project_id):
        with self.database.get_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM projects WHERE id = ?",
                (project_id,),
            )

            return cursor.rowcount > 0

    def search_projects(self, search_text):
        search_text = search_text.strip()

        if not search_text:
            return self.get_all_projects()

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
                    p.*,
                    COUNT(pc.component_id) AS component_types,
                    COALESCE(
                        SUM(pc.quantity_used), 0
                    ) AS assigned_quantity
                FROM projects AS p
                LEFT JOIN project_components AS pc
                    ON pc.project_id = p.id
                WHERE p.name LIKE ? ESCAPE '\\'
                   OR p.description LIKE ? ESCAPE '\\'
                   OR p.status LIKE ? ESCAPE '\\'
                GROUP BY p.id
                ORDER BY p.name COLLATE NOCASE, p.id
                """,
                (pattern,) * 3,
            ).fetchall()

            return [dict(row) for row in rows]

    def get_available_components(self):
        """Return inventory components for assignment."""

        with self.database.get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, name, category, quantity
                FROM components
                ORDER BY name COLLATE NOCASE, id
                """
            ).fetchall()

            return [dict(row) for row in rows]

    def get_project_components(self, project_id):
        """Return components associated with a project."""

        with self.database.get_connection() as connection:
            rows = connection.execute(
                """
                SELECT
                    pc.project_id,
                    pc.component_id,
                    c.name,
                    c.category,
                    c.quantity AS inventory_quantity,
                    pc.quantity_used
                FROM project_components AS pc
                JOIN components AS c
                    ON c.id = pc.component_id
                WHERE pc.project_id = ?
                ORDER BY c.name COLLATE NOCASE, c.id
                """,
                (project_id,),
            ).fetchall()

            return [dict(row) for row in rows]

    def assign_component(
        self,
        project_id,
        component_id,
        quantity_used,
    ):
        """
        Add or update a component assignment.

        This records project usage without changing inventory.
        """

        try:
            quantity_used = int(quantity_used)
        except (TypeError, ValueError):
            raise ValueError(
                "Assigned quantity must be an integer."
            ) from None

        if quantity_used <= 0:
            raise ValueError(
                "Assigned quantity must be greater than zero."
            )

        with self.database.get_connection() as connection:
            connection.execute(
                """
                INSERT INTO project_components (
                    project_id,
                    component_id,
                    quantity_used
                )
                VALUES (?, ?, ?)
                ON CONFLICT(project_id, component_id)
                DO UPDATE SET
                    quantity_used = excluded.quantity_used
                """,
                (project_id, component_id, quantity_used),
            )

    def remove_component(self, project_id, component_id):
        """Remove an association without deleting inventory."""

        with self.database.get_connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM project_components
                WHERE project_id = ?
                  AND component_id = ?
                """,
                (project_id, component_id),
            )

            return cursor.rowcount > 0

    def get_project_count(self):
        with self.database.get_connection() as connection:
            return connection.execute(
                "SELECT COUNT(*) FROM projects"
            ).fetchone()[0]