import customtkinter as ctk
from .utils import run_ps, get_gpu_names, is_admin, reg_set, reg_get

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(frame, text="GPU Tweaks (AMD)", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0,12))

    info = ctk.CTkFrame(frame, corner_radius=12)
    info.pack(fill="x", pady=6)
    ctk.CTkLabel(info, text="Detected GPUs", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,4))
    for g in get_gpu_names():
        ctk.CTkLabel(info, text="• " + g).pack(anchor="w", padx=16, pady=2)
    # driver
    out, _ = run_ps("Get-CimInstance Win32_VideoController | Select-Object Name, DriverVersion, DriverDate | Format-List | Out-String")
    tb = ctk.CTkTextbox(info, height=120)
    tb.pack(fill="x", padx=16, pady=8)
    tb.insert("1.0", out)
    tb.configure(state="disabled")

    # actions
    act = ctk.CTkFrame(frame, corner_radius=12)
    act.pack(fill="x", pady=6)
    ctk.CTkLabel(act, text="Actions", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    row = ctk.CTkFrame(act, fg_color="transparent")
    row.pack(fill="x", padx=16, pady=6)
    ctk.CTkButton(row, text="Open AMD Software", command=lambda: run_ps("Start-Process 'amdsoftware' -ErrorAction SilentlyContinue")).pack(side="left", padx=4)
    ctk.CTkButton(row, text="Open Device Manager", command=lambda: run_ps("Start-Process devmgmt.msc")).pack(side="left", padx=4)
    ctk.CTkButton(row, text="Restart AMD Driver (pnputil)", command=lambda: run_ps("pnputil /restart-device (Get-PnpDevice -Class Display | Where-Object {$_.FriendlyName -match 'AMD|Radeon'} | Select-Object -First 1 -ExpandProperty InstanceId)")).pack(side="left", padx=4)

    # registry tweaks for GPU
    tw = ctk.CTkFrame(frame, corner_radius=12)
    tw.pack(fill="x", pady=6)
    ctk.CTkLabel(tw, text="GPU Registry Tweaks", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    tweaks = [
        ("Disable fullscreen optimizations (global)", r"HKCU\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers", "*", "~ DISABLEDXMAXIMIZEDWINDOWEDMODE", "str"),
        ("Enable Hardware Accelerated GPU Scheduling", r"HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers", "HwSchMode", 2, "dword"),
        ("Disable MPO (Multi-Plane Overlay) - fixes stutter", r"HKLM\SOFTWARE\Microsoft\Windows\Dwm", "OverlayTestMode", 5, "dword"),
    ]
    for name, path, valname, value, kind in tweaks:
        r = ctk.CTkFrame(tw, fg_color="transparent")
        r.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(r, text=name, wraplength=600).pack(side="left")
        def apply(p=path, vn=valname, v=value, k=kind):
            if k == "dword":
                reg_set(p, vn, v)
            else:
                reg_set(p, vn, v, __import__("winreg").REG_SZ)
        ctk.CTkButton(r, text="Apply", width=80, command=apply).pack(side="right", padx=4)
        ctk.CTkButton(r, text="Revert", width=80, command=lambda p=path, vn=valname: __import__("modules.utils", fromlist=["reg_delete"]).reg_delete(p, vn)).pack(side="right", padx=4)

    note = ctk.CTkLabel(frame, text="Note: True clock/voltage OC requires AMD ADLX SDK (native). This app focuses on safe OS/driver-level tweaks + monitoring. Full ADLX OC module planned.", text_color="gray", wraplength=1100)
    note.pack(anchor="w", pady=12)
    return frame
