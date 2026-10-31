# Changelog

All notable changes to **CircuitVault** will be documented in this file.

CircuitVault is a Python/PySide6 desktop application for managing electronic components, registered hardware devices, sensor readings, and engineering projects.

The project follows [Semantic Versioning](https://semver.org/) and uses the *Keep a Changelog* format.

---

## [Unreleased]

### Planned

- Automatic local network device discovery.
- Raspberry Pi, ESP32, and Arduino device detection.
- Automated device availability monitoring.
- Live sensor data acquisition.
- Serial and network-based device communication.
- Sensor measurement visualization.
- Low-stock inventory notifications.
- Inventory import and export.
- Advanced component usage tracking.
- Project progress tracking and reporting.

---

## [0.1.0] - Unreleased

### Added

#### Application Foundation

- Created the initial CircuitVault desktop application using Python and PySide6.
- Implemented a modular project architecture.
- Added the main application window.
- Implemented sidebar navigation between five application pages.
- Added active navigation button styling.
- Implemented page refresh behavior during navigation.
- Added a centralized Qt stylesheet.
- Created reusable GUI widgets and data-entry dialogs.

#### Dashboard

- Added the Dashboard page.
- Implemented metric cards for displaying application statistics.
- Added total component record count.
- Added registered device count.
- Added online device count based on stored device status.
- Added sensor reading count.
- Implemented database-backed metric updates.

#### Component Management

- Added the Components page.
- Implemented component creation, retrieval, updating, and deletion.
- Added searchable component inventory.
- Added component category and manufacturer information.
- Added part number tracking.
- Added inventory quantity management.
- Added storage location information.
- Added datasheet reference storage.
- Added component notes.
- Implemented component input validation.
- Added component management dialogs.

#### Device Management

- Added the Devices page.
- Implemented device registration and management.
- Added device creation, retrieval, updating, and deletion.
- Added searchable device records.
- Added device type information.
- Added hostname storage.
- Added IP address storage.
- Added MAC address storage.
- Added manually maintained Online and Offline statuses.
- Added device management dialogs.

#### Sensor Management

- Added the Sensors page.
- Implemented manual sensor reading management.
- Added sensor reading creation, retrieval, updating, and deletion.
- Added searchable sensor measurement records.
- Added associations between sensor readings and registered devices.
- Added sensor names and measurement types.
- Added numerical measurement values.
- Added measurement units.
- Added measurement timestamps.
- Added sensor reading dialogs.

#### Project Management

- Added the Projects page.
- Implemented project creation, retrieval, updating, and deletion.
- Added searchable project records.
- Added project descriptions.
- Added project status tracking.
- Added support for Planning, Active, On Hold, and Completed statuses.
- Added project management dialogs.
- Implemented component assignments to projects.
- Added assignment quantity tracking.
- Added the ability to update existing component assignments.
- Added component assignment removal.
- Added project component statistics.
- Added an Assigned Components table.
- Preserved inventory quantities when assigning components to projects.

#### Database

- Integrated SQLite for persistent local data storage.
- Added the `DatabaseManager` class.
- Implemented database initialization.
- Added database connection management.
- Added SQL transaction handling.
- Added foreign-key enforcement.
- Created the `components` table.
- Created the `devices` table.
- Created the `sensor_readings` table.
- Created the `projects` table.
- Created the `project_components` table.
- Added database constraints for inventory and assignment quantities.
- Implemented cascading deletion for related records.
- Added repository classes for each primary data module.
- Added database-backed dashboard statistics.

#### Testing

- Added pytest for automated testing.
- Added pytest-qt for GUI testing.
- Created isolated temporary SQLite test databases.
- Added database initialization tests.
- Added component repository tests.
- Added component page tests.
- Added device repository tests.
- Added device page tests.
- Added sensor repository tests.
- Added sensor page tests.
- Added project repository tests.
- Added project page tests.
- Added integration tests.
- Added main window navigation tests.
- Added database persistence tests.
- Added foreign-key relationship tests.
- Added transaction rollback tests.
- Added project-component assignment tests.
- Added device-sensor relationship tests.

#### Documentation

- Added the Software Requirements Specification (`docs/SRS.md`).
- Added the Software Design Document (`docs/SDD.md`).
- Added the User Guide (`docs/USER_GUIDE.md`).
- Added the project README.
- Added the MIT License.
- Added this changelog.
- Documented application architecture and database relationships.
- Documented installation and application usage.

### Fixed

- Corrected project table selection handling to prevent stale selections.
- Updated project and component selection methods to use Qt's selection model.
- Corrected action button states when no project or component is selected.
- Improved consistency between project selection and assigned component display.

### Security

- Used parameterized SQL statements for database operations.
- Added input validation for applicable record fields.
- Enabled SQLite foreign-key constraints.
- Added transaction rollback handling.
- Used local database storage without requiring external account credentials.

### Notes

CircuitVault v0.1.0 establishes the initial application foundation.

The release focuses on local electronics inventory management, manually registered devices, sensor reading storage, and project-component relationships.

Automatic network discovery and live sensor data collection are not included in this version.

Windows executable packaging and final release verification are pending.

---

## Versioning

CircuitVault follows Semantic Versioning:

- **MAJOR:** Significant or incompatible application changes.
- **MINOR:** New functionality and feature additions.
- **PATCH:** Bug fixes and maintenance updates.

Development versions use the `0.x.x` format until the application reaches a stable `1.0.0` release.

---

**CircuitVault — Electronics Inventory and Engineering Project Management**