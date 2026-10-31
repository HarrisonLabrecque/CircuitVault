# CircuitVault
## Software Design Document (SDD)

**Version:** 0.1.0  
**Application:** CircuitVault  
**Application Type:** Desktop Electronics Inventory Management System  
**Programming Language:** Python  
**GUI Framework:** PySide6  
**Database:** SQLite  
**Target Platform:** Windows 11  
**Document Status:** Initial Release Design

---

# 1. Introduction

## 1.1 Purpose

This Software Design Document (SDD) describes the architecture, components, database structure, user interface, and implementation design of CircuitVault version 0.1.0.

The document provides a technical reference for understanding, maintaining, testing, and extending the application.

It complements the Software Requirements Specification (`docs/SRS.md`), which defines the application's functional and non-functional requirements.

## 1.2 Scope

CircuitVault is a Python desktop application designed to manage electronic components, registered hardware devices, sensor measurements, and engineering projects.

Version 0.1.0 includes five primary modules:

1. Dashboard
2. Components
3. Devices
4. Sensors
5. Projects

The application uses PySide6 for its graphical interface and SQLite for persistent local data storage.

The initial version focuses on manually managed data. Automatic network discovery, live sensor acquisition, and remote device communication are reserved for future development.

## 1.3 Design Objectives

CircuitVault is designed to:

- Provide a modular and maintainable codebase.
- Separate user interface logic from database operations.
- Maintain persistent local inventory records.
- Support relationships between components and projects.
- Associate sensor measurements with registered devices.
- Provide a consistent graphical interface.
- Support automated testing.
- Allow future integration with embedded systems and network-connected hardware.

## 1.4 Intended Audience

This document is intended for:

- Software developers
- Application maintainers
- Software testers
- Engineering students
- Contributors to future CircuitVault development

---

# 2. System Architecture

## 2.1 Architectural Overview

CircuitVault follows a modular, layered desktop application architecture.

The application is divided into four primary layers:

| Layer | Responsibility |
|---|---|
| Presentation Layer | PySide6 windows, pages, dialogs, and widgets |
| Data Model Layer | Representing application data |
| Repository Layer | Performing CRUD operations and queries |
| Database Layer | SQLite connections, schema initialization, and transactions |

The separation of these layers reduces coupling and allows individual modules to be tested independently.

## 2.2 High-Level Architecture

```text
+--------------------------------------------------+
|                 CIRCUITVAULT                     |
|                  Main Window                     |
+--------------------------------------------------+
|                                                  |
|  Dashboard   Components   Devices                |
|  Sensors     Projects                             |
|                                                  |
+--------------------------------------------------+
                       |
                       v
+--------------------------------------------------+
|                PRESENTATION LAYER                |
|                                                  |
|  DashboardPage                                   |
|  ComponentsPage                                  |
|  DevicesPage                                     |
|  SensorsPage                                     |
|  ProjectsPage                                    |
|                                                  |
|  Dialogs and Custom Widgets                      |
+--------------------------------------------------+
                       |
                       v
+--------------------------------------------------+
|                 REPOSITORY LAYER                 |
|                                                  |
|  ComponentRepository                             |
|  DeviceRepository                                |
|  SensorRepository                                |
|  ProjectRepository                               |
+--------------------------------------------------+
                       |
                       v
+--------------------------------------------------+
|                  DATABASE LAYER                  |
|                                                  |
|                DatabaseManager                   |
|                                                  |
|                     SQLite                       |
+--------------------------------------------------+
```

The GUI communicates with repositories to retrieve or modify records.

Repositories communicate with the database manager to execute SQL operations.

## 2.3 Architectural Principles

The implementation follows these principles:

**Modularity:** Each major application feature is maintained in a separate module.

**Separation of concerns:** GUI classes handle presentation and user interaction, while repository classes manage database operations.

**Reusability:** Shared database management and GUI widgets can be reused across modules.

**Testability:** Repositories and selected GUI pages support dependency injection, allowing tests to use isolated databases.

**Extensibility:** Future networking and sensor acquisition modules can be added without replacing the existing application architecture.

---

# 3. Project Directory Structure

