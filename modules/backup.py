import shutil, os, datetime

def backup_file(src):
    dst = src + '.bak.' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    shutil.copy2(src, dst)
    return dst
