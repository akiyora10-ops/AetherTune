import customtkinter as ctk

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color='transparent')
    ctk.CTkLabel(frame, text='Hotkeys', font=ctk.CTkFont(size=24, weight='bold')).pack(anchor='w', pady=(0,12))
    ctk.CTkLabel(frame, text='Global hotkeys coming soon.', text_color='gray').pack(anchor='w', pady=4)
    return frame
