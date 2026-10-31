# CircuitVault
## Software Requirements Specification (SRS)

**Version:** 0.1.0  
**Application:** CircuitVault  
**Application Type:** Desktop Electronics Inventory Management System  
**Programming Language:** Python  
**GUI Framework:** PySide6  
**Database:** SQLite  
**Target Platform:** Windows 11  
**Document Status:** Initial Release Specification

---

# 1. Introduction

## 1.1 Purpose

This Software Requirements Specification (SRS) defines the functional and non-functional requirements for CircuitVault version 0.1.0.

CircuitVault is a desktop application designed to organize and manage electronic components, registered hardware devices, sensor readings, and electronics projects.

The application provides a centralized interface for maintaining a personal electronics inventory and associating components with engineering projects.

This document establishes the requirements implemented in version 0.1.0 and identifies potential enhancements for future releases.

## 1.2 Scope

CircuitVault v0.1.0 provides five primary application modules:

1. Dashboard
2. Components
3. Devices
4. Sensors
5. Projects

The application uses a local SQLite database for persistent data storage and PySide6 for its graphical interface.

Users can manage electronic components, maintain device records, record sensor measurements, create projects, and associate inventory components with those projects.

Version 0.1.0 focuses on local data management.

Automatic network discovery, live sensor monitoring, and remote device communication are outside the scope of this release.

## 1.3 Intended Audience

This document is intended for:

- Software developers
- Electronics hobbyists
- Embedded systems developers
- Robotics enthusiasts
- Engineering students
- Application maintainers

## 1.4 Definitions and Acronyms

| Term | Definition |
|---|---|
| SRS | Software Requirements Specification |
| GUI | Graphical User Interface |
| CRUD | Create, Read, Update, Delete |
| SQLite | Embedded relational database |
| PySide6 | Python bindings for the Qt framework |
| Repository | Software component responsible for database operations |
| Component | Electronic part stored in inventory |
| Device | Registered electronic or computing device |
| Sensor Reading | Recorded measurement associated with a device |
| Project | Engineering activity that may use inventory components |
| Foreign Key | Database constraint linking related records |

---

# 2. Overall Description

## 2.1 Product Perspective

CircuitVault is a standalone desktop application.

The application follows a modular architecture that separates:

- Graphical interface components
- Application data models
- Database management
- Repository operations
- Future networking functionality
- Future sensor integration functionality

The application operates locally without requiring an internet connection for its core features.

## 2.2 Product Functions

CircuitVault v0.1.0 supports the following functions.

### Dashboard

- Display the total number of component records.
- Display the number of registered devices.
- Display the number of devices marked online.
- Display the number of stored sensor readings.
- Refresh displayed statistics.

### Components

- Add electronic components.
- View stored components.
- Edit component information.
- Delete components.
- Search component records.
- Track component quantities.
- Store manufacturer information, datasheet references, and notes.

### Devices

- Register electronic devices.
- View registered devices.
- Edit device information.
- Delete devices.
- Search device records.
- Store network identification information.
- Track manually recorded device status.

### Sensors

- Add sensor readings.
- View recorded measurements.
- Edit sensor readings.
- Delete sensor readings.
- Search recorded measurements.
- Associate sensor readings with registered devices.

### Projects

- Create engineering projects.
- View stored projects.
- Edit project information.
- Delete projects.
- Search projects.
- Track project status.
- Assign inventory components to projects.
- Specify quantities assigned to projects.
- Remove component assignments.

## 2.3 User Characteristics

CircuitVault is intended for users with basic computer skills and an interest in electronics or engineering.

Users should be familiar with basic concepts such as electronic components, device names, and sensor measurements.

Programming experience is not required for normal GUI operation.

## 2.4 Operating Environment

### Software Environment

| Requirement | Specification |
|---|---|
| Operating System | Windows 11 |
| Programming Language | Python 3 |
| GUI Framework | PySide6 |
| Database | SQLite |
| Testing Framework | pytest |
| GUI Testing | pytest-qt |
| Development Environment | Python virtual environment |

### Hardware Environment

CircuitVault is designed to run on a standard Windows desktop or laptop.

The initial release does not require specialized electronics hardware.

## 2.5 Design Constraints

CircuitVault v0.1.0 must:

- Use Python as its primary programming language.
- Use PySide6 for the desktop interface.
- Use SQLite for persistent local storage.
- Separate database operations from GUI logic.
- Support operation without an active internet connection.
- Maintain referential integrity between related database records.
- Prevent invalid component quantities.
- Prevent invalid project assignment quantities.

## 2.6 Assumptions and Dependencies

The application assumes:

- The user has permission to access the application database.
- The local filesystem is available for persistent storage.
- Required Python dependencies are installed when running from source.
- Users manually enter component, device, and sensor information.
- The application is primarily used by one local user.

