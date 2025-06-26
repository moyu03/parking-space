import tkinter as tk
from tkinter import scrolledtext
from core.parking import Car, ParkingLot, WaitingLane
from core.billing import Billing
from utils.time_utils import timestamp_to_str

class ParkingUI:
    """停车管理界面"""
    def __init__(self, master, config, user):
        self.master = master
        self.config = config
        self.user = user
        self.master.title("停车管理")
        self.master.geometry("900x500")
        
        # 主框架
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 输入区域
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(input_frame, text="车牌号:").pack(side=tk.LEFT)
        self.car_id_entry = tk.Entry(input_frame, width=20)
        self.car_id_entry.pack(side=tk.LEFT, padx=5)
        self.car_id_entry.focus()
        self.car_id_entry.bind("<Return>", lambda event: self.car_arrive())
        
        tk.Button(input_frame, text="车辆进入", command=self.car_arrive).pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="车辆离开", command=self.car_depart).pack(side=tk.LEFT)
        tk.Button(input_frame, text="返回主菜单", command=self.return_main).pack(side=tk.RIGHT)
        
        # 状态区域
        status_frame = tk.Frame(main_frame)
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        # 停车场状态
        status_left = tk.Frame(status_frame)
        status_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(status_left, text="停车场状态", font=("Arial", 10, "bold")).pack(anchor="w")
        self.status_text = tk.Text(status_left, height=12)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # 日志输出
        status_right = tk.Frame(status_frame)
        status_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(status_right, text="操作日志", font=("Arial", 10, "bold")).pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(status_right, height=12)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)  # 设置为只读
        
        # 初始化停车场和便道
        self.parking_lot = ParkingLot(config.parking_capacity)
        self.waiting_lane = WaitingLane(config.waiting_capacity)
        self.billing = Billing(config)
        
        self.refresh_status()
        self.log("停车管理系统已启动", "info")

    def log(self, message, level="info"):
        """在日志区域添加消息"""
        self.log_text.config(state=tk.NORMAL)
        
        # 根据消息级别设置不同颜色
        if level == "error":
            tag = "red"
            self.log_text.tag_config("red", foreground="red")
        elif level == "success":
            tag = "green"
            self.log_text.tag_config("green", foreground="green")
        elif level == "warning":
            tag = "orange"
            self.log_text.tag_config("orange", foreground="orange")
        else:
            tag = "black"
        
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)  # 滚动到底部
        self.log_text.config(state=tk.DISABLED)

    def car_arrive(self):
        """处理车辆进入"""
        car_id = self.car_id_entry.get().strip()
        if not car_id:
            self.log("错误：请输入车牌号", "error")
            return
        
        if self.is_car_exists(car_id):
            self.log(f"错误：车牌号 {car_id} 已存在", "error")
            self.car_id_entry.delete(0, tk.END)
            return
        
        car = Car(car_id)
        if self.parking_lot.arrive(car):
            self.log(f"成功：车辆 {car_id} 停入停车场", "success")
        elif self.waiting_lane.enqueue(car):
            self.log(f"提示：停车场已满，车辆 {car_id} 在便道等待", "info")
        else:
            self.log(f"失败：停车场和便道均满，车辆 {car_id} 无法进入", "warning")
        
        self.car_id_entry.delete(0, tk.END)
        self.refresh_status()

    def car_depart(self):
        """处理车辆离开"""
        car_id = self.car_id_entry.get().strip()
        if not car_id:
            self.log("错误：请输入车牌号", "error")
            return
        
        self.car_id_entry.delete(0, tk.END)
        
        # 检查车辆是否在便道中
        if self.is_car_in_waiting_lane(car_id):
            self.log(f"错误：车辆 {car_id} 在便道中，无法从停车场离开", "error")
            return
        
        # 从停车场离开（实现让路机制）
        car, moved_cars = self.parking_lot.depart(car_id)
        if not car:
            self.log(f"失败：未找到车牌号为 {car_id} 的车辆", "error")
            return
        
        # 记录让路车辆信息
        if moved_cars:
            moved_ids = [moved_car.car_id for moved_car in moved_cars]
            self.log(f"提示：车辆 {car_id} 离开，让路车辆: {', '.join(moved_ids)}", "info")
        
        # 计算费用
        duration = car.get_duration()
        fee = self.billing.calculate_fee(duration)
        formatted = self.billing.format_duration(duration)
        self.log(f"成功：车辆 {car_id} 停留 {formatted}，应缴费用: ¥{fee}", "success")
        
        # 从便道移入一辆车到停车场
        next_car = self.waiting_lane.dequeue()
        if next_car:
            if self.parking_lot.arrive(next_car):
                self.log(f"成功：车辆 {next_car.car_id} 已从便道移入停车场", "success")
            else:
                self.log(f"错误：无法将车辆 {next_car.car_id} 移入停车场", "error")
        
        self.refresh_status()

    def refresh_status(self):
        """刷新状态显示"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        
        # 停车场状态
        self.status_text.insert(tk.END, "停车场状态:\n")
        parking_state = self.parking_lot.current_state()
        if parking_state:
            for car_id, t in parking_state:
                self.status_text.insert(tk.END, f"- {car_id} | {timestamp_to_str(t)}\n")
        else:
            self.status_text.insert(tk.END, "（空）\n")
        
        # 便道状态
        self.status_text.insert(tk.END, "\n便道等待区:\n")
        waiting_state = self.waiting_lane.current_state()
        if waiting_state:
            for car_id, t in waiting_state:
                self.status_text.insert(tk.END, f"- {car_id} | {timestamp_to_str(t)}\n")
        else:
            self.status_text.insert(tk.END, "（空）\n")
        
        self.status_text.config(state=tk.DISABLED)

    def return_main(self):
        """返回主菜单"""
        self.master.destroy()
        from ui.main_menu import MainMenu
        root = tk.Tk()
        MainMenu(root, self.user, self.config)
        root.mainloop()

    def is_car_exists(self, car_id):
        """检查车牌号是否已存在"""
        for car_info in self.parking_lot.current_state():
            if car_info[0] == car_id:
                return True
        for car_info in self.waiting_lane.current_state():
            if car_info[0] == car_id:
                return True
        return False

    def is_car_in_waiting_lane(self, car_id):
        """检查车辆是否在便道中"""
        for car_info in self.waiting_lane.current_state():
            if car_info[0] == car_id:
                return True
        return False