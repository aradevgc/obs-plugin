"""
OBS Controller - Aplicación de escritorio para macOS
Genera un DMG con la aplicación que inicia el servidor automáticamente
"""

from setuptools import setup
import py2app

APP = ['server/app.py']
DATA_FILES = [
    'templates',
]

OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleName': 'OBS Controller',
        'CFBundleDisplayName': 'OBS Controller',
        'CFBundleIdentifier': 'com.obscontroller.app',
        'CFBundleVersion': '1.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2024',
        'LSMinimumSystemVersion': '10.15',
        'NSHighResolutionCapable': True,
    },
    'resources': ['templates'],
    'iconfile': None,  # Añadir icono si se desea
    'site_packages': True,
    'includes': ['flask', 'flask_socketio', 'socketio'],
}

setup(
    name='OBS Controller',
    version='1.0.0',
    description='Controlador de overlays para OBS',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
