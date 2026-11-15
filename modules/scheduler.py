import threading, time

def every(seconds, func):
    def loop():
        while True:
            func()
            time.sleep(seconds)
    threading.Thread(target=loop, daemon=True).start()
