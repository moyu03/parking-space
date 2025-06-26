# ui/parking_ui.py

import tkinter as tk
from tkinter import messagebox
from core.parking import Car, ParkingLot, WaitingLane
from core.billing import Billing
from utils.time_utils import timestamp_to_str

class ParkingUI:
    def __init__(self, master, config, user):
        self.master = master
        self.config = config
        self.user = user
        self.master.title("停车管理")
        self.master.geometry("600x400")

        self.parking_lot = ParkingLot(config.parking_capacity)
        self.waiting_lane = WaitingLane(config.waiting_capacity)
        self.billing = Billing(config)

        self.car_id_entry = tk.Entry(master, width=20)
        self.car_id_entry.pack(pady=5)

        tk.Button(master, text="车辆进入", command=self.car_arrive).pack()
        tk.Button(master, text="车辆离开", command=self.car_depart).pack()

        self.status_text = tk.Text(master, height=15)
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Button(master, text="返回主菜单", command=self.return_main).pack()
        self.refresh_status()

    def car_arrive(self):
        car_id = self.car_id_entry.get().strip()
        if not car_id:
            messagebox.showwarning("错误", "请输入车牌号")
            return
        car = Car(car_id)
        if self.parking_lot.arrive(car):
            messagebox.showinfo("成功", f"车辆 {car_id} 停入停车场")
        elif self.waiting_lane.enqueue(car):
            messagebox.showinfo("提示", f"停车场已满，车辆 {car_id} 等待中")
        else:
            messagebox.showwarning("失败", f"停车场和便道均满，车辆 {car_id} 无法进入")
        self.refresh_status()

    def car_depart(self):
        car_id = self.car_id_entry.get().strip()
        car = self.parking_lot.depart(car_id)
        if not car:
            messagebox.showwarning("失败", f"未找到车牌号为 {car_id} 的车辆")
            return
        duration = car.get_duration()
        fee = self.billing.calculate_fee(duration)
        formatted = self.billing.format_duration(duration)
        messagebox.showinfo("离开成功", f"车辆 {car_id} 停留 {formatted}\n应缴费用: ¥{fee}")

        next_car = self.waiting_lane.dequeue()
        if next_car:
            self.parking_lot.arrive(next_car)
        self.refresh_status()

    def refresh_status(self):
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, "[停车场]:\n")
        for car_id, t in self.parking_lot.current_state():
            self.status_text.insert(tk.END, f"- {car_id} | {timestamp_to_str(t)}\n")

        self.status_text.insert(tk.END, "\n[便道等待区]:\n")
        for car_id, t in self.waiting_lane.current_state():
            self.status_text.insert(tk.END, f"- {car_id} | {timestamp_to_str(t)}\n")

    def return_main(self):
        self.master.destroy()
        from ui.main_menu import MainMenu
        root = tk.Tk()
        MainMenu(root, self.user, self.config)
        root.mainloop()
