import customtkinter as ctk
from .utils import reg_set

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color='transparent')
    ctk.CTkLabel(frame, text='Privacy', font=ctk.CTkFont(size=24, weight='bold')).pack(anchor='w', pady=(0,12))
    items = [
        ('Disable telemetry', lambda: reg_set(r'HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection', 'AllowTelemetry', 0)),
        ('Disable activity history', lambda: reg_set(r'HKLM\SOFTWARE\Policies\Microsoft\Windows\System', 'EnableActivityFeed', 0)),
        ('Disable Cortana', lambda: reg_set(r'HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search', 'AllowCortana', 0)),
    ]
    for name, cb in items:
        ctk.CTkButton(frame, text=name, command=cb).pack(anchor='w', pady=4)
    return frame
