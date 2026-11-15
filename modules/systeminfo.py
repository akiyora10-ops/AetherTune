import platform, psutil

def summary():
    return {
        'os': platform.system(),
        'release': platform.release(),
        'machine': platform.machine(),
        'cpu': platform.processor(),
        'ram_gb': round(psutil.virtual_memory().total/1e9,2),
    }
