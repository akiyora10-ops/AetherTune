import customtkinter as ctk, os, subprocess
from .utils import is_admin, run_ps

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(frame, text="Settings", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0,12))

    card = ctk.CTkFrame(frame, corner_radius=12)
    card.pack(fill="x", pady=6)
    ctk.CTkLabel(card, text="Safety", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    ctk.CTkButton(card, text="Create System Restore Point", command=lambda: run_ps("Checkpoint-Computer -Description 'AetherTune' -RestorePointType 'MODIFY_SETTINGS'")).pack(anchor="w", padx=16, pady=4)
    ctk.CTkButton(card, text="Open System Restore", command=lambda: run_ps("rstrui.exe")).pack(anchor="w", padx=16, pady=4)
    ctk.CTkButton(card, text="Open Registry Editor", command=lambda: subprocess.Popen("regedit")).pack(anchor="w", padx=16, pady=4)

    about = ctk.CTkFrame(frame, corner_radius=12)
    about.pack(fill="x", pady=6)
    ctk.CTkLabel(about, text="About AetherTune", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    for l in [
        "Version 0.1.0",
        "AMD laptop-focused Windows tuning suite.",
        "Admin: " + ("YES" if is_admin() else "NO"),
        "Built with Python + customtkinter.",
    ]:
        ctk.CTkLabel(about, text=l).pack(anchor="w", padx=16, pady=2)
    ctk.CTkLabel(about, text="", height=6).pack()
    return frame
