import customtkinter as ctk
import winreg, json, os
from .utils import reg_set, reg_get, reg_delete, is_admin

BACKUP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "registry_backup.json")

TWEAKS = [
    # (name, category, path, value_name, value, kind, description)
    ("Disable Windows Tips/Ads", "Privacy", r"HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager", "SubscribedContent-338389Enabled", 0, "dword", "Stops suggested apps/tips in Start."),
    ("Disable Telemetry (AllowTelemetry)", "Privacy", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry", 0, "dword", "Limits diagnostic data."),
    ("Disable Activity History", "Privacy", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\System", "EnableActivityFeed", 0, "dword", "Disables timeline/activity feed."),
    ("Disable Cortana", "Privacy", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search", "AllowCortana", 0, "dword", "Disables Cortana."),
    ("Disable Web Search in Start", "Privacy", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Search", "BingSearchEnabled", 0, "dword", "No web results in Start search."),
    ("Disable Game DVR", "Gaming", r"HKCU\System\GameConfigStore", "GameDVR_Enabled", 0, "dword", "Disables Game DVR capture."),
    ("Enable Game Mode", "Gaming", r"HKCU\Software\Microsoft\GameBar", "AutoGameModeEnabled", 1, "dword", "Auto enables Game Mode."),
    ("Disable Fullscreen Optimizations (global)", "Gaming", r"HKCU\System\GameConfigStore", "GameDVR_FSEBehaviorMode", 2, "dword", "Reduces FSO overhead."),
    ("Ultimate Performance Power (unlock)", "Performance", r"HKLM\SYSTEM\CurrentControlSet\Control\Power", "CsEnabled", 0, "dword", "Disables connected standby (laptops careful)."),
    ("Disable Prefetch (SSD)", "Performance", r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters", "EnablePrefetcher", 0, "dword", "Disables prefetch on SSD systems."),
    ("Disable Superfetch/SysMain (already)", "Performance", r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters", "EnableSuperfetch", 0, "dword", "Disables superfetch."),
    ("Increase Network Throttling", "Network", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "NetworkThrottlingIndex", 0xFFFFFFFF, "dword", "Removes network throttling."),
    ("Set System Responsiveness 10", "Performance", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "SystemResponsiveness", 10, "dword", "Prioritizes foreground apps."),
    ("Disable Animations", "UI", r"HKCU\Control Panel\Desktop", "UserPreferencesMask", None, "anim", "Disables window animations."),
    ("Show File Extensions", "UI", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "HideFileExt", 0, "dword", "Shows file extensions."),
    ("Disable Lock Screen", "UI", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Personalization", "NoLockScreen", 1, "dword", "Skips lock screen."),
    ("Disable Sticky Keys Prompt", "UI", r"HKCU\Control Panel\Accessibility\StickyKeys", "Flags", "506", "str", "Disables sticky keys prompt."),
    ("Enable Dark Mode", "UI", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "AppsUseLightTheme", 0, "dword", "Dark mode for apps."),
    ("Disable Background Apps", "Performance", r"HKCU\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications", "GlobalUserDisabled", 1, "dword", "Stops background apps."),
    ("Disable Windows Defender (not recommended)", "Security", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "DisableAntiSpyware", 1, "dword", "Disables Defender (risky)."),
]

class RegistryTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Registry Tweaks", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0,12))
        if not is_admin():
            ctk.CTkLabel(self, text="Run as Administrator for HKLM tweaks.", text_color="orange").pack(anchor="w", pady=4)

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", pady=6)
        ctk.CTkButton(toolbar, text="Backup Registry (export HKCU/HKLM relevant)", command=self.backup).pack(side="left", padx=4)
        ctk.CTkButton(toolbar, text="Restore Backup", command=self.restore).pack(side="left", padx=4)
        ctk.CTkButton(toolbar, text="Create System Restore Point", command=self.restore_point).pack(side="left", padx=4)

        self.scroll = ctk.CTkScrollableFrame(self, height=520)
        self.scroll.pack(fill="both", expand=True, pady=6)

        cats = {}
        for t in TWEAKS:
            cats.setdefault(t[1], []).append(t)

        for cat, items in cats.items():
            ctk.CTkLabel(self.scroll, text=cat, font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", pady=(10,4))
            for t in items:
                self._row(t)

    def _row(self, t):
        name, cat, path, vname, value, kind, desc = t
        r = ctk.CTkFrame(self.scroll, corner_radius=8)
        r.pack(fill="x", pady=3)
        left = ctk.CTkFrame(r, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True, padx=10, pady=6)
        ctk.CTkLabel(left, text=name, font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        ctk.CTkLabel(left, text=desc, text_color="gray", font=ctk.CTkFont(size=11), wraplength=700).pack(anchor="w")
        ctk.CTkLabel(left, text=path + " \\" + vname, text_color="#4b5563", font=ctk.CTkFont(size=10)).pack(anchor="w")

        right = ctk.CTkFrame(r, fg_color="transparent")
        right.pack(side="right", padx=10)
        def apply():
            try:
                if kind == "dword":
                    reg_set(path, vname, int(value))
                elif kind == "str":
                    reg_set(path, vname, str(value), winreg.REG_SZ)
                elif kind == "anim":
                    import winreg as w
                    mask = bytes([0x90,0x12,0x03,0x80,0x10,0x00,0x00,0x00])
                    reg_set(r"HKCU\Control Panel\Desktop", "UserPreferencesMask", mask, w.REG_BINARY)
                    reg_set(r"HKCU\Control Panel\Desktop", "MinAnimate", "0", w.REG_SZ)
                self._toast(f"Applied: {name}")
            except Exception as e:
                self._toast(f"Error: {e}")
        def revert():
            try:
                reg_delete(path, vname)
                self._toast(f"Reverted: {name}")
            except Exception as e:
                self._toast(f"Error: {e}")
        ctk.CTkButton(right, text="Apply", width=70, command=apply).pack(side="left", padx=3)
        ctk.CTkButton(right, text="Revert", width=70, command=revert).pack(side="left", padx=3)

    def _toast(self, msg):
        # simple print + status label
        print(msg)

    def backup(self):
        data = {}
        for t in TWEAKS:
            name, cat, path, vname, value, kind, desc = t
            cur = reg_get(path, vname)
            data[f"{path}\\{vname}"] = cur
        with open(BACKUP, "w") as f:
            json.dump(data, f, indent=2, default=str)
        self._toast(f"Backup saved: {BACKUP}")

    def restore(self):
        if not os.path.exists(BACKUP):
            self._toast("No backup file found.")
            return
        with open(BACKUP) as f:
            data = json.load(f)
        for k, v in data.items():
            if v is None:
                continue
            path, vname = k.rsplit("\\", 1)
            try:
                if isinstance(v, bool):
                    reg_set(path, vname, int(v))
                elif isinstance(v, int):
                    reg_set(path, vname, v)
                else:
                    reg_set(path, vname, str(v), winreg.REG_SZ)
            except Exception as e:
                self._toast(f"Restore err {k}: {e}")
        self._toast("Restore attempted.")

    def restore_point(self):
        rc, out, err = __import__("subprocess").run(
            ["powershell", "-NoProfile", "-Command",
             "Checkpoint-Computer -Description 'AetherTune' -RestorePointType 'MODIFY_SETTINGS'"],
            capture_output=True, text=True)
        self._toast("Restore point requested (requires admin).")

def build(parent):
    return RegistryTab(parent)
