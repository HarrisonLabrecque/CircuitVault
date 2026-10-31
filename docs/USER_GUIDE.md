# CircuitVault
## User Guide

**Version:** 0.1.0  
**Application:** CircuitVault  
**Application Type:** Electronics Inventory Management System  
**Platform:** Windows 11  
**Programming Language:** Python  
**GUI Framework:** PySide6  
**Database:** SQLite  
**Document Status:** Initial Release

---

# 1. Introduction

## 1.1 About CircuitVault

CircuitVault is a desktop application designed to help users organize electronic components, registered hardware devices, sensor measurements, and engineering projects.

The application provides a centralized interface for managing an electronics inventory and associating components with engineering projects.

CircuitVault uses a local SQLite database to store information between application sessions.

Version 0.1.0 focuses on manual inventory management, device registration, sensor recording, and project organization.

## 1.2 Key Features

CircuitVault v0.1.0 includes five primary modules:

| Module | Description |
|---|---|
| Dashboard | Displays inventory and device statistics |
| Components | Manages electronic component inventory |
| Devices | Manages registered hardware devices |
| Sensors | Stores and manages sensor measurements |
| Projects | Organizes projects and component assignments |

### Additional Features

- Local SQLite database
- Searchable records
- Add, edit, and delete operations
- Component quantity tracking
- Device status tracking
- Project status tracking
- Component-to-project assignments
- Persistent data storage
- Graphical desktop interface

## 1.3 Intended Users

CircuitVault is designed for:

- Electronics hobbyists
- Embedded systems developers
- Robotics enthusiasts
- Engineering students
- Makers
- Software developers working with electronic hardware

No programming knowledge is required to use the graphical interface.

---

# 2. System Requirements

## 2.1 Supported Operating System

CircuitVault v0.1.0 targets Windows 11.

Other operating systems are not formally supported in this release.

## 2.2 Software Requirements

When running CircuitVault from source, the following software is required:

| Software | Purpose |
|---|---|
| Python 3 | Application runtime |
| PySide6 | Graphical interface |
| SQLite | Local database |
| pip | Python package installation |
| Python virtual environment | Dependency isolation |

SQLite support is included with standard Python installations.

## 2.3 Hardware Requirements

CircuitVault is designed to run on a standard Windows desktop or laptop.

No external electronic hardware is required to use version 0.1.0.

## 2.4 Internet Connection

An internet connection is not required for normal operation.

Internet access may be needed to download Python packages during installation.

---

# 3. Installation

## 3.1 Obtain the Application

Obtain the CircuitVault source code from the project's repository or a provided source archive.

Extract the files into a directory on your computer.

Example:

```text
Documents/
└── CircuitVault/
    ├── main.py
    ├── requirements.txt
    ├── app/
    ├── database/
    ├── models/
    ├── styles/
    └── docs/
```

## 3.2 Open PowerShell

Open Windows PowerShell.

Navigate to the CircuitVault directory:

```powershell
cd path\to\CircuitVault
```

Replace `path\to\CircuitVault` with the actual directory path.

## 3.3 Create a Virtual Environment

Create a Python virtual environment:

```powershell
python -m venv .venv
```

This creates an isolated environment for CircuitVault's dependencies.

## 3.4 Activate the Virtual Environment

Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

When activated, PowerShell should display the environment name.

Example:

```text
(.venv) PS C:\Projects\CircuitVault>
```

## 3.5 Install Dependencies

Install the required Python packages:

```powershell
python -m pip install -r requirements.txt
```

Wait for the installation process to finish.

## 3.6 Launch CircuitVault

Start the application:

```powershell
python main.py
```

The CircuitVault main window should appear.

## 3.7 Close CircuitVault

Close the application using the window's standard Close button.

The application will exit, and previously committed database records will remain stored.

---

# 4. Application Overview

## 4.1 Main Window

CircuitVault uses a sidebar-based desktop interface.

The sidebar provides access to the application's five primary pages.

```text
+---------------------------------------------------------+
|                      CircuitVault                       |
+---------------+-----------------------------------------+
|               |                                         |
| Dashboard     |                                         |
|               |                                         |
| Components    |                                         |
|               |            Active Page                  |
| Devices       |                                         |
|               |                                         |
| Sensors       |                                         |
|               |                                         |
| Projects      |                                         |
|               |                                         |
|               |                                         |
| CircuitVault  |                                         |
| v0.1.0        |                                         |
+---------------+-----------------------------------------+
```

