# CircuitVault

**CircuitVault** is a Python desktop application for managing electronic components, hardware devices, sensor readings, and engineering projects.

Built with **Python, PySide6, and SQLite**, CircuitVault provides a centralized environment for organizing electronics inventory, maintaining device records, tracking sensor measurements, and assigning components to projects.

The application is designed for electronics hobbyists, embedded systems developers, robotics enthusiasts, engineering students, and makers.

**Current Version:** 0.1.0  
**Development Status:** Initial Release Preparation  
**Platform:** Windows 11  
**Language:** Python  
**GUI Framework:** PySide6  
**Database:** SQLite

---

## Features

CircuitVault v0.1.0 includes five primary modules.

### Dashboard

The Dashboard provides an overview of stored application data.

- Total component records
- Registered devices
- Devices marked online
- Stored sensor readings
- Updated statistics when navigating to the Dashboard

### Components

Manage electronic components and maintain a local inventory.

- Add electronic components
- Edit existing component records
- Delete components
- Search inventory records
- Track component quantities
- Store manufacturer and part number information
- Record storage locations
- Store datasheet references and notes

### Devices

Maintain a database of electronic and computing devices.

- Register hardware devices
- Edit device information
- Delete device records
- Search registered devices
- Store hostnames, IP addresses, and MAC addresses
- Track manually recorded Online and Offline statuses

Supported device records can represent Raspberry Pi, ESP32, Arduino, Raspberry Pi Pico, and other electronic systems.

Automatic network discovery is not included in v0.1.0.

### Sensors

Record and manage sensor measurements associated with registered devices.

- Add sensor readings
- Edit recorded measurements
- Delete readings
- Search sensor records
- Associate measurements with registered devices
- Store measurement values and units
- Maintain measurement history in SQLite

Sensor measurements are entered manually in v0.1.0.

### Projects

Organize engineering projects and associate inventory components with them.

- Create projects
- Edit project information
- Delete projects
- Search projects
- Track project statuses
- Assign inventory components to projects
- Specify component assignment quantities
- Update existing assignments
- Remove component assignments
- View project component statistics

Supported project statuses:

- Planning
- Active
- On Hold
- Completed

Component assignments do not automatically reduce inventory quantities.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| PySide6 | Desktop graphical interface |
| SQLite | Local persistent database |
| pytest | Automated testing |
| pytest-qt | GUI testing |
| PyInstaller | Planned Windows executable packaging |
| Git | Version control |

The application uses a modular architecture separating GUI components, database repositories, and application data models.

---

## System Requirements

**Supported operating system:** Windows 11

To run CircuitVault from source, you will need:

- Python 3
- pip
- A Python virtual environment
- Project dependencies listed in `requirements.txt`

No specialized electronics hardware or active internet connection is required for normal application operation.

Internet access may be necessary to install dependencies.

---

## Installation

### 1. Obtain the Source Code

Clone the repository:

```powershell
git clone <repository-url>
```

Replace `<repository-url>` with the actual CircuitVault repository address.

Navigate into the project directory:

```powershell
cd CircuitVault
```

Alternatively, download and extract the source archive.

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

### 3. Activate the Virtual Environment

In Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Launch CircuitVault

```powershell
python main.py
```

The application will open its main window with the Dashboard selected.

---

## Application Structure

```text
CircuitVault/
|
|-- main.py
|-- README.md
|-- CHANGELOG.md
|-- LICENSE
|-- requirements.txt
|-- requirements-lock.txt
|-- pytest.ini
|
|-- app/
|   |-- main_window.py
|   |
|   |-- pages/
|   |   |-- dashboard_page.py
|   |   |-- components_page.py
|   |   |-- devices_page.py
|   |   |-- sensors_page.py
|   |   |-- projects_page.py
|   |
|   |-- dialogs/
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
|   |-- scanner.py
|
|-- sensors/
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

The `network/` and `sensors/` directories are reserved for future automated hardware communication features.

---

## Database

CircuitVault uses SQLite for local data storage.

The database contains five primary tables:

| Table | Purpose |
|---|---|
| `components` | Electronic component inventory |
| `devices` | Registered hardware devices |
| `sensor_readings` | Recorded sensor measurements |
| `projects` | Engineering project records |
| `project_components` | Project-component assignments |

The development database is stored at:

```text
data/circuitvault.db
```

### Database Relationships

CircuitVault maintains relationships between stored records.

**Devices and Sensors