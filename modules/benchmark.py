import customtkinter as ctk
from .utils import run_ps

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color='transparent')
    ctk.CTkLabel(frame, text='Benchmark', font=ctk.CTkFont(size=24, weight='bold')).pack(anchor='w', pady=(0,12))
    ctk.CTkLabel(frame, text='Run a quick CPU stress to gauge performance.', text_color='gray').pack(anchor='w', pady=4)
    def run_stress():
        run_ps('Start-Process powershell -ArgumentList "-NoProfile -Command while($true){}"')
    ctk.CTkButton(frame, text='Start CPU Stress (manual stop)', command=run_stress).pack(anchor='w', pady=8)
    return frame