## 4.2 Navigation

Click a sidebar button to open the corresponding page.

| Navigation Item | Function |
|---|---|
| Dashboard | View application statistics |
| Components | Manage electronic inventory |
| Devices | Manage hardware device records |
| Sensors | Manage sensor measurements |
| Projects | Manage projects and assigned components |

The selected page is displayed in the main content area.

## 4.3 Common Controls

Several pages use similar controls.

| Control | Function |
|---|---|
| Add | Create a new record |
| Edit | Modify an existing record |
| Delete | Remove a record |
| Search | Filter displayed records |
| Refresh | Reload stored information |
| Save | Confirm changes |
| Cancel | Close a dialog without saving |

Some actions require a record to be selected before they become available.

---

# 5. Dashboard

## 5.1 Overview

The Dashboard provides a summary of the information stored in CircuitVault.

It is the default page displayed when the application starts.

## 5.2 Dashboard Metrics

The Dashboard displays four statistics.

| Metric | Description |
|---|---|
| Total Components | Number of component records |
| Known Devices | Number of registered devices |
| Online Devices | Number of devices marked Online |
| Sensor Readings | Number of stored sensor measurements |

## 5.3 Understanding Component Counts

The Total Components metric counts distinct inventory records.

For example, suppose the inventory contains:

| Component | Quantity |
|---|---:|
| ESP32-S3 | 2 |
| MPU6050 | 3 |
| Raspberry Pi Pico | 4 |

The Dashboard displays:

**Total Components: 3**

It does not display the sum of inventory quantities.

## 5.4 Updating Dashboard Statistics

To view updated statistics:

1. Add, edit, or delete records in another module.
2. Click Dashboard in the sidebar.
3. Review the refreshed statistics.

## 5.5 Online Device Count

The Online Devices metric counts devices whose recorded status is Online.

CircuitVault v0.1.0 does not automatically check whether devices are currently reachable over the network.

---

# 6. Components

## 6.1 Overview

The Components page manages electronic component inventory.

Examples of supported components include:

- Microcontrollers
- Sensors
- Integrated circuits
- Motors
- Development boards
- Electronic modules
- Passive components

## 6.2 Component Information

Each component record supports the following fields:

| Field | Description |
|---|---|
| Name | Component name |
| Category | Component classification |
| Manufacturer | Manufacturer name |
| Part Number | Component part number |
| Quantity | Number of units available |
| Storage Location | Physical storage location |
| Datasheet | Datasheet reference |
| Notes | Additional information |

## 6.3 Adding a Component

To add a component:

1. Open the Components page.
2. Click Add Component.
3. Enter the component information.
4. Verify the quantity.
5. Click Save.

The component will be stored in the SQLite database.

### Example: MPU6050

| Field | Example Value |
|---|---|
| Name | MPU6050 |
| Category | Sensor |
| Manufacturer | InvenSense |
| Part Number | GY-521 |
| Quantity | 3 |
| Storage Location | Drawer A1 |
| Notes | Six-axis accelerometer and gyroscope |

## 6.4 Editing a Component

To edit an existing component:

1. Open the Components page.
2. Select the component in the table.
3. Click Edit Selected.
4. Modify the required fields.
5. Click Save.

The updated information will be stored in the database.

## 6.5 Deleting a Component

To delete a component:

1. Open the Components page.
2. Select the component.
3. Click Delete Selected.
4. Confirm the deletion if prompted.

**Important:** Deleting a component also removes its assignments to projects.

The projects themselves are not deleted.

## 6.6 Searching Components

Use the search field to locate stored components.

Enter a search term relevant to the component.

For example:

```text
MPU6050
```

The table will display matching records.

Clear the search field to return to the full inventory list.

## 6.7 Inventory Quantity

The Quantity field represents the number of units recorded in inventory.

For example:

```text
Component: ESP32-S3
Quantity: 3
```

If one unit is physically removed from inventory, manually edit the component record to reflect the new quantity.

Project assignments do not automatically deduct inventory quantities in v0.1.0.

## 6.8 Datasheet References

The Datasheet field can store a reference to a component's technical documentation.

For example:

```text
https://example.com/component-datasheet.pdf
```

The field stores the reference; automatic datasheet downloading is not a feature of v0.1.0.

---

# 7. Devices

## 7.1 Overview

The Devices page manages registered electronic and computing devices.

Examples include:

- Raspberry Pi
- ESP32
- Arduino
- Raspberry Pi Pico
- Development boards
- Network-connected embedded devices

## 7.2 Device Information

Each device record supports:

| Field | Description |
|---|---|
| Name | Device name |
| Device Type | Device classification |
| Hostname | Network hostname |
| IP Address | Network address |
| MAC Address | Hardware network address |
| Status | Online or Offline |

## 7.3 Registering a Device

To register a device:

1. Open the Devices page.
2. Click Add Device.
3. Enter the device information.
4. Select the device status.
5. Click Save.

### Example: Raspberry Pi

| Field | Example Value |
|---|---|
| Name | Robot Pi |
| Device Type | Raspberry Pi |
| Hostname | robotpi.local |
| IP Address | 192.168.1.20 |
| MAC Address | AA:BB:CC:DD:EE:01 |
| Status | Offline |

## 7.4 Editing a Device

To update a device:

1. Select the device in the table.
2. Click Edit Selected.
3. Modify the information.
4. Click Save.

## 7.5 Deleting a Device

To delete a device:

1. Select the device.
2. Click Delete Selected.
3. Confirm the deletion if prompted.

**Important:** Deleting a device also deletes sensor readings associated with that device.

This behavior maintains database referential integrity.

## 7.6 Searching Devices

Enter a search term in the Devices page search field.

Use the search field to locate relevant device records.

## 7.7 Device Status

CircuitVault supports two device statuses:

| Status | Meaning |
|---|---|
| Online | Device is manually recorded as online |
| Offline | Device is manually recorded as offline |

Version 0.1.0 does not perform automatic network availability checks.

The user is responsible for maintaining accurate device status information.

---

# 8. Sensors

## 8.1 Overview

The Sensors page manages sensor measurements associated with registered devices.

Version 0.1.0 supports manual sensor data entry.

## 8.2 Sensor Reading Information

Each sensor reading contains:

| Field | Description |
|---|---|
| Device | Registered device associated with the measurement |
| Sensor Name | Name of the sensor |
| Metric | Measurement type |
| Value | Numerical measurement |
| Unit | Measurement unit |
| Timestamp | Time associated with the measurement |

## 8.3 Registering a Device First

Before recording a sensor measurement, the associated device must exist in the Devices module.

For example, to record MPU6050 measurements from a Raspberry Pi:

1. Open Devices.
2. Register the Raspberry Pi.
3. Open Sensors.
4. Add the sensor measurement.

## 8.4 Adding a Sensor Reading

To add a sensor reading:

1. Open the Sensors page.
2. Click Add Reading.
3. Select the registered device.
4. Enter the sensor name.
5. Enter the measurement type.
6. Enter the measurement value.
7. Enter the measurement unit.
8. Click Save.

### Example: MPU6050 Measurement

| Field | Example Value |
|---|---|
| Device | Robot Pi |
| Sensor Name | MPU6050 |
| Metric | Acceleration X |
| Value | 0.12 |
| Unit | g |

## 8.5 Editing a Sensor Reading

To edit a reading:

1. Select the reading in the table.
2. Click Edit Selected.
3. Modify the measurement information.
4. Click Save.

## 8.6 Deleting a Sensor Reading

To delete a reading:

1. Select the reading.
2. Click Delete Selected.
3. Confirm the deletion if prompted.

## 8.7 Searching Sensor Readings

Use the Sensors page search field to locate stored measurements.

## 8.8 Sensor Measurement Units

CircuitVault can store measurements using different units.

Examples include:

| Measurement | Example Unit |
|---|---|
| Temperature | °C |
| Acceleration | g |
| Angular Velocity | °/s |
| Voltage | V |
| Current | A |
| Distance | mm |

The application stores the unit associated with each measurement.

Automatic unit conversion is not included in v0.1.0.

## 8.9 Automatic Sensor Collection

CircuitVault v0.1.0 does not automatically retrieve live measurements from connected hardware.

Automated sensor acquisition is planned for future versions.

---

# 9. Projects

## 9.1 Overview

The Projects page allows users to organize electronics and engineering projects.

Each project can be associated with components already stored in the inventory.

## 9.2 Project Information

Each project contains:

| Field | Description |
|---|---|
| Name | Project name |
| Description | Project description |
| Status | Current project status |
| Created At | Creation timestamp |

## 9.3 Project Statuses

CircuitVault supports four project statuses.

