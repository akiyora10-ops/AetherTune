import customtkinter as ctk
import psutil, threading, time
from .utils import run_ps, get_gpu_names, get_temps

class Monitor(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.running = True
        ctk.CTkLabel(self, text="Live Monitor", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0,12))

        self.gridf = ctk.CTkFrame(self, fg_color="transparent")
        self.gridf.pack(fill="both", expand=True)
        self.gridf.grid_columnconfigure((0,1), weight=1)

        self.cards = {}
        items = ["CPU %", "RAM %", "GPU %", "VRAM", "Temp (C)", "Disk R/W", "Net Up/Down", "Battery"]
        for i, name in enumerate(items):
            card = ctk.CTkFrame(self.gridf, corner_radius=12)
            card.grid(row=i//2, column=i%2, padx=6, pady=6, sticky="nsew")
            ctk.CTkLabel(card, text=name, font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=14, pady=(10,2))
            val = ctk.CTkLabel(card, text="--", font=ctk.CTkFont(size=26, weight="bold"))
            val.pack(anchor="w", padx=14, pady=(0,12))
            self.cards[name] = val

        self.log = ctk.CTkTextbox(self, height=140)
        self.log.pack(fill="x", pady=8)
        threading.Thread(target=self.loop, daemon=True).start()

    def loop(self):
        net_prev = psutil.net_io_counters()
        disk_prev = psutil.disk_io_counters()
        t_prev = time.time()
        while self.running:
            try:
                cpu = psutil.cpu_percent(interval=None)
                ram = psutil.virtual_memory().percent
                # gpu via wmi (AMD/NVIDIA) - utilization not always available; use load via counter
                gpu_pct = _gpu_util()
                vram = _vram()
                temps = get_temps()
                tempstr = ", ".join(str(t) for t in temps) if temps else "n/a"
                now = time.time()
                dt = now - t_prev
                net = psutil.net_io_counters()
                disk = psutil.disk_io_counters()
                up = (net.bytes_sent - net_prev.bytes_sent)/dt/1024 if dt>0 else 0
                down = (net.bytes_recv - net_prev.bytes_recv)/dt/1024 if dt>0 else 0
                dr = (disk.read_bytes - disk_prev.read_bytes)/dt/1024 if dt>0 else 0
                dw = (disk.write_bytes - disk_prev.write_bytes)/dt/1024 if dt>0 else 0
                net_prev, disk_prev, t_prev = net, disk, now
                bat = psutil.sensors_battery()
                batstr = f"{bat.percent}% {'AC' if bat and bat.power_plugged else 'BAT'}" if bat else "n/a"

                def upd():
                    self.cards["CPU %"].configure(text=f"{cpu:.1f}%")
                    self.cards["RAM %"].configure(text=f"{ram:.1f}%")
                    self.cards["GPU %"].configure(text=f"{gpu_pct}")
                    self.cards["VRAM"].configure(text=f"{vram}")
                    self.cards["Temp (C)"].configure(text=tempstr)
                    self.cards["Disk R/W"].configure(text=f"R {dr:.0f} / W {dw:.0f} KB/s")
                    self.cards["Net Up/Down"].configure(text=f"Up {up:.0f} / Dn {down:.0f} KB/s")
                    self.cards["Battery"].configure(text=batstr)
                self.after(0, upd)
            except Exception as e:
                pass
            time.sleep(1.5)

    def destroy(self):
        self.running = False
        super().destroy()

def _gpu_util():
    out, _ = run_ps("(Get-Counter '\\GPU Engine(*)\\Utilization Percentage' -ErrorAction SilentlyContinue).CounterSamples | Measure-Object -Property CookedValue -Sum | Select-Object -ExpandProperty Sum")
    try:
        return f"{float(out):.1f}%"
    except Exception:
        return "n/a"

def _vram():
    out, _ = run_ps("Get-CimInstance Win32_VideoController | Select-Object -First 1 -ExpandProperty AdapterRAM")
    try:
        return f"{int(out)/1e9:.1f} GB"
    except Exception:
        return "n/a"

def build(parent):
    return Monitor(parent)