## 3.1 Directory Organization

The following structure represents the principal modules of CircuitVault v0.1.0.

```text
CircuitVault/
|
|-- main.py
|-- requirements.txt
|-- requirements-lock.txt
|-- pytest.ini
|-- README.md
|-- CHANGELOG.md
|-- LICENSE
|
|-- app/
|   |-- __init__.py
|   |-- main_window.py
|   |
|   |-- pages/
|   |   |-- __init__.py
|   |   |-- dashboard_page.py
|   |   |-- components_page.py
|   |   |-- devices_page.py
|   |   |-- sensors_page.py
|   |   |-- projects_page.py
|   |
|   |-- dialogs/
|   |   |-- __init__.py
|   |   |-- component_dialog.py
|   |   |-- device_dialog.py
|   |   |-- sensor_reading_dialog.py
|   |   |-- project_dialog.py
|   |   |-- project_component_dialog.py
|   |
|   |-- widgets/
|       |-- metric_card.py
|
|-- database/
|   |-- __init__.py
|   |-- database.py
|   |-- component_repository.py
|   |-- device_repository.py
|   |-- sensor_repository.py
|   |-- project_repository.py
|
|-- models/
|   |-- component.py
|   |-- device.py
|   |-- sensor_reading.py
|   |-- project.py
|
|-- network/
|   |-- __init__.py
|   |-- scanner.py
|
|-- sensors/
|   |-- __init__.py
|   |-- sensor_manager.py
|
|-- styles/
|   |-- main.qss
|
|-- data/
|   |-- circuitvault.db
|
|-- docs/
|   |-- SRS.md
|   |-- SDD.md
|   |-- USER_GUIDE.md
|
|-- tests/
    |-- __init__.py
    |-- conftest.py
    |-- test_database.py
    |-- test_component_repository.py
    |-- test_components_page.py
    |-- test_device_repository.py
    |-- test_devices_page.py
    |-- test_sensor_repository.py
    |-- test_sensors_page.py
    |-- test_project_repository.py
    |-- test_projects_page.py
    |-- test_integration.py
```

## 3.2 Directory Responsibilities

| Directory | Responsibility |
|---|---|
| `app/` | Main GUI implementation |
| `app/pages/` | Individual application pages |
| `app/dialogs/` | Data-entry and editing dialogs |
| `app/widgets/` | Reusable GUI components |
| `database/` | Database manager and repositories |
| `models/` | Application data representations |
| `network/` | Future network discovery functionality |
| `sensors/` | Future automated sensor collection |
| `styles/` | Application stylesheet |
| `data/` | Local SQLite database |
| `docs/` | Technical and user documentation |
| `tests/` | Automated test suite |

The `network/` and `sensors/` directories provide a foundation for future functionality and do not imply that automatic device discovery or live sensor acquisition is implemented in v0.1.0.

---

# 4. Application Entry Point

## 4.1 Main Application

**File:** `main.py`

The entry point is responsible for initializing and launching the desktop application.

Its responsibilities include:

- Creating the Qt application instance.
- Initializing the database.
- Loading the application stylesheet.
- Creating the main window.
- Starting the Qt event loop.

## 4.2 Startup Sequence

```text
Application Started
        |
        v
Initialize QApplication
        |
        v
Initialize SQLite Database
        |
        v
Load Application Stylesheet
        |
        v
Create MainWindow
        |
        v
Initialize Application Pages
        |
        v
Display Main Window
        |
        v
Start Qt Event Loop
```

The database must be initialized before pages attempt to retrieve stored records.

---

# 5. Main Window Design

## 5.1 MainWindow

**File:** `app/main_window.py`

**Class:** `MainWindow`

The main window serves as the central container for CircuitVault's user interface.

It is implemented using `QMainWindow`.

## 5.2 Main Window Components

The main window contains:

- Application title
- Sidebar navigation
- Main content area
- Version information
- Five application pages

A `QStackedWidget` manages the currently displayed page.

## 5.3 Navigation Structure

| Index | Page |
|---|---|
| 0 | Dashboard |
| 1 | Components |
| 2 | Devices |
| 3 | Sensors |
| 4 | Projects |