| Status | Description |
|---|---|
| Planning | Project is being planned |
| Active | Project is currently being developed |
| On Hold | Project development is temporarily paused |
| Completed | Project work is finished |

## 9.4 Creating a Project

To create a project:

1. Open the Projects page.
2. Click Add Project.
3. Enter a project name.
4. Select the project status.
5. Enter a description.
6. Click Save.

### Example: ESP32-S3 Flight Controller

| Field | Example Value |
|---|---|
| Name | ESP32-S3 Flight Controller |
| Status | Active |
| Description | Indoor flight controller prototype using ESP32-S3 and MPU6050 sensors |

## 9.5 Editing a Project

To edit a project:

1. Select the project in the Projects table.
2. Click Edit Selected.
3. Modify the project information.
4. Click Save.

## 9.6 Deleting a Project

To delete a project:

1. Select the project.
2. Click Delete Selected.
3. Confirm the deletion.

Deleting a project removes its component assignments.

The inventory component records remain available.

## 9.7 Searching Projects

The Projects page supports searching by:

- Project name
- Project description
- Project status

Enter a search term in the search field.

Clear the field to display all projects.

---

# 10. Assigning Components to Projects

## 10.1 Overview

CircuitVault allows users to associate inventory components with engineering projects.

This provides a record of which components are planned for or used by a project.

## 10.2 Assigning a Component

To assign a component:

1. Open the Projects page.
2. Select an existing project.
3. Click Assign Component.
4. Select a component from the inventory.
5. Enter the assignment quantity.
6. Click Save.

The component will appear in the Assigned Components table.

## 10.3 Assignment Example

Suppose the inventory contains:

| Component | Inventory Quantity |
|---|---:|
| MPU6050 | 3 |
| ESP32-S3 | 2 |

The user creates the project:

**ESP32-S3 Flight Controller**

The user then assigns:

| Component | Assigned Quantity |
|---|---:|
| MPU6050 | 3 |
| ESP32-S3 | 1 |

The project displays:

**Component Types:** 2

**Assigned Quantity:** 4

## 10.4 Assignment Quantities and Inventory

Component assignments do not automatically reduce inventory quantities.

For example:

```text
Component: MPU6050

Inventory Quantity: 3

Assigned to Project: 2

Inventory Quantity After Assignment: 3
```

The inventory quantity remains unchanged.

If components are physically consumed or removed from storage, users must update inventory quantities manually.

## 10.5 Updating an Assignment

To change the assigned quantity:

1. Select the project.
2. Click Assign Component.
3. Select the same inventory component.
4. Enter the new quantity.
5. Click Save.

The existing assignment quantity will be updated.

## 10.6 Removing an Assignment

To remove a component assignment:

1. Select the project.
2. Select the component in the Assigned Components table.
3. Click Remove Assignment.
4. Confirm the action.

The component association will be removed.

The inventory record will remain unchanged.

## 10.7 Project Component Statistics

The Projects table displays:

| Statistic | Description |
|---|---|
| Component Types | Number of distinct assigned components |
| Assigned Quantity | Sum of assigned quantities |

These statistics are calculated from the stored component assignments.

---

# 11. Database and Data Storage

## 11.1 SQLite Database

CircuitVault uses SQLite for persistent local storage.

The database stores:

- Component inventory
- Registered devices
- Sensor readings
- Engineering projects
- Component assignments

## 11.2 Database Location

The development version uses a database file located at:

```text
data/circuitvault.db
```

The database path used by a packaged executable may depend on its final packaging configuration.

## 11.3 Data Persistence

Records are stored in the database and remain available after the application closes.

For example:

1. Create a component.
2. Close CircuitVault.
3. Restart the application.
4. Open Components.
5. Verify that the component remains available.

## 11.4 Database Relationships

CircuitVault maintains relationships between records.

### Devices and Sensor Readings

Sensor readings belong to registered devices.

Deleting a device removes its associated sensor readings.

### Projects and Components

Projects can have multiple component assignments.

Deleting a project removes its assignments without deleting the inventory components.

Deleting an inventory component removes its project assignments.

## 11.5 Database Backup

Users should periodically back up their database file.

To create a simple backup:

1. Close CircuitVault.
2. Navigate to the `data/` directory.
3. Copy `circuitvault.db`.
4. Store the copy in a separate backup location.

Example:

```text
CircuitVault_Backup/
└── circuitvault.db
```

**Important:** Close the application before copying the database to avoid capturing an incomplete or inconsistent backup.

