import tkinter as tk
from tkinter import messagebox
from .main_menu import MainMenu

class SettingsUI:
    def __init__(self, master, config, user):
        self.master = master
        self.config = config
        self.user = user
        self.master.title("系统设置")
        self.master.geometry("500x500")
        
        # 主框架
        main_frame = tk.Frame(master, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 容量设置
        capacity_frame = tk.LabelFrame(main_frame, text="容量设置")
        capacity_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(capacity_frame, text="停车场容量:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.parking_entry = tk.Entry(capacity_frame)
        self.parking_entry.grid(row=0, column=1, padx=5, pady=5)
        self.parking_entry.insert(0, str(config.parking_capacity))
        
        tk.Label(capacity_frame, text="便道容量:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.waiting_entry = tk.Entry(capacity_frame)
        self.waiting_entry.grid(row=1, column=1, padx=5, pady=5)
        self.waiting_entry.insert(0, str(config.waiting_capacity))
        
        # 计费设置
        billing_frame = tk.LabelFrame(main_frame, text="计费设置")
        billing_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(billing_frame, text="计费模式:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.billing_var = tk.StringVar(value=config.billing_mode)
        billing_options = ["per_minute", "per_hour", "fixed"]
        billing_menu = tk.OptionMenu(billing_frame, self.billing_var, *billing_options)
        billing_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(billing_frame, text="费率/固定费用:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.rate_entry = tk.Entry(billing_frame)
        self.rate_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # 根据当前计费模式设置默认值
        if config.billing_mode == "per_minute":
            self.rate_entry.insert(0, str(config.fee_per_minute))
        elif config.billing_mode == "per_hour":
            self.rate_entry.insert(0, str(config.fee_per_hour))
        else:
            self.rate_entry.insert(0, str(config.fixed_fee))
        
        # 双门系统设置（仅管理员可见）
        if user.role == "admin":
            dual_frame = tk.LabelFrame(main_frame, text="双门系统设置")
            dual_frame.pack(fill=tk.X, pady=10)
            
            self.dual_var = tk.BooleanVar(value=config.enable_dual_exit)
            tk.Checkbutton(dual_frame, text="启用双门系统", 
                          variable=self.dual_var).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
            
            tk.Label(dual_frame, text="北出口便道容量:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.north_entry = tk.Entry(dual_frame)
            self.north_entry.grid(row=1, column=1, padx=5, pady=5)
            self.north_entry.insert(0, str(config.dual_exit_settings["north_waiting_capacity"]))
            
            tk.Label(dual_frame, text="南出口便道容量:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.south_entry = tk.Entry(dual_frame)
            self.south_entry.grid(row=2, column=1, padx=5, pady=5)
            self.south_entry.insert(0, str(config.dual_exit_settings["south_waiting_capacity"]))
            
            tk.Label(dual_frame, text="优化触发阈值:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
            self.threshold_entry = tk.Entry(dual_frame)
            self.threshold_entry.grid(row=3, column=1, padx=5, pady=5)
            self.threshold_entry.insert(0, str(config.dual_exit_settings["optimization_threshold"]))
        
        # 按钮区域
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="保存设置", 
                 command=self.save_settings).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="返回主菜单", 
                 command=self.return_main).pack(side=tk.RIGHT, padx=5)
    
    def save_settings(self):
        """保存系统设置"""
        try:
            # 保存容量设置
            self.config.parking_capacity = int(self.parking_entry.get())
            self.config.waiting_capacity = int(self.waiting_entry.get())
            
            # 保存计费设置
            billing_mode = self.billing_var.get()
            self.config.billing_mode = billing_mode
            
            rate = float(self.rate_entry.get())
            if billing_mode == "per_minute":
                self.config.fee_per_minute = rate
            elif billing_mode == "per_hour":
                self.config.fee_per_hour = rate
            else:
                self.config.fixed_fee = rate
            
            # 保存双门系统设置（如果可见）
            if hasattr(self, 'dual_var'):
                self.config.enable_dual_exit = self.dual_var.get()
                
                # 更新双门系统设置
                self.config.dual_exit_settings = {
                    "north_waiting_capacity": int(self.north_entry.get()),
                    "south_waiting_capacity": int(self.south_entry.get()),
                    "optimization_threshold": float(self.threshold_entry.get())
                }
            
            messagebox.showinfo("成功", "系统设置已保存")
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
    
    def return_main(self):
        """返回主菜单"""
        self.master.destroy()