---

# 3. Functional Requirements

## 3.1 Dashboard Requirements

### FR-DASH-001: Dashboard Display

The system shall provide a Dashboard page accessible through the main navigation interface.

### FR-DASH-002: Component Statistics

The system shall display the total number of component records stored in the database.

### FR-DASH-003: Device Statistics

The system shall display the total number of registered devices.

### FR-DASH-004: Online Device Statistics

The system shall display the number of devices whose recorded status is Online.

### FR-DASH-005: Sensor Statistics

The system shall display the total number of stored sensor readings.

### FR-DASH-006: Dashboard Refresh

The system shall retrieve updated statistics when the Dashboard page is refreshed.

---

## 3.2 Component Management Requirements

### FR-COMP-001: Add Component

The system shall allow users to create a component record.

A component record shall support the following fields:

| Field | Description |
|---|---|
| ID | Unique component identifier |
| Name | Component name |
| Category | Component classification |
| Manufacturer | Component manufacturer |
| Part Number | Manufacturer or module part number |
| Quantity | Number of units in inventory |
| Storage Location | Physical storage location |
| Datasheet | Datasheet reference |
| Notes | Additional information |
| Created At | Record creation timestamp |

### FR-COMP-002: Required Fields

The system shall require a component name and category.

### FR-COMP-003: Quantity Validation

The system shall prevent negative inventory quantities.

### FR-COMP-004: View Components

The system shall display stored components in a table.

### FR-COMP-005: Edit Component

The system shall allow users to modify existing component information.

### FR-COMP-006: Delete Component

The system shall allow users to remove component records.

### FR-COMP-007: Search Components

The system shall provide a search interface for locating component records.

### FR-COMP-008: Component Persistence

The system shall preserve component records between application sessions.

---

## 3.3 Device Management Requirements

### FR-DEV-001: Register Device

The system shall allow users to register an electronic or computing device.

Supported device information shall include:

| Field | Description |
|---|---|
| ID | Unique device identifier |
| Name | Device name |
| Device Type | Device classification |
| Hostname | Network hostname |
| IP Address | Network IP address |
| MAC Address | Network hardware address |
| Status | Recorded device status |
| Last Seen | Last recorded activity timestamp |
| Created At | Record creation timestamp |

### FR-DEV-002: View Devices

The system shall display registered devices in a table.

### FR-DEV-003: Edit Device

The system shall allow users to modify registered device information.

### FR-DEV-004: Delete Device

The system shall allow users to delete device records.

### FR-DEV-005: Search Devices

The system shall support searching registered devices.

### FR-DEV-006: Device Status

The system shall support Online and Offline device statuses.

### FR-DEV-007: Device Persistence

The system shall preserve registered device information between application sessions.

---

## 3.4 Sensor Management Requirements

### FR-SENS-001: Record Sensor Measurement

The system shall allow users to create sensor reading records.

A sensor reading shall support:

| Field | Description |
|---|---|
| ID | Unique reading identifier |
| Device ID | Associated registered device |
| Sensor Name | Name of the sensor |
| Metric | Measurement type |
| Value | Recorded numerical value |
| Unit | Measurement unit |
| Timestamp | Measurement timestamp |

### FR-SENS-002: Device Association

Each sensor reading shall reference a registered device.

### FR-SENS-003: View Sensor Readings

The system shall display stored sensor readings in a table.

### FR-SENS-004: Edit Sensor Reading

The system shall allow users to update recorded measurements.

### FR-SENS-005: Delete Sensor Reading

The system shall allow users to delete stored measurements.

### FR-SENS-006: Search Sensor Readings

The system shall provide a search function for sensor records.

### FR-SENS-007: Sensor Persistence

The system shall preserve sensor readings between application sessions.

### FR-SENS-008: Device Deletion Behavior

Deleting a device shall remove sensor readings associated with that device.

---

## 3.5 Project Management Requirements

### FR-PROJ-001: Create Project

The system shall allow users to create engineering projects.

A project shall support:

| Field | Description |
|---|---|
| ID | Unique project identifier |
| Name | Project name |
| Description | Project description |
| Status | Current project status |
| Created At | Record creation timestamp |

### FR-PROJ-002: Required Project Name

The system shall require a non-empty project name.

### FR-PROJ-003: Project Status

The system shall support the following statuses:

- Planning
- Active
- On Hold
- Completed

### FR-PROJ-004: View Projects

The system shall display stored projects in a table.

### FR-PROJ-005: Edit Project

The system shall allow users to update project information.

### FR-PROJ-006: Delete Project

The system shall allow users to delete projects.

### FR-PROJ-007: Search Projects

The system shall allow users to search projects by name, description, or status.