The navigation system uses buttons to change the active page.

## 5.4 Navigation Method

**Method:** `navigate_to(index)`

Responsibilities:

1. Validate the requested page index.
2. Change the active page.
3. Update the active sidebar button.
4. Refresh the selected page's data.

## 5.5 Page Refresh Methods

| Page | Refresh Method |
|---|---|
| Dashboard | `refresh_metrics()` |
| Components | `refresh_components()` |
| Devices | `refresh_devices()` |
| Sensors | `refresh_readings()` |
| Projects | `refresh_projects()` |

Refreshing pages during navigation helps ensure that changes made in one module are reflected in related modules.

---

# 6. Dashboard Module Design

## 6.1 Overview

**File:** `app/pages/dashboard_page.py`

**Class:** `DashboardPage`

The Dashboard provides a summary of the application's stored information.

## 6.2 Dashboard Statistics

The Dashboard displays four metrics:

| Metric | Description |
|---|---|
| Total Components | Number of component records |
| Known Devices | Number of registered devices |
| Online Devices | Number of devices marked Online |
| Sensor Readings | Number of stored measurements |

## 6.3 Metric Cards

**File:** `app/widgets/metric_card.py`

Metric cards are reusable PySide6 widgets designed to display numerical statistics.

Each card represents a single metric.

## 6.4 Data Retrieval

Dashboard statistics are retrieved through:

`DatabaseManager.get_dashboard_statistics()`

The method executes SQL queries against the relevant database tables.

## 6.5 Refresh Behavior

The Dashboard refreshes its metrics when the user navigates to the page.

This ensures that newly created or deleted records are reflected in the displayed statistics.

---

# 7. Components Module Design

## 7.1 Overview

**File:** `app/pages/components_page.py`

**Class:** `ComponentsPage`

The Components module provides inventory management functionality.

## 7.2 Component Data Model

**File:** `models/component.py`

The component data model represents electronic inventory information.

The database stores the following fields:

| Field | Data Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| name | TEXT | Component name |
| category | TEXT | Component category |
| manufacturer | TEXT | Manufacturer |
| part_number | TEXT | Part number |
| quantity | INTEGER | Inventory quantity |
| storage_location | TEXT | Storage location |
| datasheet | TEXT | Datasheet reference |
| notes | TEXT | Additional notes |
| created_at | TEXT | Creation timestamp |

## 7.3 Component Repository

**File:** `database/component_repository.py`

**Class:** `ComponentRepository`

The repository manages component records.

Principal operations include:

- Adding components
- Retrieving components
- Updating components
- Deleting components
- Searching components

## 7.4 Component Dialog

**File:** `app/dialogs/component_dialog.py`

The dialog provides input fields for component information.

It is used for creating and editing inventory records.

## 7.5 Component Workflow

```text
User Opens Components Page
             |
             v
     Component Table
             |
             v
   Add / Edit / Delete
             |
             v
      Component Dialog
             |
             v
    Validate User Input
             |
             v
    ComponentRepository
             |
             v
       SQLite Database
             |
             v
     Refresh Components
```

## 7.6 Quantity Management

Component inventory quantities must be non-negative integers.

Component assignments to projects do not automatically decrease inventory quantities in v0.1.0.

---

# 8. Devices Module Design

## 8.1 Overview

**File:** `app/pages/devices_page.py`

**Class:** `DevicesPage`

The Devices module manages registered electronic and computing devices.

## 8.2 Device Data Model

**File:** `models/device.py`

The device database record contains:

| Field | Data Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| name | TEXT | Device name |
| device_type | TEXT | Device classification |
| hostname | TEXT | Network hostname |
| ip_address | TEXT | IP address |
| mac_address | TEXT | MAC address |
| status | TEXT | Online or Offline |
| last_seen | TEXT | Last recorded activity |
| created_at | TEXT | Creation timestamp |

## 8.3 Device Repository

**File:** `database/device_repository.py`

**Class:** `DeviceRepository`

The repository provides database operations for registered devices.

## 8.4 Device Dialog

**File:** `app/dialogs/device_dialog.py`

The device dialog allows users to enter or update device information.

