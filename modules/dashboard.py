import customtkinter as ctk
from .utils import get_cpu_name, get_gpu_names, get_ram, get_battery, get_temps, is_admin, run_ps

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.grid_columnconfigure((0,1,2), weight=1)

    title = ctk.CTkLabel(frame, text="Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
    title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,12))

    # system info card
    info = ctk.CTkFrame(frame, corner_radius=12)
    info.grid(row=1, column=0, columnspan=3, sticky="ew", pady=6)
    ctk.CTkLabel(info, text="System", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,4))
    cpu = get_cpu_name()
    gpus = get_gpu_names()
    total, avail, pct = get_ram()
    bat = get_battery()
    temps = get_temps()
    lines = [
        f"CPU: {cpu}",
        f"GPU: {', '.join(gpus) if gpus else 'Unknown'}",
        f"RAM: {total/1e9:.1f} GB total / {avail/1e9:.1f} GB free ({pct}% used)",
        f"Battery: {bat[0]}% ({'plugged' if bat and bat[1] else 'on battery'})" if bat else "Battery: n/a (desktop)",
        f"Temps (C): {temps if temps else 'n/a'}",
        f"Admin: {'YES' if is_admin() else 'NO - run as admin for full tweaks'}",
    ]
    for l in lines:
        ctk.CTkLabel(info, text=l, anchor="w").pack(anchor="w", padx=16, pady=2)
    ctk.CTkLabel(info, text="", height=6).pack()

    # quick actions
    qa = ctk.CTkFrame(frame, corner_radius=12)
    qa.grid(row=2, column=0, columnspan=3, sticky="ew", pady=6)
    ctk.CTkLabel(qa, text="Quick Actions", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    btns = ctk.CTkFrame(qa, fg_color="transparent")
    btns.pack(fill="x", padx=16, pady=(0,12))
    actions = [
        ("High Performance Power Plan", lambda: _set_hp()),
        ("Clear Temp Files", lambda: _clean()),
        ("Flush DNS", lambda: run_ps("ipconfig /flushdns")),
        ("Restart Explorer", lambda: run_ps("Stop-Process -Name explorer -Force; Start-Process explorer")),
    ]
    for i,(t,cb) in enumerate(actions):
        b = ctk.CTkButton(btns, text=t, command=lambda c=cb: c())
        b.grid(row=i//2, column=i%2, padx=6, pady=6, sticky="ew")
    btns.grid_columnconfigure((0,1), weight=1)

    # status
    st = ctk.CTkFrame(frame, corner_radius=12)
    st.grid(row=3, column=0, columnspan=3, sticky="ew", pady=6)
    ctk.CTkLabel(st, text="Tips", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,4))
    for t in [
        "Run as Administrator to apply registry/power tweaks.",
        "GPU overclocking on AMD needs ADLX SDK (C++). This app exposes info + safe registry/perf tweaks; full OC coming.",
        "Always create a restore point before registry tweaks (Settings tab).",
    ]:
        ctk.CTkLabel(st, text="• "+t, anchor="w", wraplength=1100).pack(anchor="w", padx=16, pady=2)
    ctk.CTkLabel(st, text="", height=6).pack()

    return frame

def _set_hp():
    from .utils import list_power_plans, set_power_plan
    for g,n in list_power_plans():
        if "high performance" in n.lower():
            set_power_plan(g)

def _clean():
    import os, shutil
    for p in [os.environ.get("TEMP"), r"C:\Windows\Temp"]:
        if p and os.path.exists(p):
            for f in os.listdir(p):
                fp = os.path.join(p, f)
                try:
                    if os.path.isfile(fp) or os.path.islink(fp):
                        os.remove(fp)
                    elif os.path.isdir(fp):
                        shutil.rmtree(fp, ignore_errors=True)
                except Exception:
                    pass
