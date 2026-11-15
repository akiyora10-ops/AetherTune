import psutil

def top_processes(n=5):
    return sorted(psutil.process_iter(['name','memory_info']), key=lambda p: p.info['memory_info'].rss, reverse=True)[:n]
