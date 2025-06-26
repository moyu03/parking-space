# ui/login.py

import tkinter as tk
from tkinter import messagebox
from .main_menu import MainMenu
from models.user import User
from core.config import Config
from utils.window_utils import center_window

class LoginUI:
    def __init__(self, master):
        self.master = master
        self.master.title("登录")
        self.master.geometry("300x200")

        tk.Label(master, text="用户名:").pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        tk.Label(master, text="角色:").pack()
        self.role_var = tk.StringVar(value="user")
        tk.OptionMenu(master, self.role_var, "user", "admin").pack()

        tk.Button(master, text="登录", command=self.login).pack(pady=10)
        center_window(self.master, 300, 200)

    def login(self):
        username = self.username_entry.get().strip()
        role = self.role_var.get()
        if not username:
            messagebox.showwarning("错误", "请输入用户名")
            return
        user = User(username=username, role=role)
        config = Config()
        self.master.destroy()
        root = tk.Tk()
        MainMenu(root, user, config)
        root.mainloop()