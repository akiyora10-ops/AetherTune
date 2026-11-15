import ctypes

def toast(title, msg):
    # simple message box fallback
    ctypes.windll.user32.MessageBoxW(0, msg, title, 0)
