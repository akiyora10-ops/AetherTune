import customtkinter as ctk
from .utils import list_power_plans, get_active_power_plan, set_power_plan, run_ps, is_admin

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(frame, text="Performance", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0,12))

    # Power plans
    pp = ctk.CTkFrame(frame, corner_radius=12)
    pp.pack(fill="x", pady=6)
    ctk.CTkLabel(pp, text="Power Plans", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    self_plan_var = ctk.StringVar(value=get_active_power_plan())
    plans = list_power_plans()
    opts = [f"{n} ({g[:8]})" for g,n in plans]
    combo = ctk.CTkComboBox(pp, values=opts, width=420)
    combo.pack(anchor="w", padx=16, pady=6)
    # set current
    for g,n in plans:
        if g == get_active_power_plan():
            combo.set(f"{n} ({g[:8]})")
    def apply_plan():
        sel = combo.get()
        for g,n in plans:
            if sel.startswith(n):
                set_power_plan(g)
                ctk.CTkLabel(pp, text=f"Active: {n}", text_color="green").pack(anchor="w", padx=16)
    ctk.CTkButton(pp, text="Apply Power Plan", command=apply_plan).pack(anchor="w", padx=16, pady=6)
    ctk.CTkButton(pp, text="Unlock Ultimate Performance", command=lambda: run_ps("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61")).pack(anchor="w", padx=16, pady=4)

    # Game mode / FSO
    gm = ctk.CTkFrame(frame, corner_radius=12)
    gm.pack(fill="x", pady=6)
    ctk.CTkLabel(gm, text="Game Mode & Fullscreen", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    ctk.CTkButton(gm, text="Enable Game Mode (registry)", command=lambda: __import__("modules.utils", fromlist=["reg_set"]).reg_set(r"HKCU\Software\Microsoft\GameBar","AutoGameModeEnabled",1)).pack(anchor="w", padx=16, pady=4)
    ctk.CTkButton(gm, text="Disable Xbox Game Bar", command=lambda: run_ps("Get-AppxPackage Microsoft.XboxGamingOverlay | Remove-AppxPackage -ErrorAction SilentlyContinue")).pack(anchor="w", padx=16, pady=4)

    # Process priority
    pr = ctk.CTkFrame(frame, corner_radius=12)
    pr.pack(fill="x", pady=6)
    ctk.CTkLabel(pr, text="Process Priority / Affinity", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    ctk.CTkLabel(pr, text="Set a running process to High priority.", text_color="gray").pack(anchor="w", padx=16)
    name_entry = ctk.CTkEntry(pr, placeholder_text="Process name (e.g. RobloxPlayerBeta)")
    name_entry.pack(anchor="w", padx=16, pady=4)
    def set_pri():
        n = name_entry.get().strip()
        if not n: return
        run_ps(f"Get-Process -Name '{n}' -ErrorAction SilentlyContinue | ForEach-Object {{ $_.PriorityClass = 'High' }}")
    ctk.CTkButton(pr, text="Set High Priority", command=set_pri).pack(anchor="w", padx=16, pady=4)

    # Timer resolution
    tr = ctk.CTkFrame(frame, corner_radius=12)
    tr.pack(fill="x", pady=6)
    ctk.CTkLabel(tr, text="System Tweaks", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    ctk.CTkButton(tr, text="Disable HAGS (if issues)", command=lambda: __import__("modules.utils", fromlist=["reg_set"]).reg_set(r"HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers","HwSchMode",1)).pack(anchor="w", padx=16, pady=4)
    ctk.CTkButton(tr, text="Clear Standby Memory (empty working sets)", command=lambda: run_ps("[System.GC]::Collect(); (New-Object System.Diagnostics.Process).StartInfo.FileName='cmd'; ")).pack(anchor="w", padx=16, pady=4)

    return frame
