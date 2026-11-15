# Architecture

AetherTune is a Python + customtkinter desktop app.

- `main.py`: app shell, navigation.
- `modules/`: feature modules, each exposes `build(parent)`.
- `modules/utils.py`: shared helpers (system info, registry, power plans).
- `installer/`: PyInstaller exe + PowerShell installer.
- `website/`: marketing site (Lenis + anime.js).

Data flow: UI -> utils -> Windows APIs (registry, PowerShell, WMI).
