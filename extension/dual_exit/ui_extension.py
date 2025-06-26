import tkinter as tk
import time
from tkinter import ttk
from utils.time_utils import timestamp_to_str, format_duration

class DualExitParkingUI:
    def __init__(self, master, parking_system, log_text):
        self.master = master
        self.parking_system = parking_system
        self.log_text = log_text  # 主界面的日志控件
        
        # 主框架 - 使用表格布局实现对称
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 配置网格权重确保均匀分布
        main_frame.grid_rowconfigure(0, weight=1)  # 第一行（停车场）可扩展
        main_frame.grid_rowconfigure(1, weight=1)  # 第二行（便道）可扩展
        main_frame.grid_columnconfigure(0, weight=1)  # 左列可扩展
        main_frame.grid_columnconfigure(1, weight=1)  # 右列可扩展
        
        # 北停车场状态
        north_frame = tk.LabelFrame(main_frame, text="北停车场", font=("Arial", 10, "bold"))
        north_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # 添加北停车场滚动条
        north_scroll = tk.Scrollbar(north_frame)
        north_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.north_text = tk.Text(north_frame, height=15, yscrollcommand=north_scroll.set)
        self.north_text.pack(fill=tk.BOTH, expand=True)
        north_scroll.config(command=self.north_text.yview)
        
        # 南停车场状态
        south_frame = tk.LabelFrame(main_frame, text="南停车场", font=("Arial", 10, "bold"))
        south_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        # 添加南停车场滚动条
        south_scroll = tk.Scrollbar(south_frame)
        south_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.south_text = tk.Text(south_frame, height=15, yscrollcommand=south_scroll.set)
        self.south_text.pack(fill=tk.BOTH, expand=True)
        south_scroll.config(command=self.south_text.yview)
        
        # 北便道状态
        north_waiting_frame = tk.LabelFrame(main_frame, text="北便道", font=("Arial", 10))
        north_waiting_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        # 添加北便道滚动条
        north_waiting_scroll = tk.Scrollbar(north_waiting_frame)
        north_waiting_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.north_waiting_text = tk.Text(north_waiting_frame, height=5, yscrollcommand=north_waiting_scroll.set)
        self.north_waiting_text.pack(fill=tk.BOTH, expand=True)
        north_waiting_scroll.config(command=self.north_waiting_text.yview)
        
        # 南便道状态
        south_waiting_frame = tk.LabelFrame(main_frame, text="南便道", font=("Arial", 10))
        south_waiting_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        # 添加南便道滚动条
        south_waiting_scroll = tk.Scrollbar(south_waiting_frame)
        south_waiting_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.south_waiting_text = tk.Text(south_waiting_frame, height=5, yscrollcommand=south_waiting_scroll.set)
        self.south_waiting_text.pack(fill=tk.BOTH, expand=True)
        south_waiting_scroll.config(command=self.south_waiting_text.yview)
        
        # 添加控制按钮
        control_frame = tk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        tk.Button(control_frame, text="刷新状态", command=self.refresh_status).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="优化系统", command=self.optimize_system).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="查看便道", command=self.show_waiting_lane).pack(side=tk.LEFT, padx=5)
        
        # 初始状态
        self.refresh_status()
    
    def log(self, message, level="info"):
        """在日志区域添加消息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n", level)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def refresh_status(self):
        """刷新停车场状态显示"""
        try:
            status = self.parking_system.get_status()
            parking_status = status["parking"]
            waiting_status = status["waiting"]
            current_time = time.time()
            
            # 更新北端显示
            self.update_parking_display(
                self.north_text, 
                "北停车场状态:\n\n",
                parking_status["north"],
                current_time
            )
            self.north_text.insert(tk.END, f"\n占用: {len(parking_status['north'])}/{parking_status['capacity']//2}")
            
            # 更新南端显示
            self.update_parking_display(
                self.south_text, 
                "南停车场状态:\n\n",
                parking_status["south"],
                current_time
            )
            self.south_text.insert(tk.END, f"\n占用: {len(parking_status['south'])}/{parking_status['capacity']//2}")
            
            # 更新便道显示
            self.update_waiting_display(
                self.north_waiting_text,
                "北便道等待车辆:\n\n",
                waiting_status["north"],
                current_time
            )
            
            self.update_waiting_display(
                self.south_waiting_text,
                "南便道等待车辆:\n\n",
                waiting_status["south"],
                current_time
            )
            
        except Exception as e:
            self.log(f"刷新状态失败: {str(e)}", "error")
    
    def update_parking_display(self, text_widget, title, parking_data, current_time):
        """更新停车场显示"""
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, title)
        
        if parking_data:
            for spot in parking_data:
                duration = current_time - spot["entry_time"]
                text_widget.insert(tk.END, 
                    f"{spot['position']}: {spot['car'].car_id} "
                    f"(已停 {format_duration(duration)})\n")
        else:
            text_widget.insert(tk.END, "（空）\n")
        
        text_widget.config(state=tk.DISABLED)
    
    def update_waiting_display(self, text_widget, title, waiting_data, current_time):
        """更新便道显示"""
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, title)
        
        if waiting_data:
            for idx, item in enumerate(waiting_data):
                wait_time = current_time - item["arrival_time"]
                text_widget.insert(tk.END, 
                    f"{idx+1}. {item['car'].car_id} "
                    f"(等待 {format_duration(wait_time)})\n")
        else:
            text_widget.insert(tk.END, "（空）\n")
        
        text_widget.config(state=tk.DISABLED)
    
    def optimize_system(self):
        """执行系统优化并显示结果"""
        try:
            success, message = self.parking_system.optimize_system()
            if success:
                self.refresh_status()
                self.log(f"系统优化: {message}", "info")
                tk.messagebox.showinfo("系统优化", message)
            else:
                self.log(f"系统优化: {message}", "info")
                tk.messagebox.showinfo("系统优化", message)
        except Exception as e:
            self.log(f"系统优化失败: {str(e)}", "error")
    
    def show_waiting_lane(self):
        """显示便道状态窗口"""
        try:
            lane_win = tk.Toplevel(self.master)
            lane_win.title("便道状态详情")
            lane_win.geometry("500x400")
            
            status = self.parking_system.get_status()["waiting"]
            current_time = time.time()
            
            # 北便道
            north_frame = tk.LabelFrame(lane_win, text="北便道")
            north_frame.pack(fill=tk.X, padx=10, pady=5)
            
            north_text = tk.Text(north_frame, height=5)
            north_text.pack(fill=tk.X, padx=5, pady=5)
            north_text.insert(tk.END, f"等待车辆: {len(status['north'])}\n\n")
            
            for idx, item in enumerate(status["north"]):
                wait_time = current_time - item["arrival_time"]
                north_text.insert(tk.END, 
                    f"{idx+1}. {item['car'].car_id} "
                    f"(等待 {format_duration(wait_time)})\n")
            north_text.config(state=tk.DISABLED)
            
            # 南便道
            south_frame = tk.LabelFrame(lane_win, text="南便道")
            south_frame.pack(fill=tk.X, padx=10, pady=5)
            
            south_text = tk.Text(south_frame, height=5)
            south_text.pack(fill=tk.X, padx=5, pady=5)
            south_text.insert(tk.END, f"等待车辆: {len(status['south'])}\n\n")
            
            for idx, item in enumerate(status["south"]):
                wait_time = current_time - item["arrival_time"]
                south_text.insert(tk.END, 
                    f"{idx+1}. {item['car'].car_id} "
                    f"(等待 {format_duration(wait_time)})\n")
            south_text.config(state=tk.DISABLED)
            
            # 统计信息
            stats_frame = tk.Frame(lane_win)
            stats_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(stats_frame, text=f"总等待车辆: {len(status['north']) + len(status['south'])}").pack(anchor="w")
            
        except Exception as e:
            self.log(f"显示便道状态失败: {str(e)}", "error")