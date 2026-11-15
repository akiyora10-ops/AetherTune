import customtkinter as ctk, json, os
from .utils import run_ps

PROF = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'profiles.json')

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color='transparent')
    ctk.CTkLabel(frame, text='Game Profiles', font=ctk.CTkFont(size=24, weight='bold')).pack(anchor='w', pady=(0,12))
    ctk.CTkLabel(frame, text='Save/load named performance profiles.', text_color='gray').pack(anchor='w', pady=4)
    entry = ctk.CTkEntry(frame, placeholder_text='Profile name')
    entry.pack(anchor='w', pady=4)
    def save():
        data = {}
        if os.path.exists(PROF):
            data = json.load(open(PROF))
        data[entry.get()] = {'created': True}
        json.dump(data, open(PROF,'w'), indent=2)
    ctk.CTkButton(frame, text='Save Profile', command=save).pack(anchor='w', pady=4)
    return frame