## 11.6 Restoring a Backup

To restore a backup:

1. Close CircuitVault.
2. Locate the backup database.
3. Make a separate copy of the current database for safety.
4. Replace the current database file with the backup.
5. Restart CircuitVault.
6. Verify that the restored records are present.

Restoring an older backup replaces the current stored data with the contents of that backup.

---

# 12. Troubleshooting

## 12.1 Application Does Not Start

**Problem:** CircuitVault does not open.

**Possible causes:**

- Python is not installed.
- The virtual environment is not activated.
- Required dependencies are missing.
- The application is launched from an incorrect directory.

**Solution:**

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the application:

```powershell
python main.py
```

## 12.2 Missing PySide6

**Problem:**

```text
ModuleNotFoundError: No module named 'PySide6'
```

**Solution:**

Install PySide6 in the active environment:

```powershell
python -m pip install PySide6
```

Alternatively, reinstall the project's dependencies:

```powershell
python -m pip install -r requirements.txt
```

## 12.3 Database Error

**Problem:** CircuitVault displays a database error.

**Possible causes:**

- Database file is inaccessible.
- Database directory is missing.
- Filesystem permissions prevent writing.
- Database file is corrupted.

**Solution:**

1. Close CircuitVault.
2. Verify that the application has permission to access its data directory.
3. Confirm that the database file exists.
4. Restore a known-good backup if necessary.

Do not delete the database file unless you intend to remove its stored records.

## 12.4 Cannot Add a Component

**Problem:** The component cannot be saved.

**Possible causes:**

- Component name is missing.
- Component category is missing.
- Quantity is invalid.

**Solution:**

Verify that the required fields contain valid information.

Inventory quantities must not be negative.

## 12.5 Cannot Add a Project

**Problem:** The project cannot be saved.

**Possible causes:**

- Project name is empty.
- Project status is invalid.

**Solution:**

Enter a project name and select a supported status.

## 12.6 Cannot Assign a Component

**Problem:** A component cannot be assigned to a project.

**Possible causes:**

- No project is selected.
- No inventory components exist.
- The assignment quantity is invalid.

**Solution:**

1. Create at least one inventory component.
2. Create or select a project.
3. Click Assign Component.
4. Select the component.
5. Enter a positive quantity.

## 12.7 Cannot Add a Sensor Reading

**Problem:** A sensor reading cannot be saved.

**Possible cause:** No registered device is available.

**Solution:**

Register the associated device in the Devices module before creating the reading.

## 12.8 Dashboard Statistics Appear Outdated

**Problem:** Dashboard values do not reflect recent changes.

**Solution:**

Navigate away from the Dashboard and return to it.

The Dashboard refreshes its statistics when the page is opened.

---

# 13. Frequently Asked Questions

## 13.1 Does CircuitVault Require Internet Access?

No.

The core application works locally.

Internet access may be required during installation to download dependencies.

## 13.2 Can CircuitVault Automatically Discover Raspberry Pi Devices?

Not in version 0.1.0.

Automatic network discovery is planned for a future release.

## 13.3 Can CircuitVault Read Live ESP32 Sensor Data?

Not in version 0.1.0.

Sensor readings are entered manually.

## 13.4 Does Assigning Components Reduce Inventory?

No.

Component assignments are recorded separately from inventory quantities.

## 13.5 Can One Component Be Assigned to Multiple Projects?

Yes.

A component can be associated with multiple projects.

Each project maintains its own assignment quantity.

## 13.6 Does Deleting a Project Delete Its Components?

No.

Deleting a project removes its component assignments but preserves the inventory records.

## 13.7 Does Deleting a Device Delete Its Sensor Readings?

Yes.

Associated sensor readings are removed when the registered device is deleted.

## 13.8 Where Is Application Data Stored?

The development version stores data in a local SQLite database.

The standard development database location is:

```text
data/circuitvault.db
```

## 13.9 Can CircuitVault Be Used Without Programming Experience?

Yes.

The graphical interface provides controls for managing records without writing Python code or SQL queries.

---

# 14. Future Features

CircuitVault is designed to support additional functionality in future versions.

Potential enhancements include:

### Network Discovery

- Raspberry Pi discovery
- ESP32 discovery
- Local network scanning
- Automatic device availability checks

### Sensor Integration

- Live sensor measurements
- Serial communication
- Network-based data acquisition
- Sensor history visualization

### Inventory Management

- Low-stock alerts
- Inventory import and export
- Component