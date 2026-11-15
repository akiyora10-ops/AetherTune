import customtkinter as ctk
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules import dashboard, monitor, gpu, registry, performance, startup, cleaner, wallpaper, network, settings, debloat

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

APP_NAME = "AetherTune"
APP_VERSION = "0.1.0"

class AetherTune(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{APP_VERSION} - AMD Laptop Tuning Suite")
        self.geometry("1280x820")
        self.minsize(1080, 700)

        # grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # sidebar
        self.sidebar = ctk.CTkFrame(self, width=210, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(20, weight=1)

        logo = ctk.CTkLabel(self.sidebar, text=APP_NAME, font=ctk.CTkFont(size=22, weight="bold"))
        logo.grid(row=0, column=0, padx=20, pady=(20, 4))
        sub = ctk.CTkLabel(self.sidebar, text="AMD Laptop Suite", font=ctk.CTkFont(size=11), text_color="gray")
        sub.grid(row=1, column=0, padx=20, pady=(0, 16))

        self.nav_buttons = {}
        nav = [
            ("Dashboard", dashboard.build),
            ("Monitor", monitor.build),
            ("GPU Tweaks", gpu.build),
            ("Registry", registry.build),
            ("Performance", performance.build),
            ("Startup", startup.build),
            ("Cleaner", cleaner.build),
            ("Wallpaper", wallpaper.build),
            ("Network", network.build),
            ("Debloat", debloat.build),
            ("Settings", settings.build),
        ]
        r = 2
        for name, builder in nav:
            btn = ctk.CTkButton(self.sidebar, text=name, height=36, corner_radius=8,
                                fg_color="transparent", hover_color="#1f2937",
                                anchor="w", command=lambda n=name, b=builder: self.show(n, b))
            btn.grid(row=r, column=0, padx=12, pady=3, sticky="ew")
            self.nav_buttons[name] = btn
            r += 1

        # content area
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="#0b0f19")
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.current = None
        self.show("Dashboard", dashboard.build)

    def show(self, name, builder):
        if self.current is not None:
            self.current.destroy()
        self.current = builder(self.content)
        self.current.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        for n, b in self.nav_buttons.items():
            b.configure(fg_color="#1f2937" if n == name else "transparent")

if __name__ == "__main__":
    app = AetherTune()
    app.mainloop()
