# ui/parking_ui.py

import tkinter as tk
from tkinter import messagebox
from core.parking import Car, ParkingLot, WaitingLane
from core.billing import Billing
from utils.time_utils import timestamp_to_str

class ParkingUI:
    """
    停车管理界面类
    
    功能：
    - 显示停车场和便道的状态
    - 处理车辆进入和离开操作
    - 计算停车费用
    - 提供返回主菜单功能
    
    关键属性：
    - master: Tkinter根窗口
    - config: 系统配置对象
    - user: 当前用户对象
    - parking_lot: 停车场对象
    - waiting_lane: 便道对象
    - billing: 计费对象
    - car_id_entry: 车牌号输入框
    - status_text: 状态显示文本框
    """
    
    def __init__(self, master, config, user):
        """
        初始化停车管理界面
        
        参数:
        - master: Tkinter根窗口
        - config: 系统配置对象
        - user: 当前用户对象
        """
        self.master = master
        self.config = config
        self.user = user
        self.master.title("停车管理")
        self.master.geometry("600x400")

        # 初始化停车场和便道对象
        self.parking_lot = ParkingLot(config.parking_capacity)
        self.waiting_lane = WaitingLane(config.waiting_capacity)
        
        # 初始化计费对象
        self.billing = Billing(config)

        # 车牌号输入框
        self.car_id_entry = tk.Entry(master, width=20)
        self.car_id_entry.pack(pady=5)
        self.car_id_entry.focus()  # 自动聚焦到输入框
        
        # 绑定回车键到车辆进入操作
        self.car_id_entry.bind("<Return>", lambda event: self.car_arrive())

        # 车辆进入按钮
        tk.Button(master, text="车辆进入", command=self.car_arrive).pack()
        
        # 车辆离开按钮
        tk.Button(master, text="车辆离开", command=self.car_depart).pack()

        # 状态显示文本框
        self.status_text = tk.Text(master, height=15)
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 返回主菜单按钮
        tk.Button(master, text="返回主菜单", command=self.return_main).pack()
        
        # 刷新状态显示
        self.refresh_status()

    def car_arrive(self):
        """
        处理车辆进入操作
        
        功能:
        1. 获取车牌号
        2. 检查是否为空
        3. 检查车牌号是否已存在
        4. 尝试将车辆停入停车场或便道
        5. 清空输入框
        6. 刷新状态显示
        """
        # 获取车牌号并去除空白
        car_id = self.car_id_entry.get().strip()
        
        # 检查车牌号是否为空
        if not car_id:
            messagebox.showwarning("错误", "请输入车牌号")
            return
        
        # 检查车牌号是否已存在
        if self.is_car_exists(car_id):
            messagebox.showwarning("错误", f"车牌号 {car_id} 已存在，请勿重复添加")
            self.car_id_entry.delete(0, tk.END)  # 清空输入框
            return
        
        # 创建车辆对象
        car = Car(car_id)
        
        # 尝试将车辆停入停车场
        if self.parking_lot.arrive(car):
            messagebox.showinfo("成功", f"车辆 {car_id} 停入停车场")
        
        # 尝试将车辆停入便道
        elif self.waiting_lane.enqueue(car):
            messagebox.showinfo("提示", f"停车场已满，车辆 {car_id} 等待中")
        
        # 停车场和便道都已满
        else:
            messagebox.showwarning("失败", f"停车场和便道均满，车辆 {car_id} 无法进入")
        
        # 清空输入框
        self.car_id_entry.delete(0, tk.END)
        
        # 刷新状态显示
        self.refresh_status()

    def car_depart(self):
        """
        处理车辆离开操作
        
        功能:
        1. 获取车牌号
        2. 检查是否为空
        3. 尝试从停车场移出车辆
        4. 计算停车费用
        5. 清空输入框
        6. 如果有等待车辆，移入停车场
        7. 刷新状态显示
        """
        # 获取车牌号并去除空白
        car_id = self.car_id_entry.get().strip()
        
        # 检查车牌号是否为空
        if not car_id:
            messagebox.showwarning("错误", "请输入车牌号")
            return
        
        # 清空输入框
        self.car_id_entry.delete(0, tk.END)
        
        # 尝试从停车场移出车辆
        car = self.parking_lot.depart(car_id)
        if not car:
            messagebox.showwarning("失败", f"未找到车牌号为 {car_id} 的车辆")
            return
        
        # 计算停车时间和费用
        duration = car.get_duration()
        fee = self.billing.calculate_fee(duration)
        formatted = self.billing.format_duration(duration)
        
        # 显示离开信息
        messagebox.showinfo("离开成功", f"车辆 {car_id} 停留 {formatted}\n应缴费用: ¥{fee}")

        # 从便道中移出第一辆车（如果有）并移入停车场
        next_car = self.waiting_lane.dequeue()
        if next_car:
            self.parking_lot.arrive(next_car)
            messagebox.showinfo("提示", f"车辆 {next_car.car_id} 已从便道移入停车场")
        
        # 刷新状态显示
        self.refresh_status()

    def refresh_status(self):
        """
        刷新状态显示
        
        功能:
        1. 清空状态文本框
        2. 显示停车场当前状态
        3. 显示便道当前状态
        """
        # 清空状态文本框
        self.status_text.delete(1.0, tk.END)
        
        # 显示停车场状态
        self.status_text.insert(tk.END, "[停车场]:\n")
        for car_id, t in self.parking_lot.current_state():
            self.status_text.insert(tk.END, f"- {car_id} | {timestamp_to_str(t)}\n")
        
        # 显示便道状态
        self.status_text.insert(tk.END, "\n[便道等待区]:\n")
        for car_id, t in self.waiting_lane.current_state():
            self.status_text.insert(tk.END, f"- {car_id} | {timestamp_to_str(t)}\n")

    def return_main(self):
        """
        返回主菜单
        
        功能:
        1. 销毁当前窗口
        2. 创建主菜单窗口
        """
        self.master.destroy()
        from ui.main_menu import MainMenu
        root = tk.Tk()
        MainMenu(root, self.user, self.config)
        root.mainloop()

    def is_car_exists(self, car_id):
        """
        检查车牌号是否已在停车场或便道中存在
        
        参数:
        - car_id: 要检查的车牌号
        
        返回:
        - True: 车牌号已存在
        - False: 车牌号不存在
        """
        # 检查停车场
        for car_info in self.parking_lot.current_state():
            if car_info[0] == car_id:
                return True
        
        # 检查便道
        for car_info in self.waiting_lane.current_state():
            if car_info[0] == car_id:
                return True
        
        return False