### FR-PROJ-008: Assign Component

The system shall allow users to associate an inventory component with a project.

### FR-PROJ-009: Assignment Quantity

The system shall allow users to specify a positive integer quantity for a component assignment.

### FR-PROJ-010: Update Assignment

Assigning an already-associated component to the same project shall update its recorded assignment quantity.

### FR-PROJ-011: Remove Assignment

The system shall allow users to remove a component assignment.

### FR-PROJ-012: Inventory Preservation

Creating, updating, or removing a project-component assignment shall not automatically change the component's inventory quantity.

### FR-PROJ-013: Project Deletion Behavior

Deleting a project shall remove its component assignments without deleting the associated inventory components.

### FR-PROJ-014: Component Deletion Behavior

Deleting an inventory component shall remove its associated project assignments.

### FR-PROJ-015: Project Statistics

The Projects page shall display the number of distinct component types assigned to each project and the total assigned quantity.

---

# 4. External Interface Requirements

## 4.1 User Interface

CircuitVault shall provide a graphical desktop interface built using PySide6.

The main application window shall contain:

- Sidebar navigation
- Main content area
- Dashboard page
- Components page
- Devices page
- Sensors page
- Projects page

## 4.2 Navigation

The system shall allow users to navigate between all five application pages.

The active navigation item shall be visually distinguishable from inactive items.

## 4.3 Dialog Interfaces

The application shall use dialog windows for creating and editing records.

Dialogs shall provide appropriate input fields and Save and Cancel actions.

Invalid input shall be rejected with an appropriate user-facing message.

## 4.4 Database Interface

The application shall communicate with a local SQLite database through repository classes.

The GUI shall not require direct SQL statements to perform routine operations.

## 4.5 Network Interface

Automatic network communication is not required for v0.1.0.

Device hostnames, IP addresses, and MAC addresses are stored as user-managed records.

---

# 5. Non-Functional Requirements

## 5.1 Usability

### NFR-USE-001

The application shall provide clearly labeled navigation controls.

### NFR-USE-002

The application shall use tables to display stored records.

### NFR-USE-003

The application shall provide appropriate feedback when database operations fail.

### NFR-USE-004

Actions requiring a selected record shall be disabled when no applicable record is selected.

### NFR-USE-005

The application shall request confirmation before destructive operations where implemented.

## 5.2 Reliability

### NFR-REL-001

The application shall use SQLite transactions to maintain database consistency.

### NFR-REL-002

The application shall enforce foreign-key relationships between associated records.

### NFR-REL-003

The application shall preserve committed data between application sessions.

### NFR-REL-004

Failed database transactions shall be rolled back.

## 5.3 Maintainability

### NFR-MAIN-001

The application shall use a modular directory structure.

### NFR-MAIN-002

Database operations shall be separated into repository classes.

### NFR-MAIN-003

GUI pages shall be maintained as separate Python modules.

### NFR-MAIN-004

The project shall maintain automated tests for core functionality.

### NFR-MAIN-005

The project shall maintain versioned documentation.

## 5.4 Performance

### NFR-PERF-001

The application shall support routine inventory operations on a standard Windows computer.

### NFR-PERF-002

Database queries shall be performed locally.

### NFR-PERF-003

The application shall avoid unnecessary network dependencies for core operations.

Specific performance benchmarks are not established for v0.1.0.

## 5.5 Security

### NFR-SEC-001

The application shall use parameterized SQL statements for user-supplied database values.

### NFR-SEC-002

The application shall validate required input fields before storing records.

### NFR-SEC-003

The application shall not require external account credentials for local inventory management.

### NFR-SEC-004

Database access shall be subject to the operating system's filesystem permissions.

## 5.6 Portability

CircuitVault v0.1.0 targets Windows 11.

The use of Python, PySide6, and SQLite provides a foundation for potential cross-platform support.

Other operating systems are not formally supported in this release.

---

# 6. Database Requirements

## 6.1 Database Overview

CircuitVault shall use SQLite for persistent local storage.

The database shall contain the following primary tables:

| Table | Purpose |
|---|---|
| components | Electronic component inventory |
| devices | Registered hardware devices |
| sensor_readings | Recorded sensor measurements |
| projects | Engineering project records |
| project_components | Associations between projects and components |

## 6.2 Database Relationships

The database shall implement the following relationships:

**Devices → Sensor Readings**

One registered device may have multiple sensor readings.

Each sensor reading shall reference one registered device.

**Projects → Project Components**

One project may have multiple component assignments.

**Components → Project Components**

One component may be associated with multiple projects.

The `project_components` table shall implement the many-to-many relationship between projects and components.

## 6.3 Referential Integrity

The database shall enforce foreign-key constraints.

Deleting a device shall delete its associated sensor readings.

