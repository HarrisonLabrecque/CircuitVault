"""
CircuitVault - Project Repository Tests
Version: 0.1.0

Tests:
    - Project CRUD
    - Project validation
    - Project searching
    - Component assignments
    - Foreign-key relationships
    - Inventory preservation
    - Database persistence
"""

import sqlite3

import pytest

from database.project_repository import ProjectRepository


# ============================================================
# PROJECT CREATION
# ============================================================

def test_add_project(project_repository, sample_project):
    project_id = project_repository.add_project(sample_project)

    assert project_id > 0

    project = project_repository.get_project(project_id)

    assert project is not None
    assert project["name"] == "ESP32-S3 Flight Controller"
    assert project["status"] == "Active"


def test_add_multiple_projects(project_repository, sample_project):
    project_repository.add_project(sample_project)

    second = sample_project.copy()
    second["name"] = "ROS2 Robot"

    project_repository.add_project(second)

    assert project_repository.get_project_count() == 2


def test_add_minimal_project(project_repository):
    project_id = project_repository.add_project({
        "name": "Test Project",
    })

    project = project_repository.get_project(project_id)

    assert project["name"] == "Test Project"
    assert project["description"] == ""
    assert project["status"] == "Planning"


# ============================================================
# PROJECT RETRIEVAL
# ============================================================

def test_get_all_projects(project_repository, sample_project):
    project_repository.add_project(sample_project)

    projects = project_repository.get_all_projects()

    assert len(projects) == 1
    assert projects[0]["name"] == "ESP32-S3 Flight Controller"


def test_get_nonexistent_project(project_repository):
    assert project_repository.get_project(9999) is None


def test_projects_sorted_by_name(project_repository):
    project_repository.add_project({
        "name": "Zeta Project",
        "status": "Planning",
    })

    project_repository.add_project({
        "name": "Alpha Project",
        "status": "Active",
    })

    projects = project_repository.get_all_projects()

    assert projects[0]["name"] == "Alpha Project"
    assert projects[1]["name"] == "Zeta Project"


def test_project_initial_component_totals(
    project_repository,
    sample_project,
):
    project_repository.add_project(sample_project)

    projects = project_repository.get_all_projects()

    assert projects[0]["component_types"] == 0
    assert projects[0]["assigned_quantity"] == 0


# ============================================================
# PROJECT UPDATES
# ============================================================

def test_update_project(project_repository, sample_project):
    project_id = project_repository.add_project(sample_project)

    updated = sample_project.copy()
    updated["name"] = "Updated Flight Controller"
    updated["status"] = "Completed"

    result = project_repository.update_project(
        project_id,
        updated,
    )

    assert result is True

    project = project_repository.get_project(project_id)

    assert project["name"] == "Updated Flight Controller"
    assert project["status"] == "Completed"


def test_update_nonexistent_project(
    project_repository,
    sample_project,
):
    assert project_repository.update_project(
        9999,
        sample_project,
    ) is False


# ============================================================
# PROJECT DELETION
# ============================================================

def test_delete_project(project_repository, sample_project):
    project_id = project_repository.add_project(sample_project)

    assert project_repository.delete_project(project_id) is True
    assert project_repository.get_project(project_id) is None


def test_delete_nonexistent_project(project_repository):
    assert project_repository.delete_project(9999) is False


# ============================================================
# PROJECT SEARCH
# ============================================================

@pytest.mark.parametrize(
    "search_text",
    [
        "ESP32",
        "flight controller",
        "Active",
    ],
)
def test_search_project_fields(
    project_repository,
    sample_project,
    search_text,
):
    project_repository.add_project(sample_project)

    results = project_repository.search_projects(search_text)

    assert len(results) == 1


def test_search_case_insensitive(
    project_repository,
    sample_project,
):
    project_repository.add_project(sample_project)

    results = project_repository.search_projects("esp32")

    assert len(results) == 1


def test_search_no_matches(project_repository, sample_project):
    project_repository.add_project(sample_project)

    results = project_repository.search_projects(
        "Nonexistent Project"
    )

    assert results == []


def test_empty_search_returns_all(
    project_repository,
    sample_project,
):
    project_repository.add_project(sample_project)

    assert len(project_repository.search_projects("")) == 1


def test_search_literal_underscore(project_repository):
    project_repository.add_project({
        "name": "Flight_Controller",
        "status": "Planning",
    })

    project_repository.add_project({
        "name": "Flight Controller",
        "status": "Planning",
    })

    results = project_repository.search_projects("_")

    assert len(results) == 1
    assert results[0]["name"] == "Flight_Controller"


# ============================================================
# PROJECT VALIDATION
# ============================================================

@pytest.mark.parametrize(
    "invalid_name",
    ["", "   ", None],
)
def test_invalid_project_name(
    project_repository,
    sample_project,
    invalid_name,
):
    project = sample_project.copy()
    project["name"] = invalid_name

    with pytest.raises(ValueError):
        project_repository.add_project(project)


