import customtkinter as ctk, urllib.request, json

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color='transparent')
    ctk.CTkLabel(frame, text='Updater', font=ctk.CTkFont(size=24, weight='bold')).pack(anchor='w', pady=(0,12))
    status = ctk.CTkLabel(frame, text='Check GitHub for updates.', text_color='gray')
    status.pack(anchor='w', pady=4)
    def check():
        try:
            status.configure(text='Latest: see GitHub releases')
        except Exception as e:
            status.configure(text=str(e))
    ctk.CTkButton(frame, text='Check Updates', command=check).pack(anchor='w', pady=4)
    return frame
