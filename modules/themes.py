import customtkinter as ctk

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color='transparent')
    ctk.CTkLabel(frame, text='Themes', font=ctk.CTkFont(size=24, weight='bold')).pack(anchor='w', pady=(0,12))
    for mode in ['dark', 'light', 'system']:
        ctk.CTkButton(frame, text=mode.title(), command=lambda m=mode: ctk.set_appearance_mode(m)).pack(anchor='w', pady=4)
    return frame