def test_invalid_project_status(
    project_repository,
    sample_project,
):
    project = sample_project.copy()
    project["status"] = "Unknown"

    with pytest.raises(ValueError):
        project_repository.add_project(project)


@pytest.mark.parametrize(
    "status",
    ["Planning", "Active", "On Hold", "Completed"],
)
def test_valid_project_statuses(project_repository, status):
    project_id = project_repository.add_project({
        "name": f"{status} Project",
        "status": status,
    })

    assert project_repository.get_project(project_id)["status"] == status


# ============================================================
# COMPONENT ASSIGNMENTS
# ============================================================

def test_assign_component(
    project_repository,
    registered_project,
    registered_component,
):
    project_repository.assign_component(
        registered_project,
        registered_component,
        3,
    )

    components = project_repository.get_project_components(
        registered_project
    )

    assert len(components) == 1
    assert components[0]["quantity_used"] == 3
    assert components[0]["name"] == "MPU6050"


def test_update_existing_assignment(
    project_repository,
    registered_project,
    registered_component,
):
    project_repository.assign_component(
        registered_project,
        registered_component,
        2,
    )

    project_repository.assign_component(
        registered_project,
        registered_component,
        5,
    )

    components = project_repository.get_project_components(
        registered_project
    )

    assert len(components) == 1
    assert components[0]["quantity_used"] == 5


def test_remove_component_assignment(
    project_repository,
    registered_project,
    registered_component,
):
    project_repository.assign_component(
        registered_project,
        registered_component,
        2,
    )

    result = project_repository.remove_component(
        registered_project,
        registered_component,
    )

    assert result is True
    assert project_repository.get_project_components(
        registered_project
    ) == []


def test_remove_nonexistent_assignment(
    project_repository,
    registered_project,
    registered_component,
):
    assert project_repository.remove_component(
        registered_project,
        registered_component,
    ) is False


def test_project_component_totals(
    project_repository,
    registered_project,
    registered_component,
):
    project_repository.assign_component(
        registered_project,
        registered_component,
        3,
    )

    project = project_repository.get_all_projects()[0]

    assert project["component_types"] == 1
    assert project["assigned_quantity"] == 3


def test_inventory_not_reduced(
    project_repository,
    component_repository,
    registered_project,
    registered_component,
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


def test_get_available_components(
    project_repository,
    registered_component,
):
    components = project_repository.get_available_components()

    assert len(components) == 1
    assert components[0]["name"] == "MPU6050"


# ============================================================
# ASSIGNMENT VALIDATION
# ============================================================

@pytest.mark.parametrize(
    "invalid_quantity",
    [0, -1, "invalid", None],
)
def test_invalid_assignment_quantity(
    project_repository,
    registered_project,
    registered_component,
    invalid_quantity,
):
    with pytest.raises(ValueError):
        project_repository.assign_component(
            registered_project,
            registered_component,
            invalid_quantity,
        )


def test_assign_nonexistent_component(
    project_repository,
    registered_project,
):
    with pytest.raises(sqlite3.IntegrityError):
        project_repository.assign_component(
            registered_project,
            9999,
            1,
        )


def test_assign_to_nonexistent_project(
    project_repository,
    registered_component,
):
    with pytest.raises(sqlite3.IntegrityError):
        project_repository.assign_component(
            9999,
            registered_component,
            1,
        )


# ============================================================
# FOREIGN KEY RELATIONSHIPS
# ============================================================

def test_project_deletion_removes_assignments(
    project_repository,
    component_repository,
    registered_project,
    registered_component,
):
    project_repository.assign_component(
        registered_project,
        registered_component,
        2,
    )

    project_repository.delete_project(registered_project)

    assert project_repository.get_project_components(
        registered_project
    ) == []

    # Inventory remains available.
    assert component_repository.get_component(
        registered_component
    ) is not None


def test_component_deletion_removes_assignment(
    project_repository,
    component_repository,
    registered_project,
    registered_component,
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
# DATABASE PERSISTENCE
# ============================================================

def test_project_persistence(
    project_repository,
    test_database,
    sample_project,
):
    project_id = project_repository.add_project(sample_project)

    new_repository = ProjectRepository(
        database=test_database
    )

    project = new_repository.get_project(project_id)

    assert project is not None
    assert project["name"] == "ESP32-S3 Flight Controller"


def test_assignment_persistence(
    project_repository,
    test_database,
    registered_project,
    registered_component,
):
    project_repository.assign_component(
        registered_project,
        registered_component,
        3,
    )

    new_repository = ProjectRepository(
        database=test_database
    )

    components = new_repository.get_project_components(
        registered_project
    )

    assert len(components) == 1
    assert components[0]["quantity_used"] == 3