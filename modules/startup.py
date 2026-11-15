import customtkinter as ctk
from .utils import run_ps

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(frame, text="Startup & Services", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0,12))

    # Startup items
    st = ctk.CTkFrame(frame, corner_radius=12)
    st.pack(fill="both", expand=True, pady=6)
    ctk.CTkLabel(st, text="Startup Programs (HKCU/HKLM Run)", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    txt = ctk.CTkTextbox(st, height=220)
    txt.pack(fill="x", padx=16, pady=6)
    def refresh_startup():
        out, _ = run_ps("Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location | Format-Table -AutoSize | Out-String")
        txt.delete("1.0", "end")
        txt.insert("1.0", out)
    refresh_startup()
    ctk.CTkButton(st, text="Refresh", command=refresh_startup).pack(anchor="w", padx=16, pady=4)

    # services
    sv = ctk.CTkFrame(frame, corner_radius=12)
    sv.pack(fill="both", expand=True, pady=6)
    ctk.CTkLabel(sv, text="Service Control", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    ctk.CTkLabel(sv, text="Enter service name to disable/enable.", text_color="gray").pack(anchor="w", padx=16)
    entry = ctk.CTkEntry(sv, placeholder_text="Service name (e.g. DiagTrack)")
    entry.pack(anchor="w", padx=16, pady=4)
    row = ctk.CTkFrame(sv, fg_color="transparent")
    row.pack(anchor="w", padx=16, pady=4)
    def disable():
        n = entry.get().strip()
        if not n: return
        run_ps(f"Stop-Service -Name '{n}' -Force -ErrorAction SilentlyContinue; Set-Service -Name '{n}' -StartupType Disabled")
    def enable():
        n = entry.get().strip()
        if not n: return
        run_ps(f"Set-Service -Name '{n}' -StartupType Automatic")
    ctk.CTkButton(row, text="Disable", command=disable).pack(side="left", padx=4)
    ctk.CTkButton(row, text="Enable (Auto)", command=enable).pack(side="left", padx=4)

    # common bloat services quick buttons
    ctk.CTkLabel(sv, text="Quick disable common bloat:", text_color="gray").pack(anchor="w", padx=16, pady=(8,2))
    qrow = ctk.CTkFrame(sv, fg_color="transparent")
    qrow.pack(anchor="w", padx=16, pady=4)
    for svc in ["DiagTrack", "dmwappushservice", "SysMain", "XblAuthManager", "XblGameSave", "XboxNetApiSvc"]:
        ctk.CTkButton(qrow, text=svc, width=130, command=lambda s=svc: run_ps(f"Stop-Service -Name '{s}' -Force -ErrorAction SilentlyContinue; Set-Service -Name '{s}' -StartupType Disabled")).pack(side="left", padx=3, pady=2)

    return frame
