# ui/main_menu.py

import tkinter as tk
from .parking_ui import ParkingUI
from .setting import SettingsUI
from utils.window_utils import center_window

class MainMenu:
    def __init__(self, master, user, config):
        self.master = master
        self.user = user
        self.config = config
        self.master.title(f"主菜单 - 用户: {user.username} ({user.role})")
        self.master.geometry("300x200")

        tk.Label(master, text="欢迎使用停车场管理系统", font=("Arial", 14)).pack(pady=10)

        tk.Button(master, text="进入停车系统", width=25, command=self.enter_parking).pack(pady=5)
        tk.Button(master, text="设置", width=25, command=self.open_settings).pack(pady=5)
        tk.Button(master, text="退出应用", width=25, command=master.quit).pack(pady=5)
        center_window(self.master, 300, 200)

    def enter_parking(self):
        self.master.destroy()
        root = tk.Tk()
        ParkingUI(root, self.config, self.user)
        root.mainloop()

    def open_settings(self):
        if self.user.role != "admin":
            tk.messagebox.showwarning("权限不足", "只有管理员可以访问设置")
            return
        self.master.destroy()
        root = tk.Tk()
        SettingsUI(root, self.config, self.user)
        root.mainloop()
