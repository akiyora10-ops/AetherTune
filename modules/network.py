import customtkinter as ctk
from .utils import run_ps

def build(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(frame, text="Network", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0,12))

    card = ctk.CTkFrame(frame, corner_radius=12)
    card.pack(fill="x", pady=6)
    ctk.CTkLabel(card, text="Network Tweaks", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    for t, cmd in [
        ("Flush DNS", "ipconfig /flushdns"),
        ("Reset Winsock", "netsh winsock reset"),
        ("Reset TCP/IP", "netsh int ip reset"),
        ("Release/Renew IP", "ipconfig /release; ipconfig /renew"),
    ]:
        ctk.CTkButton(card, text=t, command=lambda c=cmd: run_ps(c)).pack(anchor="w", padx=16, pady=4)

    # TCP optimizer
    tcp = ctk.CTkFrame(frame, corner_radius=12)
    tcp.pack(fill="x", pady=6)
    ctk.CTkLabel(tcp, text="TCP Optimizer (registry)", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(12,6))
    from .utils import reg_set
    def apply_tcp():
        reg_set(r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "TcpAckFrequency", 1)
        reg_set(r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "TCPNoDelay", 1)
        reg_set(r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "TcpDelAckTicks", 0)
    ctk.CTkButton(tcp, text="Apply Low-Latency TCP", command=apply_tcp).pack(anchor="w", padx=16, pady=6)
    ctk.CTkLabel(tcp, text="Best for gaming; may not help on all networks.", text_color="gray").pack(anchor="w", padx=16, pady=4)

    return frame
