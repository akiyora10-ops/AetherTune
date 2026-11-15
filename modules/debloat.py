import customtkinter as ctk
from .utils import run_ps

BLOAT = [
    "Microsoft.3DBuilder", "Microsoft.BingWeather", "Microsoft.GetHelp", "Microsoft.Getstarted",
    "Microsoft.Microsoft3DViewer", "Microsoft.MicrosoftOfficeHub", "Microsoft.MicrosoftSolitaireCollection",
    "Microsoft.MixedReality.Portal", "Microsoft.People", "Microsoft.SkypeApp", "Microsoft.Wallet",
    "Microsoft.WindowsAlarms", "Microsoft.WindowsCamera", "microsoft.windowscommunicationsapps",
    "Microsoft.WindowsFeedbackHub", "Microsoft.WindowsMaps", "Microsoft.WindowsSoundRecorder",
    "Microsoft.Xbox.TCUI", "Microsoft.XboxApp", "Microsoft.XboxGameOverlay", "Microsoft.XboxGamingOverlay",
    "Microsoft.XboxIdentityProvider", "Microsoft.XboxSpeechToTextOverlay", "Microsoft.YourPhone",
    "Microsoft.ZuneMusic", "Microsoft.ZuneVideo", "Microsoft.549981C3F5F10",  # Cortana
]

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(frame, text="Debloat (Remove UWP Apps)", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0,12))
    if not __import__("modules.utils", fromlist=["is_admin"]).is_admin():
        ctk.CTkLabel(frame, text="Run as Administrator for removal.", text_color="orange").pack(anchor="w", pady=4)

    scroll = ctk.CTkScrollableFrame(frame, height=420)
    scroll.pack(fill="both", expand=True, pady=6)
    selected = {}
    for app in BLOAT:
        var = ctk.BooleanVar(value=False)
        selected[app] = var
        ctk.CTkCheckBox(scroll, text=app, variable=var).pack(anchor="w", padx=8, pady=2)

    status = ctk.CTkLabel(frame, text="", text_color="gray")
    status.pack(anchor="w", pady=4)

    def remove_selected():
        to_remove = [a for a, v in selected.items() if v.get()]
        if not to_remove:
            status.configure(text="Nothing selected.")
            return
        status.configure(text="Removing...")
        frame.update()
        for a in to_remove:
            run_ps(f"Get-AppxPackage -Name '{a}' | Remove-AppxPackage -ErrorAction SilentlyContinue")
            run_ps(f"Get-AppxProvisionedPackage -Online | Where-Object {{$_.PackageName -like '*{a}*'}} | Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue")
        status.configure(text=f"Removed {len(to_remove)} apps (best effort).")

    ctk.CTkButton(frame, text="Remove Selected", command=remove_selected).pack(anchor="w", pady=6)
    ctk.CTkButton(frame, text="Select All Bloat", command=lambda: [v.set(True) for v in selected.values()]).pack(anchor="w", pady=2)
    return frame