## 8.5 Device Status

Devices support the following statuses:

- Online
- Offline

Version 0.1.0 stores the recorded status in SQLite.

Automatic status detection is reserved for future releases.

## 8.6 Device Relationships

A device may have multiple associated sensor readings.

Deleting a device removes its associated sensor readings through a database foreign-key relationship.

---

# 9. Sensors Module Design

## 9.1 Overview

**File:** `app/pages/sensors_page.py`

**Class:** `SensorsPage`

The Sensors module manages manually recorded sensor measurements.

## 9.2 Sensor Reading Data Model

**File:** `models/sensor_reading.py`

The sensor reading database record contains:

| Field | Data Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| device_id | INTEGER | Associated device |
| sensor_name | TEXT | Sensor name |
| metric | TEXT | Measurement type |
| value | REAL | Numerical measurement |
| unit | TEXT | Measurement unit |
| timestamp | TEXT | Measurement timestamp |

## 9.3 Sensor Repository

**File:** `database/sensor_repository.py`

**Class:** `SensorRepository`

The repository provides operations for:

- Adding sensor readings
- Retrieving sensor readings
- Updating sensor readings
- Deleting sensor readings
- Searching sensor readings

## 9.4 Sensor Reading Dialog

**File:** `app/dialogs/sensor_reading_dialog.py`

The dialog provides fields for selecting a registered device and entering measurement information.

## 9.5 Sensor Data Workflow

```text
User Opens Sensors Page
             |
             v
     Add Sensor Reading
             |
             v
    Select Registered Device
             |
             v
     Enter Measurement
             |
             v
       Validate Data
             |
             v
      SensorRepository
             |
             v
       SQLite Database
             |
             v
    Refresh Sensor Table
```

## 9.6 Sensor Data Collection

Sensor measurements are entered manually in version 0.1.0.

Future versions may integrate automatic acquisition from embedded devices.

---

# 10. Projects Module Design

## 10.1 Overview

**File:** `app/pages/projects_page.py`

**Class:** `ProjectsPage`

The Projects module manages engineering projects and their associated inventory components.

## 10.2 Project Data Model

**File:** `models/project.py`

The project database record contains:

| Field | Data Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| name | TEXT | Project name |
| description | TEXT | Project description |
| status | TEXT | Project status |
| created_at | TEXT | Creation timestamp |

## 10.3 Project Statuses

Supported statuses are:

- Planning
- Active
- On Hold
- Completed

## 10.4 Project Repository

**File:** `database/project_repository.py`

**Class:** `ProjectRepository`

The repository manages:

- Project creation
- Project retrieval
- Project updates
- Project deletion
- Project searching
- Component assignments
- Assignment updates
- Assignment removal

## 10.5 Project Dialog

**File:** `app/dialogs/project_dialog.py`

**Class:** `ProjectDialog`

The dialog contains:

- Project name input
- Project status selector
- Project description input
- Save and Cancel buttons

Project names are required.

## 10.6 Component Assignment Dialog

**File:** `app/dialogs/project_component_dialog.py`

**Class:** `ProjectComponentDialog`

The dialog allows users to:

1. Select an existing inventory component.
2. Specify an assignment quantity.
3. Save the association to the project.

## 10.7 Projects Page Tables

The Projects page contains two tables.

### Projects Table

| Column | Description |
|---|---|
| ID | Project identifier |
| Name | Project name |
| Status | Project status |
| Description | Project description |
| Component Types | Number of assigned component types |
| Assigned Quantity | Total assigned component quantity |

### Assigned Components Table

| Column | Description |
|---|---|
| Component ID | Inventory component identifier |
| Name | Component name |
| Category | Component category |
| Inventory Quantity | Current inventory quantity |
| Assigned Quantity | Quantity associated with the project |

## 10.8 Component Assignment Workflow

```text
User Selects Project
         |
         v
Click Assign Component
         |
         v
ProjectComponentDialog
         |
         v
Select Inventory Component
         |
         v
Enter Assignment Quantity
         |
         v
Validate Assignment
         |
         v
ProjectRepository
         |
         v
project_components Table
         |
         v
Refresh Projects Page
```

