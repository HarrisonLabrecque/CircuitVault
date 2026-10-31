# -*- mode: python ; coding: utf-8 -*-

"""
CircuitVault - PyInstaller Configuration
Version: 0.1.0

Build:
    Windows one-file executable
    PySide6 graphical application
"""

from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules


# ============================================================
# BUILD CONFIGURATION
# ============================================================

PROJECT_DIR = Path(SPECPATH).resolve()

APP_NAME = "CircuitVault"


# ============================================================
# HIDDEN IMPORTS
# ============================================================

hidden_imports = []

for package in (
    "app",
    "database",
    "models",
    "network",
    "sensors",
):
    hidden_imports.extend(
        collect_submodules(package)
    )


# ============================================================
# ANALYSIS
# ============================================================

a = Analysis(
    [str(PROJECT_DIR / "main.py")],

    pathex=[
        str(PROJECT_DIR),
    ],

    binaries=[],

    datas=[
        (
            str(PROJECT_DIR / "styles" / "main.qss"),
            "styles"
        ),
    ],

    hiddenimports=hidden_imports,

    hookspath=[],

    hooksconfig={},

    runtime_hooks=[],

    excludes=[
        "pytest",
        "pytestqt",
    ],

    noarchive=False,
)


# ============================================================
# PYTHON ARCHIVE
# ============================================================

pyz = PYZ(
    a.pure,
)


# ============================================================
# EXECUTABLE
# ============================================================

exe = EXE(
    pyz,

    a.scripts,

    a.binaries,

    a.datas,

    [],

    name=APP_NAME,

    debug=False,

    bootloader_ignore_signals=False,

    strip=False,

    upx=False,

    console=False,

    disable_windowed_traceback=False,
)