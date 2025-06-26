import tkinter as tk
from tkinter import ttk, messagebox
from core.config import Config
from models.user import User

class MainMenu:
    """主菜单界面"""
    def __init__(self, master, user, config=None):
        self.master = master
        self.master.title("停车管理系统")
        self.master.geometry("600x400")
        
        # 系统配置
        self.config = config or Config()
        self.user = user
        
        # 主框架
        main_frame = tk.Frame(master, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # 标题
        title_label = tk.Label(
            main_frame, 
            text="欢迎使用智能停车管理系统", 
            font=("微软雅黑", 20, "bold"),
            pady=20
        )
        title_label.pack(fill=tk.X)
        
        # 用户信息
        user_frame = tk.Frame(main_frame)
        user_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(user_frame, text=f"当前用户: {user.username}").pack(side=tk.LEFT)
        tk.Label(user_frame, text=f"角色: {user.role}").pack(side=tk.RIGHT)
        
        # 系统选择区域
        system_frame = tk.LabelFrame(main_frame, text="选择系统模式", padx=10, pady=10)
        system_frame.pack(fill=tk.X, pady=20)
        
        # 系统模式选择按钮
        btn_frame = tk.Frame(system_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(
            btn_frame, 
            text="单门系统", 
            command=lambda: self.start_parking_system(single_exit=True),
            width=15,
            height=2,
            font=("微软雅黑", 12),
            bg="#4CAF50",
            fg="white"
        ).pack(side=tk.LEFT, padx=10, expand=True)
        
        tk.Button(
            btn_frame, 
            text="双门系统", 
            command=lambda: self.start_parking_system(single_exit=False),
            width=15,
            height=2,
            font=("微软雅黑", 12),
            bg="#2196F3",
            fg="white"
        ).pack(side=tk.RIGHT, padx=10, expand=True)
        
        # 分隔线
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # 其他功能按钮
        other_frame = tk.Frame(main_frame)
        other_frame.pack(fill=tk.X, pady=10)
        
        if user.role == "admin":
            tk.Button(
                other_frame, 
                text="系统设置", 
                command=self.open_settings,
                width=15
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Button(
                other_frame, 
                text="用户管理", 
                command=self.user_management,
                width=15
            ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            other_frame, 
            text="退出系统", 
            command=self.master.quit,
            width=15
        ).pack(side=tk.RIGHT, padx=5)
        
        # 状态栏
        status_bar = tk.Label(main_frame, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 居中窗口
        self.center_window()
    
    def center_window(self):
        """居中窗口"""
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")
    
    def start_parking_system(self, single_exit=True):
        """启动停车管理系统"""
        # 设置系统模式
        self.config.enable_dual_exit = not single_exit
        
        # 创建停车管理系统窗口
        from ui.parking_ui import ParkingUI
        
        # 隐藏主菜单
        self.master.withdraw()
        
        # 创建新窗口
        parking_window = tk.Toplevel(self.master)
        parking_window.protocol("WM_DELETE_WINDOW", lambda: self.on_parking_close(parking_window))
        
        # 启动停车管理系统
        ParkingUI(parking_window, self.config, self.user)
    
    def on_parking_close(self, window):
        """停车管理系统关闭时的回调"""
        window.destroy()
        self.master.deiconify()  # 重新显示主菜单
    
    def open_settings(self):
        """打开系统设置"""
        # 这里实现系统设置界面
        messagebox.showinfo("系统设置", "系统设置功能开发中")
    
    def user_management(self):
        """用户管理"""
        # 这里实现用户管理界面
        messagebox.showinfo("用户管理", "用户管理功能开发中")