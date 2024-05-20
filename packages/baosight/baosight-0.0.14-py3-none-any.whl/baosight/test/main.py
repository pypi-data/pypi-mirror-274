import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading


def run_command():
    """ 运行命令行命令，并将输出实时显示在 Text 控件中。"""
    # 示例命令，这里应替换为需要执行的实际命令
    cmd = ['ping', 'www.google.com', '-n', '5']

    # 启动子进程执行命令
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 实时读取输出
    for line in process.stdout:
        text_area.insert(tk.END, line)
        text_area.see(tk.END)  # 自动滚动到底部
        root.update_idletasks()  # 更新GUI

    # 等待命令执行结束
    process.wait()

    # 将结束信息或错误信息输出到文本区域
    if process.returncode == 0:
        text_area.insert(tk.END, "\n命令执行完成！\n")
    else:
        error = process.stderr.read()
        text_area.insert(tk.END, f"\n发生错误：\n{error}")
    text_area.see(tk.END)
    root.update_idletasks()


def start_thread():
    """ 在新线程中运行命令，避免阻塞 GUI。"""
    threading.Thread(target=run_command).start()


# 创建主窗口
root = tk.Tk()
root.title("安装界面")

# 创建滚动文本区域用于显示输出，设置背景为黑色，前景（文字）为白色
text_area = scrolledtext.ScrolledText(root, width=80, height=20, bg='black', fg='white', insertbackground='white')
text_area.grid(column=0, row=0, padx=10, pady=10)

# 创建启动命令的按钮
start_button = tk.Button(root, text="开始安装", command=start_thread)
start_button.grid(column=0, row=1, padx=10, pady=10)

# 启动主事件循环
root.mainloop()
