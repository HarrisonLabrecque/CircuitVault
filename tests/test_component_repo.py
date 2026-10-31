"""
CircuitVault - Component Repository Tests
Version: 0.1.0

Tests:
    - Add components
    - Retrieve components
    - Update components
    - Delete components
    - Search components
    - Component counts
    - Data validation
    - Database persistence
"""

import pytest


# ============================================================
# CREATE OPERATIONS
# ============================================================

def test_add_component(component_repository, sample_component):
    """Verify that a component can be added."""

    component_id = component_repository.add_component(
        sample_component
    )

    assert component_id > 0

    component = component_repository.get_component(
        component_id
    )

    assert component is not None
    assert component["name"] == "MPU6050"
    assert component["category"] == "Sensor"
    assert component["quantity"] == 3


def test_add_multiple_components(
    component_repository,
    sample_component,
):
    """Verify that multiple components can be stored."""

    component_repository.add_component(sample_component)

    second_component = sample_component.copy()
    second_component["name"] = "ESP32-S3"
    second_component["category"] = "Microcontroller"

    component_repository.add_component(second_component)

    components = component_repository.get_all_components()

    assert len(components) == 2


def test_add_component_with_optional_fields_missing(
    component_repository,
):
    """Verify that optional fields may be omitted."""

    component_id = component_repository.add_component({
        "name": "Resistor",
        "category": "Resistor",
        "quantity": 10,
    })

    component = component_repository.get_component(
        component_id
    )

    assert component["manufacturer"] == ""
    assert component["notes"] == ""
    assert component["quantity"] == 10


# ============================================================
# READ OPERATIONS
# ============================================================

def test_get_all_components(
    component_repository,
    sample_component,
):
    """Verify that all stored components are returned."""

    component_repository.add_component(sample_component)

    components = component_repository.get_all_components()

    assert len(components) == 1
    assert components[0]["name"] == "MPU6050"


def test_get_nonexistent_component(component_repository):
    """Verify that missing records return None."""

    component = component_repository.get_component(9999)

    assert component is None


def test_components_sorted_by_name(component_repository):
    """Verify that inventory records are alphabetically ordered."""

    component_repository.add_component({
        "name": "Zener Diode",
        "category": "Diode",
        "quantity": 2,
    })

    component_repository.add_component({
        "name": "Arduino Nano",
        "category": "Microcontroller",
        "quantity": 1,
    })

    components = component_repository.get_all_components()

    assert [component["name"] for component in components] == [
        "Arduino Nano",
        "Zener Diode",
    ]


# ============================================================
# UPDATE OPERATIONS
# ============================================================

def test_update_component(
    component_repository,
    sample_component,
):
    """Verify that an existing component can be updated."""

    component_id = component_repository.add_component(
        sample_component
    )

    updated_data = sample_component.copy()
    updated_data["quantity"] = 5
    updated_data["storage_location"] = "Drawer B2"

    result = component_repository.update_component(
        component_id,
        updated_data,
    )

    assert result is True

    component = component_repository.get_component(
        component_id
    )

    assert component["quantity"] == 5
    assert component["storage_location"] == "Drawer B2"


def test_update_nonexistent_component(
    component_repository,
    sample_component,
):
    """Verify that updating a missing component returns False."""

    result = component_repository.update_component(
        9999,
        sample_component,
    )

    assert result is False


# ============================================================
# DELETE OPERATIONS
# ============================================================

def test_delete_component(
    component_repository,
    sample_component,
):
    """Verify that components can be deleted."""

    component_id = component_repository.add_component(
        sample_component
    )

    result = component_repository.delete_component(
        component_id
    )

    assert result is True

    assert component_repository.get_component(
        component_id
    ) is None


def test_delete_nonexistent_component(component_repository):
    """Verify that deleting a missing component returns False."""

    result = component_repository.delete_component(9999)

    assert result is False


# ============================================================
# SEARCH OPERATIONS
# ============================================================

def test_search_component_by_name(
    component_repository,
    sample_component,
):
    """Verify searching by component name."""

    component_repository.add_component(sample_component)

    results = component_repository.search_components(
        "MPU"
    )

    assert len(results) == 1
    assert results[0]["name"] == "MPU6050"


def test_search_component_by_category(
    component_repository,
    sample_component,
):
    """Verify searching by category."""

    component_repository.add_component(sample_component)

    results = component_repository.search_components(
        "Sensor"
    )

    assert len(results) == 1


def test_search_component_case_insensitive(
    component_repository,
    sample_component,
):
    """Verify that ordinary ASCII searches ignore case."""

    component_repository.add_component(sample_component)

    results = component_repository.search_components(
        "mpu6050"
    )

    assert len(results) == 1


def test_search_component_no_matches(
    component_repository,
    sample_component,
):
    """Verify that unmatched searches return an empty list."""

    component_repository.add_component(sample_component)

    results = component_repository.search_components(
        "Nonexistent Part"
    )

    assert results == []


def test_empty_search_returns_all(
    component_repository,
    sample_component,
):
    """Verify that an empty search returns all components."""

    component_repository.add_component(sample_component)

    results = component_repository.search_components("")

    assert len(results) == 1


# ============================================================
# COUNT OPERATIONS
# ============================================================

def test_component_count(
    component_repository,
    sample_component,
):
    """Verify component record counting."""

    assert component_repository.get_component_count() == 0

    component_repository.add_component(sample_component)

    assert component_repository.get_component_count() == 1


# ============================================================
# VALIDATION
# ============================================================

@pytest.mark.parametrize(
    "invalid_name",
    ["", "   ", None],
)
def test_invalid_component_name(
    component_repository,
    sample_component,
    invalid_name,
):
    """Verify that empty component names are rejected."""

    component = sample_component.copy()
    component["name"] = invalid_name

    with pytest.raises(ValueError):
        component_repository.add_component(component)


def test_negative_quantity(
    component_repository,
    sample_component,
):
    """Verify that negative quantities are rejected."""

    component = sample_component.copy()
    component["quantity"] = -5

    with pytest.raises(ValueError):
        component_repository.add_component(component)


def test_invalid_quantity_type(
    component_repository,
    sample_component,
):
    """Verify that invalid quantity values are rejected."""

    component = sample_component.copy()
    component["quantity"] = "invalid"

    with pytest.raises(ValueError):
        component_repository.add_component(component)


def test_missing_category(
    component_repository,
    sample_component,
):
    """Verify that component categories are required."""

    component = sample_component.copy()
    component["category"] = ""

    with pytest.raises(ValueError):
        component_repository.add_component(component)


# ============================================================
# DATABASE PERSISTENCE
# ============================================================

def test_component_persistence(
    component_repository,
    test_database,
    sample_component,
):
    """Verify that components persist across repository instances."""

    component_id = component_repository.add_component(
        sample_component
    )

    from database.component_repository import ComponentRepository

    new_repository = ComponentRepository(
        database=test_database
    )

    component = new_repository.get_component(
        component_id
    )

    assert component is not None
    assert component["name"] == "MPU6050"