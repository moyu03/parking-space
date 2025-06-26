import time
import tkinter as tk
from tkinter import scrolledtext
from core.parking import Car, ParkingLot, WaitingLane
from core.billing import Billing
from utils.time_utils import timestamp_to_str
from utils.window_utils import center_window

class ParkingUI:
    """停车管理界面"""
    def __init__(self, master, config, user):
        self.master = master
        self.config = config
        self.user = user
        self.master.title("停车管理")
        self.master.geometry("900x500")
        
        # 初始化停车场和便道
        self.parking_lot = ParkingLot(config.parking_capacity)
        self.waiting_lane = WaitingLane(config.waiting_capacity)
        self.billing = Billing(config)
        
        # 主框架
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 输入区域
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(input_frame, text="车牌号:").grid(row=0, column=0, padx=5)
        self.car_id_entry = tk.Entry(input_frame, width=20)
        self.car_id_entry.grid(row=0, column=1, padx=5)
        self.car_id_entry.focus()
        self.car_id_entry.bind("<Return>", lambda event: self.car_arrive())
        
        tk.Button(input_frame, text="车辆进入", command=self.car_arrive).grid(row=0, column=2, padx=5)
        tk.Button(input_frame, text="车辆离开", command=self.car_depart).grid(row=0, column=3, padx=5)
        tk.Button(input_frame, text="返回主菜单", command=self.return_main).grid(row=0, column=4, padx=5)
        
        # 状态区域
        status_frame = tk.Frame(main_frame)
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        # 停车场状态
        status_left = tk.LabelFrame(status_frame, text="停车场状态", font=("Arial", 10, "bold"))
        status_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 添加滚动条
        status_scroll = tk.Scrollbar(status_left)
        status_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.status_text = tk.Text(status_left, height=15, yscrollcommand=status_scroll.set)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        status_scroll.config(command=self.status_text.yview)
        
        # 日志输出
        status_right = tk.LabelFrame(status_frame, text="操作日志", font=("Arial", 10, "bold"))
        status_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.log_text = scrolledtext.ScrolledText(status_right, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)  # 设置为只读
        
        # 配置日志颜色标签
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("success", foreground="green")
        self.log_text.tag_config("fee", foreground="#aa16aa",font=("Arial", 10, "bold"))
        self.log_text.tag_config("warning", foreground="orange")
        self.log_text.tag_config("info", foreground="blue")
        self.log_text.tag_config("movement", foreground="#8A2BE2")  # 紫罗兰色
        self.log_text.tag_config("movement-bold", foreground="#8A2BE2", font=("Arial", 10, "bold"))
        
        # 刷新状态和启动定时刷新
        self.refresh_status()
        self.log("停车管理系统已启动", "info")
        center_window(self.master, 900, 500)
        self.auto_refresh()  # 确保在控件创建后调用

    def log(self, message, level="info"):
        """在日志区域添加消息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n", level)
        self.log_text.see(tk.END)  # 滚动到底部
        self.log_text.config(state=tk.DISABLED)

    def car_arrive(self):
        """处理车辆进入"""
        car_id = self.car_id_entry.get().strip()
        if not car_id:
            self.log("错误：请输入车牌号\n", "error")
            return
        
        if self.is_car_exists(car_id):
            self.log(f"错误：车牌号 {car_id} 已存在\n", "error")
            self.car_id_entry.delete(0, tk.END)
            return
        
        car = Car(car_id)
        if self.parking_lot.arrive(car):
            position = len(self.parking_lot.stack)
            self.log(f"成功：车辆 {car_id} 停入停车场（车位 {position}）\n", "success")
        elif self.waiting_lane.enqueue(car):
            position = len(self.waiting_lane.queue)
            self.log(f"提示：停车场已满，车辆 {car_id} 在便道等待（位置 {position}）\n", "info")
        else:
            self.log(f"失败：停车场和便道均满，车辆 {car_id} 无法进入\n", "warning")
        
        self.car_id_entry.delete(0, tk.END)
        self.refresh_status()

    def car_depart(self):
        """处理车辆离开"""
        car_id = self.car_id_entry.get().strip()
        if not car_id:
            self.log("错误：请输入车牌号\n", "error")
            return
        
        self.car_id_entry.delete(0, tk.END)
        
        # 检查车辆是否在便道中
        if self.is_car_in_waiting_lane(car_id):
            self.log(f"错误：车辆 {car_id} 在便道中，无法从停车场离开\n", "error")
            return
        
        # 从停车场离开（实现让路机制）
        car, moved_cars = self.parking_lot.depart(car_id)
        if not car:
            self.log(f"失败：未找到车牌号为 {car_id} 的车辆\n", "error")
            return
        
        # 记录让路车辆信息
        if moved_cars:
            moved_ids = [car.car_id for car in moved_cars]
            self.log(f"提示：车辆 {car_id} 离开，\n让路车辆: {', '.join(moved_ids)}（共 {len(moved_cars)} 辆）", "movement-bold")
        else:
            self.log(f"提示：车辆 {car_id} 离开，无让路车辆", "info")
        
    # 计算费用 - 使用直接计算方式
        current_time = time.time()
        duration = current_time - car.enter_time  # 直接计算时长
        fee = self.billing.calculate_fee(duration)
        formatted = self.billing.format_duration(duration)
        self.log(f"成功：车辆 {car_id} 停留 {formatted}", "success")
        self.log(f"车辆:{car_id}应缴费用: ¥{fee:.2f}\n", "fee")
        # 关键修复：从便道移入一辆车到停车场
        next_car = self.waiting_lane.dequeue()
        if next_car:
            # 更新车辆的进入时间为当前时间
            next_car.update_enter_time(time.time())
            
            # 关键修复：使用正确的停车场对象
            if self.parking_lot.arrive(next_car):  # 确保这里是self.parking_lot
                position = len(self.parking_lot.stack)
                self.log(f"成功：车辆 {next_car.car_id} 已从便道移入停车场（车位 {position}）\n", "success")
            else:
                # 如果停车场已满（理论上不应该发生），将车放回便道
                self.waiting_lane.enqueue(next_car)
                self.log(f"错误：无法将车辆 {next_car.car_id} 移入停车场（已满），已放回便道\n", "error")
        else:
            self.log("提示：便道中无等待车辆\n", "info")
        
        self.refresh_status()

    def refresh_status(self):
        """刷新状态显示 - 使用固定宽度格式对齐"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        
        # 添加容量信息
        parking_count = len(self.parking_lot.stack)
        parking_capacity = self.parking_lot.capacity
        waiting_count = len(self.waiting_lane.queue)
        waiting_capacity = self.waiting_lane.capacity
        
        self.status_text.insert(tk.END, 
            f"停车场: {parking_count}/{parking_capacity} 便道: {waiting_count}/{waiting_capacity}\n\n")
        
        # 获取当前时间
        current_time = time.time()
        
        # 定义固定列宽
        id_width = 17     # 车牌号列宽
        time_width = 28   # 时间列宽
        duration_width = 18  # 时长列宽
        fee_width = 12    # 费用列宽
        
        # 停车场状态 - 增加时长和费用显示
        self.status_text.insert(tk.END, "停车场状态:\n")
        header = f"{'车牌号':<{id_width}} {'时间':<{time_width}} {'时长':<{duration_width}} {'费用':<{fee_width}}\n"
        self.status_text.insert(tk.END, header)
        self.status_text.insert(tk.END, "-" * (len(header)-1) + "\n")  # 减1是因为换行符
        
        parking_state = self.parking_lot.current_state()
        if parking_state:
            for car_id, enter_time in parking_state:
                # 计算停留时长
                duration = current_time - enter_time
                formatted_duration = self.billing.format_duration(duration)
                # 计算实时费用（浮点数）
                fee = self.billing.calculate_fee(duration)
                # 格式化为两位小数
                fee_str = f"{fee:.2f}"
                
                # 使用固定宽度格式化每行
                formatted_line = f"{car_id:<{id_width}} {timestamp_to_str(enter_time):<{time_width}} " \
                                f"{formatted_duration:<{duration_width}} " \
                                f"¥{fee_str:<{fee_width}}"
                self.status_text.insert(tk.END, formatted_line + "\n")
        else:
            self.status_text.insert(tk.END, "（空）\n")
        
        # 便道状态 - 只显示时长
        self.status_text.insert(tk.END, "\n便道等待区:\n")
        header2 = f"{'车牌号':<{id_width}} {'时间':<{time_width}} {'时长':<{duration_width}} {'费用':<{fee_width}}\n"
        self.status_text.insert(tk.END, header2)
        self.status_text.insert(tk.END, "-" * (len(header2)-1) + "\n")
        
        waiting_state = self.waiting_lane.current_state()
        if waiting_state:
            for car_id, enter_time in waiting_state:
                # 计算等待时长
                duration = current_time - enter_time
                formatted_duration = self.billing.format_duration(duration)
                
                # 使用固定宽度格式化每行
                formatted_line = f"{car_id:<{id_width}} {timestamp_to_str(enter_time):<{time_width}} " \
                                 f"{formatted_duration:<{duration_width}} " \
                                 f"¥0.00{'':<{fee_width-5}}"  # 固定显示¥0.00
                self.status_text.insert(tk.END, formatted_line + "\n")
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
        # 检查停车场
        for car_info in self.parking_lot.current_state():
            if car_info[0] == car_id:
                return True
        
        # 检查便道
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
    
     
    def auto_refresh(self):
        """定时刷新状态"""
        self.refresh_status()
        # 每60秒刷新一次
        self.master.after(2000, self.auto_refresh)