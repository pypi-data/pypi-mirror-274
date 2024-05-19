import ctypes
import sys

import tkinter as tk


def show_message(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x1000 | 0x40)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin(argv=None):
    if argv is None and sys.argv:
        argv = sys.argv
    if hasattr(sys, '_MEIPASS'):
        arguments = map(str, argv[1:])
    else:
        arguments = map(str, argv)
    cmd = ' '.join(arguments)
    # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, cmd, None, 0)
    show_message("错误", "请以管理员身份运行.")
    sys.exit()


def insert_tk_text(text_area, text):
    if not text_area:
        return
    text_area.insert(tk.END, text)
    text_area.see(tk.END)  # 确保滚动到最新插入的文本处
