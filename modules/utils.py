import psutil, subprocess, platform, winreg, ctypes, os

def run_ps(cmd):
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-Command", cmd],
                           capture_output=True, text=True, timeout=20)
        return r.stdout.strip(), r.stderr.strip()
    except Exception as e:
        return "", str(e)

def get_cpu_name():
    out, _ = run_ps("(Get-CimInstance Win32_Processor).Name")
    return out or platform.processor()

def get_gpu_names():
    out, _ = run_ps("Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name")
    return [x for x in out.splitlines() if x.strip()]

def get_ram():
    m = psutil.virtual_memory()
    return m.total, m.available, m.percent

def get_battery():
    b = psutil.sensors_battery()
    if b is None:
        return None
    return b.percent, b.power_plugged

def get_temps():
    # psutil sensors may be empty on Windows; try WMI thermal
    out, _ = run_ps("Get-CimInstance MSAcpi_ThermalZoneTemperature -ErrorAction SilentlyContinue | Select-Object -ExpandProperty CurrentTemperature")
    vals = []
    for line in out.splitlines():
        line=line.strip()
        if line.isdigit():
            vals.append(round(int(line)/10 - 273.15, 1))
    return vals

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def list_power_plans():
    out, _ = run_ps("powercfg /list")
    plans = []
    for line in out.splitlines():
        if "GUID" in line or ":" in line:
            # parse: Power Scheme GUID: <guid>  (name)
            import re
            m = re.search(r"([0-9a-f-]{36})\s*\((.+)\)", line, re.I)
            if m:
                plans.append((m.group(1), m.group(2)))
    return plans

def get_active_power_plan():
    out, _ = run_ps("powercfg /getactivescheme")
    import re
    m = re.search(r"([0-9a-f-]{36})", out, re.I)
    return m.group(1) if m else ""

def set_power_plan(guid):
    subprocess.run(["powercfg", "/setactive", guid], capture_output=True)

def reg_set(path, name, value, kind=winreg.REG_DWORD):
    root, sub = _split(path)
    with winreg.CreateKey(root, sub) as k:
        winreg.SetValueEx(k, name, 0, kind, value)

def reg_get(path, name, default=None):
    root, sub = _split(path)
    try:
        with winreg.OpenKey(root, sub) as k:
            v, _ = winreg.QueryValueEx(k, name)
            return v
    except Exception:
        return default

def reg_delete(path, name):
    root, sub = _split(path)
    try:
        with winreg.OpenKey(root, sub, 0, winreg.KEY_SET_VALUE) as k:
            winreg.DeleteValue(k, name)
    except Exception:
        pass

def _split(path):
    if path.startswith("HKLM"):
        return winreg.HKEY_LOCAL_MACHINE, path[5:].lstrip("\\")
    if path.startswith("HKCU"):
        return winreg.HKEY_CURRENT_USER, path[5:].lstrip("\\")
    if path.startswith("HKCR"):
        return winreg.HKEY_CLASSES_ROOT, path[5:].lstrip("\\")
    raise ValueError(path)

def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -1, "", str(e)
