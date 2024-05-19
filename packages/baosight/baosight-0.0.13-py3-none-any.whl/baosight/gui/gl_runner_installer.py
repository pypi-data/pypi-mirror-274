import threading
from tkinter import filedialog, ttk, scrolledtext

import tkinter as tk


def center_window(root):
    """ 将窗口居中放置在屏幕上 """
    root.update_idletasks()  # 更新窗口状态
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def create_installation_ui(deploy):
    root = tk.Tk()
    root.title("Gitlab Runner Installer")

    # 添加文件选择按钮
    config_button = tk.Button(
        root,
        text="选择配置文件",
        command=lambda: filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    )

    progress_bar = ttk.Progressbar(root, orient='horizontal', length=500, mode='determinate', maximum=100)
    progress_bar.pack(pady=20)
    progress_bar.pack(padx=10)
    text_area = tk.Text(root, height=20, bg='black', fg='white', insertbackground='white')
    text_area.pack(fill='both', expand=True)
    start_button = tk.Button(
        root,
        text="开始安装",
        command=lambda: threading.Thread(
            target=deploy,
            kwargs={
                "gui_objs": {
                    "config_button": config_button,
                    "progress_bar": progress_bar,
                    "root": root,
                    "start_button": start_button,
                    "text_area": text_area
                }

            }
        ).start()
    )
    start_button.pack(pady=20)
    center_window(root)
    root.mainloop()
