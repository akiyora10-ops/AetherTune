import customtkinter as ctk, os, shutil, subprocess
from .utils import run_ps

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(frame, text="Cleaner", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0,12))

    paths = [
        ("User Temp", os.environ.get("TEMP")),
        ("Windows Temp", r"C:\Windows\Temp"),
        ("Prefetch", r"C:\Windows\Prefetch"),
        ("Thumbnail Cache", os.path.join(os.environ["LOCALAPPDATA"], r"Microsoft\Windows\Explorer")),
        ("Windows Update Cache", r"C:\Windows\SoftwareDistribution\Download"),
    ]
    card = ctk.CTkFrame(frame, corner_radius=12)
    card.pack(fill="x", pady=6)
    ctk.CTkLabel(card, text="Clean Targets", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))

    status = ctk.CTkLabel(card, text="", text_color="gray")
    status.pack(anchor="w", padx=16)

    def clean_one(p):
        if not p or not os.path.exists(p): return 0
        sz = 0
        for root, dirs, files in os.walk(p):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    sz += os.path.getsize(fp)
                    os.remove(fp)
                except Exception:
                    pass
        for d in os.listdir(p):
            dp = os.path.join(p, d)
            if os.path.isdir(dp):
                shutil.rmtree(dp, ignore_errors=True)
        return sz

    def clean_all():
        total = 0
        for name, p in paths:
            s = clean_one(p)
            total += s
            status.configure(text=f"Cleaned {name}: {s/1e6:.1f} MB")
            frame.update()
        status.configure(text=f"Total freed: {total/1e6:.1f} MB")
        # DNS flush
        run_ps("ipconfig /flushdns")

    for name, p in paths:
        r = ctk.CTkFrame(card, fg_color="transparent")
        r.pack(fill="x", padx=16, pady=3)
        ctk.CTkLabel(r, text=f"{name}: {p}").pack(side="left")
    ctk.CTkButton(card, text="Clean All", command=clean_all).pack(anchor="w", padx=16, pady=10)

    # Disk cleanup
    dc = ctk.CTkFrame(frame, corner_radius=12)
    dc.pack(fill="x", pady=6)
    ctk.CTkLabel(dc, text="Windows Disk Cleanup", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    ctk.CTkButton(dc, text="Run cleanmgr", command=lambda: subprocess.Popen("cleanmgr")).pack(anchor="w", padx=16, pady=6)

    return frame