## 10.9 Assignment Behavior

Each project-component pair is unique.

If the user assigns the same component to the same project again, the stored assignment quantity is updated.

Component assignments do not automatically change inventory quantities.

## 10.10 Selection Management

The Projects page uses Qt's selection model to identify selected records.

The methods:

- `get_selected_project_id()`
- `get_selected_component_id()`

retrieve IDs from selected rows.

This design prevents stale selections from remaining active after the user clears a table selection.

Buttons requiring a selected record are disabled when no valid selection exists.

---

# 11. Database Design

## 11.1 Overview

**File:** `database/database.py`

**Class:** `DatabaseManager`

CircuitVault uses SQLite for local persistent storage.

The database contains five application tables:

1. `components`
2. `devices`
3. `sensor_readings`
4. `projects`
5. `project_components`

## 11.2 Database Manager Responsibilities

`DatabaseManager` is responsible for:

- Establishing SQLite connections
- Initializing the database schema
- Managing transactions
- Enabling foreign-key constraints
- Providing dashboard statistics

## 11.3 Connection Management

Database connections are managed using a context manager.

The database manager commits successful transactions and rolls back transactions when exceptions occur.

SQLite foreign-key enforcement is enabled for database connections.

## 11.4 Components Table

```sql
CREATE TABLE components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    manufacturer TEXT,
    part_number TEXT,
    quantity INTEGER NOT NULL DEFAULT 0
        CHECK (quantity >= 0),
    storage_location TEXT,
    datasheet TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

## 11.5 Devices Table

The `devices` table stores registered device information.

Its principal fields include:

- `id`
- `name`
- `device_type`
- `hostname`
- `ip_address`
- `mac_address`
- `status`
- `last_seen`
- `created_at`

## 11.6 Sensor Readings Table

The `sensor_readings` table contains a foreign key referencing the `devices` table.

The relationship uses:

```sql
FOREIGN KEY (device_id)
REFERENCES devices(id)
ON DELETE CASCADE
```

This ensures that deleting a registered device also removes its associated sensor readings.

## 11.7 Projects Table

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'Active',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

The repository layer validates project status values before insertion or modification.

## 11.8 Project Components Table

```sql
CREATE TABLE project_components (
    project_id INTEGER NOT NULL,
    component_id INTEGER NOT NULL,
    quantity_used INTEGER NOT NULL DEFAULT 1
        CHECK (quantity_used > 0),

    PRIMARY KEY (project_id, component_id),

    FOREIGN KEY (project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE,

    FOREIGN KEY (component_id)
        REFERENCES components(id)
        ON DELETE CASCADE
);
```

This table implements a many-to-many relationship between projects and inventory components.

## 11.9 Database Relationships

```text
+-------------------+
|      devices      |
+-------------------+
| id (PK)           |
| name              |
| device_type       |
| status            |
+-------------------+
          |
          | 1
          |
          | Many
          v
+-------------------+
|  sensor_readings  |
+-------------------+
| id (PK)           |
| device_id (FK)    |
| sensor_name       |
| metric            |
| value             |
| unit              |
+-------------------+


+-------------------+
|      projects     |
+-------------------+
| id (PK)           |
| name              |
| description       |
| status            |
+-------------------+
          |
          | 1
          |
          | Many
          v
+------------------------+
|   project_components   |
+------------------------+
| project_id (PK, FK)    |
| component_id (PK, FK)  |
| quantity_used          |
+------------------------+
          ^
          |
          | Many
          |
          | 1
+-------------------+
|     components    |
+-------------------+
| id (PK)           |
| name              |
| category          |
| quantity          |
+-------------------+
```

## 11.10 Data Integrity

Data integrity is maintained through:

- Primary keys
- Foreign keys
- Database constraints
- Repository validation
- SQL transactions
- Parameterized SQL statements

---

# 12. Data Flow Design

## 12.1 General CRUD Workflow

```text
User Action
    |
    v
PySide6 Page
    |
    v
Dialog (if required)
    |
    v
Input Validation
    |
    v
Repository Method
    |
    v
DatabaseManager
    |
    v
SQLite Database
    |
    v
Repository Result
    |
    v
Refresh GUI
```

## 12.2 Database Read Workflow

```text
Page Refresh
     |
     v
Repository Query
     |
     v
SQLite SELECT
     |
     v
Database Records
     |
     v
Python Dictionaries
     |
     v
QTableWidget
```

## 12.3 Error Handling Workflow

```text
User Action
     |
     v
Database Operation
     |
     +---- Success ----> Refresh Interface
     |
     +---- Failure ----> Catch Exception
                              |
                              v
                       QMessageBox
                              |
                              v
                       Display Error
```

The application handles relevant database errors and validation errors in its GUI operations.

---

# 13. User Interface Design

## 13.1 GUI Framework

CircuitVault uses PySide6, the Python bindings for Qt.

The interface uses standard Qt widgets, including:

- `QMainWindow`
- `QWidget`
- `QStackedWidget`
- `QPushButton`
- `QLabel`
- `QLineEdit`
- `QTableWidget`
- `QDialog`
- `QComboBox`
- `QSpinBox`
- `QTextEdit`
- `QMessageBox`

## 13.2 Main Layout

The main window uses a sidebar and content-area layout.

```text
+-------------------------------------------------------------+
|                        CircuitVault                         |
+----------------+--------------------------------------------+
|                |                                            |
| Dashboard      |                                            |
|                |                                            |
| Components     |             Active Page                    |
|                |                                            |
| Devices        |                                            |
|                |                                            |
| Sensors        |                                            |
|                |                                            |
| Projects       |                                            |
|                |                                            |
|                |                                            |
| CircuitVault   |                                            |
| v0.1.0         |                                            |
+----------------+--------------------------------------------+
```

## 13.3 Styling

**File:** `styles/main.qss`

CircuitVault uses a Qt stylesheet to define its visual appearance.

The stylesheet provides a centralized location for managing widget styling.

## 13.4 Table Behavior

Data tables use row-based selection.

Tables are configured to prevent direct cell editing.

Record modifications are performed through dedicated dialogs.

## 13.5 Dialog Behavior

Dialogs provide structured forms for entering and modifying records.

Validation occurs before valid records are submitted to repositories.

---

# 14. Error Handling and Validation

## 14.1 Validation Strategy

Validation is performed at appropriate application layers.

The GUI provides user-facing validation feedback.

Repository classes validate business rules.

SQLite enforces database-level constraints.

## 14.2 Component Validation

Component validation includes:

- Required name
- Required category
- Non-negative quantity

## 14.3 Project Validation

Project validation includes:

- Required project name
- Supported project status
- Positive assignment quantity

## 14.4 Database Errors

Database errors are handled using Python's `sqlite3` exception classes.

The GUI uses `QMessageBox` to display relevant error messages.

## 14.5 Transaction Management

Database operations use transaction management to maintain consistency.

When a transaction fails, its uncommitted changes are rolled back.

---

# 15. Testing Architecture

## 15.1 Overview

CircuitVault uses automated tests to verify database operations, GUI behavior, and integration between modules.

## 15.2 Testing Frameworks

| Tool | Purpose |
|---|---|
| pytest | Automated Python testing |
| pytest-qt | PySide6 GUI testing |
| SQLite | Isolated test databases |
| pytest fixtures | Shared test setup |

## 15.3 Repository Tests

Repository tests cover:

- CRUD operations
- Searching
- Validation
- Foreign-key relationships
- Persistence
- Assignment management

## 15.4 GUI Tests

GUI tests cover:

- Page initialization
- Table population
- Dialog validation
- Button states
- Record selection
- User-triggered CRUD operations

## 15.5 Integration Tests

**File:** `tests/test_integration.py`

Integration tests cover:

- Main window navigation
- Page refresh behavior
- Shared database access
- Dashboard statistics
- Component-project integration
- Device-sensor integration
- Database persistence
- Transaction rollback

Navigation tests use isolated page substitutes, while database integration tests use the actual repository classes.

## 15.6 Test Database Isolation

Automated database tests use temporary SQLite databases.

This prevents tests from modifying the application's normal inventory database.

## 15.7 Test Execution

Run the complete test suite using:

```powershell
python -m pytest -v
```

Run integration tests using:

```powershell
python -m pytest tests/test_integration.py -v
```

---

# 16. Security Design

## 16.1 Local Data Storage

CircuitVault stores application records locally using SQLite.

Version 0.1.0 does not require a cloud account or external database server.

## 16.2 SQL Injection Prevention

Repository methods use parameterized SQL statements for database queries involving user-supplied values.

## 16.3 Input Validation

The application validates applicable user input before committing records.

SQLite constraints provide an additional layer of protection against invalid data.

## 16.4 Filesystem Permissions

Database file access is controlled by the operating system's filesystem permissions.

## 16.5 Authentication

User authentication is not implemented in version 0.1.0.

The application is intended primarily for local personal use.

---

# 17. Performance Considerations

## 17.1 Local Database

SQLite provides local database access without requiring a separate database server.

## 17.2 Query Design

Repositories use SQL queries to retrieve and modify records.

Project component totals are calculated using database aggregation.

## 17.3 GUI Updates

Application pages refresh their displayed information when necessary.

## 17.4 Future Optimization

Future versions may introduce:

- Database indexes
- Pagination for large inventories
- Background worker threads
- Asynchronous device communication
- Cached statistics

These optimizations are not required for the initial release.

---

# 18. Future Architecture Extensions

## 18.1 Network Discovery

**Directory:** `network/`

Future network functionality may include:

- Local device scanning
- Device discovery
- Network availability monitoring
- Device status updates

## 18.2 Automated Sensor Collection

**Directory:** `sensors/`

Future sensor functionality may include:

- Serial communication
- Network sensor communication
- Periodic sensor polling
- Automated database recording

## 18.3 Data Visualization

Potential enhancements include:

- Sensor measurement charts
- Historical measurement analysis
- Inventory statistics
- Device monitoring dashboards

## 18.4 Inventory Enhancements

Future versions may support:

- Low-stock alerts
- Inventory import and export
- Component usage history
- Project-based inventory allocation
- Advanced inventory reports

## 18.5 Architectural Compatibility

Future features should preserve the separation between:

- GUI components
- Data models
- Repository classes
- Database management
- Hardware communication modules

---

# 19. Design Verification

The implementation should be evaluated against the Software Requirements Specification.

## 19.1 Verification Matrix

| Requirement Area | Design Component | Verification |
|---|---|---|
| Dashboard | DashboardPage | GUI and integration tests |
| Components | ComponentsPage, ComponentRepository | Repository and GUI tests |
| Devices | DevicesPage, DeviceRepository | Repository and GUI tests |
| Sensors | SensorsPage, SensorRepository | Repository and GUI tests |
| Projects | ProjectsPage, ProjectRepository | Repository and GUI tests |
| Database | DatabaseManager | Database tests |
| Navigation | MainWindow | Integration tests |
| Data persistence | SQLite repositories | Repository and integration tests |
| Referential integrity | SQLite foreign keys | Database and integration tests |

## 19.2 Release Verification

Before release, the following activities should be completed:

1. Execute the complete automated test suite.
2. Verify all five pages manually.
3. Confirm database persistence after application restart.
4. Review application error handling.
5. Verify documentation accuracy.
6. Package the Windows executable.
7. Test the packaged application.

---

# 20. Release Information

| Item | Description |
|---|---|
| Application | CircuitVault |
| Version | 0.1.0 |
| Release Type | Initial Development Release |
| Target Operating System | Windows 11 |
| Programming Language | Python |
| GUI Framework | PySide6 |
| Database | SQLite |
| Testing | pytest and pytest-qt |
| Architecture | Modular layered desktop application |
| Release Status | Preparation |

CircuitVault v0.1.0 establishes the foundation for an extensible electronics inventory management application.

Its architecture supports future development involving embedded devices, network discovery, automated sensor acquisition, and engineering project management.

---

# 21. Document Revision History

| Version | Description |
|---|---|
| 0.1.0 | Initial Software Design Document covering application architecture, database schema, GUI modules, repositories, integration, and testing |

---

**End of Document**

CircuitVault — Software Design Document  
Version 0.1.0