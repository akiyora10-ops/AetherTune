import shutil

def free_gb(path):
    return round(shutil.disk_usage(path).free/1e9,2)
