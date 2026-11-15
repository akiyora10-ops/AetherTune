import customtkinter as ctk
from .utils import run_ps, get_gpu_names

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(frame, text="Fan Control", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0,12))
    ctk.CTkLabel(frame, text="AMD fan control requires ADLX/ADL SDK. Showing current thermal status.", text_color="gray").pack(anchor="w", pady=4)
    for g in get_gpu_names():
        ctk.CTkLabel(frame, text="• " + g).pack(anchor="w", padx=8, pady=2)
    ctk.CTkButton(frame, text="Open AMD Software (fan curves)", command=lambda: run_ps("Start-Process 'amdsoftware'")).pack(anchor="w", pady=8)
    return frame
