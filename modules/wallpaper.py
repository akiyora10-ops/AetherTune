import customtkinter as ctk, os, ctypes, threading, time, subprocess
from tkinter import filedialog

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 1
SPIF_SENDCHANGE = 2

def set_wallpaper(path):
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(frame, text="Wallpaper & Modding", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0,12))

    card = ctk.CTkFrame(frame, corner_radius=12)
    card.pack(fill="x", pady=6)
    ctk.CTkLabel(card, text="Static Wallpaper", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    path_var = ctk.StringVar()
    ctk.CTkEntry(card, textvariable=path_var, width=500).pack(anchor="w", padx=16, pady=4)
    def browse():
        p = filedialog.askopenfilename(filetypes=[("Images","*.jpg *.jpeg *.png *.bmp")])
        if p: path_var.set(p)
    def apply():
        if path_var.get():
            set_wallpaper(path_var.get())
    ctk.CTkButton(card, text="Browse", command=browse).pack(anchor="w", padx=16, pady=2)
    ctk.CTkButton(card, text="Apply Wallpaper", command=apply).pack(anchor="w", padx=16, pady=6)

    # slideshow
    ss = ctk.CTkFrame(frame, corner_radius=12)
    ss.pack(fill="x", pady=6)
    ctk.CTkLabel(ss, text="Slideshow / Live Mod", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    folder_var = ctk.StringVar()
    ctk.CTkEntry(ss, textvariable=folder_var, width=500, placeholder_text="Folder of images").pack(anchor="w", padx=16, pady=4)
    def browse_folder():
        p = filedialog.askdirectory()
        if p: folder_var.set(p)
    ctk.CTkButton(ss, text="Browse Folder", command=browse_folder).pack(anchor="w", padx=16, pady=2)
    interval = ctk.CTkSlider(ss, from_=5, to=120, number_of_steps=23)
    interval.set(30)
    interval.pack(anchor="w", padx=16, pady=4)
    lbl = ctk.CTkLabel(ss, text="Interval: 30s")
    lbl.pack(anchor="w", padx=16)
    interval.configure(command=lambda v: lbl.configure(text=f"Interval: {int(v)}s"))

    running = {"v": False}
    def run_slideshow():
        running["v"] = True
        folder = folder_var.get()
        imgs = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith((".jpg",".jpeg",".png",".bmp"))]
        i = 0
        while running["v"] and imgs:
            set_wallpaper(imgs[i % len(imgs)])
            i += 1
            time.sleep(int(interval.get()))
    def start():
        if not running["v"]:
            threading.Thread(target=run_slideshow, daemon=True).start()
    def stop():
        running["v"] = False
    ctk.CTkButton(ss, text="Start Slideshow", command=start).pack(side="left", padx=16, pady=6)
    ctk.CTkButton(ss, text="Stop", command=stop).pack(side="left", padx=4, pady=6)

    # Lively
    lv = ctk.CTkFrame(frame, corner_radius=12)
    lv.pack(fill="x", pady=6)
    ctk.CTkLabel(lv, text="Live Wallpaper (Lively Wallpaper integration)", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    ctk.CTkLabel(lv, text="If Lively Wallpaper is installed, launch it for video/animated wallpapers.", text_color="gray").pack(anchor="w", padx=16)
    ctk.CTkButton(lv, text="Launch Lively Wallpaper", command=lambda: subprocess.Popen("livelywpf", shell=True)).pack(anchor="w", padx=16, pady=6)

    # Modding: apply theme accent
    md = ctk.CTkFrame(frame, corner_radius=12)
    md.pack(fill="x", pady=6)
    ctk.CTkLabel(md, text="Modding: Accent Color", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    color = ctk.CTkEntry(md, placeholder_text="Hex color e.g. #0078D7")
    color.pack(anchor="w", padx=16, pady=4)
    def apply_accent():
        import winreg
        c = color.get().strip().lstrip("#")
        if len(c) == 6:
            val = int(c, 16)
            # store as ABGR
            b = int(c[4:6],16); g = int(c[2:4],16); r = int(c[0:2],16)
            abgr = (b<<16)|(g<<8)|r
            winreg.SetValueEx(winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Accent"), "AccentColorMenu", 0, winreg.REG_DWORD, 0xFF000000 | abgr)
    ctk.CTkButton(md, text="Apply Accent", command=apply_accent).pack(anchor="w", padx=16, pady=6)

    return frame