Deleting a project shall delete its component assignments.

Deleting a component shall delete its project assignments.

## 6.4 Data Validation

The database and repository layer shall enforce applicable constraints, including:

- Required component names
- Required component categories
- Non-negative inventory quantities
- Required project names
- Valid project statuses
- Positive component assignment quantities
- Valid foreign-key references

---

# 7. Software Architecture

## 7.1 Architectural Overview

CircuitVault follows a modular desktop application architecture.

The major architectural layers are:

1. Presentation Layer
2. Application Data Models
3. Repository Layer
4. Database Layer

## 7.2 Presentation Layer

The presentation layer is implemented using PySide6.

It includes:

- Main application window
- Navigation sidebar
- Dashboard
- Component management interface
- Device management interface
- Sensor management interface
- Project management interface
- Data-entry dialogs

## 7.3 Repository Layer

The repository layer contains classes responsible for retrieving and modifying stored records.

Primary repositories include:

- `ComponentRepository`
- `DeviceRepository`
- `SensorRepository`
- `ProjectRepository`

## 7.4 Database Layer

The database layer is managed through `DatabaseManager`.

Its responsibilities include:

- Establishing SQLite connections
- Initializing database tables
- Managing transactions
- Enabling foreign-key constraints
- Retrieving dashboard statistics

## 7.5 Future Extension Modules

The project structure includes modules intended for future functionality:

- Network discovery
- Device communication
- Automated sensor collection

These modules are not required to provide operational functionality in version 0.1.0.

---

# 8. Verification and Testing Requirements

## 8.1 Testing Framework

CircuitVault shall use:

- pytest for automated testing
- pytest-qt for GUI testing
- Temporary SQLite databases for isolated database tests

## 8.2 Repository Testing

Repository tests shall verify:

- Record creation
- Record retrieval
- Record updates
- Record deletion
- Searching
- Input validation
- Database persistence
- Foreign-key relationships

## 8.3 GUI Testing

GUI tests shall verify:

- Page initialization
- Table population
- Record selection
- Button state management
- Dialog behavior
- CRUD interactions
- Search behavior

## 8.4 Integration Testing

Integration tests shall verify:

- Main window navigation
- Shared database access
- Dashboard statistics
- Component-project relationships
- Device-sensor relationships
- Database persistence
- Transaction rollback

## 8.5 Manual Testing

Manual testing shall verify:

- Application startup
- Navigation between all pages
- Record creation and editing
- Record deletion
- Database persistence after restarting
- Basic error handling
- Windows executable operation when packaging is complete

## 8.6 Acceptance Criteria

CircuitVault v0.1.0 shall be considered ready for release when:

1. All five primary pages are operational.
2. Core CRUD operations function correctly.
3. Database relationships maintain referential integrity.
4. Automated tests pass.
5. Manual integration testing is completed successfully.
6. Required documentation is available.
7. The intended Windows distribution is packaged and verified.

---

# 9. Future Development

The following capabilities are potential enhancements and are not requirements for version 0.1.0.

## 9.1 Network Device Discovery

Future versions may provide:

- Local network scanning
- Raspberry Pi discovery
- ESP32 discovery
- Device availability checks
- Automatic device status updates

## 9.2 Automated Sensor Collection

Future versions may support:

- Sensor data collection from connected devices
- Periodic measurement updates
- Serial communication
- Network-based sensor communication
- Historical sensor data visualization

## 9.3 Advanced Inventory Management

Potential enhancements include:

- Low-stock notifications
- Component usage history
- Inventory import and export
- Advanced filtering
- Inventory allocation and availability calculations

## 9.4 Advanced Project Management

Future versions may introduce:

- Project progress tracking
- Project milestones
- Component usage reports
- Project-specific inventory summaries
- Additional project metadata

## 9.5 Data Visualization

Potential future features include:

- Sensor measurement charts
- Inventory statistics
- Device availability history
- Project component distribution

---

# 10. Release Information

| Item | Description |
|---|---|
| Application | CircuitVault |
| Version | 0.1.0 |
| Release Type | Initial Development Release |
| Platform | Windows 11 |
| Language | Python |
| GUI Framework | PySide6 |
| Database | SQLite |
| Automated Testing | pytest and pytest-qt |
| Release Status | Preparation |

Version 0.1.0 establishes the foundation for CircuitVault as a modular electronics inventory and engineering project management application.

Future versions will expand the application's functionality while preserving the separation between interface, repository, and database components.

---

# 11. Document Revision History

| Version | Description |
|---|---|
| 0.1.0 | Initial Software Requirements Specification covering Dashboard, Components, Devices, Sensors, Projects, database management, and testing |

---

**End of Document**

CircuitVault — Software Requirements Specification  
Version 0.1.0