import time
import csv
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from core.parking import Car, ParkingLot, WaitingLane
from core.billing import Billing
from utils.time_utils import timestamp_to_str
from utils.window_utils import center_window

# 检查是否支持双向出口系统
try:
    from extension.dual_exit.adapter import DualSystemAdapter
    from extension.dual_exit.ui_extension import DualExitParkingUI
    DUAL_EXIT_SUPPORTED = True
except ImportError:
    DUAL_EXIT_SUPPORTED = False

class ParkingUI:
    """停车管理界面"""
    def __init__(self, master, config, user):
        self.master = master
        self.config = config
        self.user = user
        
        # 设置窗口标题显示当前系统模式
        system_type = "单门系统" if not config.enable_dual_exit else "双门系统"
        self.master.title(f"停车管理系统 - {system_type}")
        self.master.geometry("1000x700")  # 增大窗口尺寸
        center_window(self.master, 1000, 700)  # 确保居中显示

        # 初始化停车场和便道
        self.parking_lot = ParkingLot(config.parking_capacity)
        self.waiting_lane = WaitingLane(config.waiting_capacity)
        self.billing = Billing(config)
        
        # 主框架
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 系统模式显示
        mode_frame = tk.Frame(main_frame, bg="#f0f0f0", padx=10, pady=5)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        mode_text = "当前模式: 单门系统" if not config.enable_dual_exit else "当前模式: 双门系统"
        mode_color = "#4CAF50" if not config.enable_dual_exit else "#2196F3"
        self.mode_label = tk.Label(
            mode_frame, 
            text=mode_text, 
            font=("Arial", 10, "bold"), 
            fg="white", 
            bg=mode_color,
            padx=10,
            pady=2
        )
        self.mode_label.pack(side=tk.LEFT)
        
        # 添加返回主菜单按钮
        tk.Button(
            mode_frame, 
            text="返回主菜单", 
            command=self.return_main,
            padx=5
        ).pack(side=tk.RIGHT)
        
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
        
        # 在输入区域新增按钮
        tk.Button(input_frame, text="搜索车辆", command=self.search_car).grid(row=0, column=5, padx=5)
        tk.Button(input_frame, text="历史记录", command=self.show_history).grid(row=0, column=6, padx=5)
        
        # 如果是管理员，添加导出按钮
        if user.role == "admin":
            tk.Button(input_frame, text="导出数据", command=self.export_data).grid(row=0, column=7, padx=5)
        
       
        # 状态区域
        status_frame = tk.Frame(main_frame)
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        # 首先确保日志控件总是被创建
        # 日志输出 - 现在总是初始化
        status_right = tk.LabelFrame(status_frame, text="操作日志", font=("Arial", 10, "bold"))
        status_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.log_text = scrolledtext.ScrolledText(status_right, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

        # 配置日志标签
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("success", foreground="green")
        self.log_text.tag_config("fee", foreground="#aa16aa", font=("Arial", 10, "bold"))
        self.log_text.tag_config("warning", foreground="orange")
        self.log_text.tag_config("info", foreground="blue")
        self.log_text.tag_config("movement", foreground="#8A2BE2")  # 紫罗兰色
        self.log_text.tag_config("movement-bold", foreground="#8A2BE2", font=("Arial", 10, "bold"))
        
        # 根据系统模式显示不同的UI
        self.dual_system = None
        self.dual_ui = None
        
        # 左侧状态区域容器 - 现在作为独立变量
        self.status_left_container = tk.Frame(status_frame)
        self.status_left_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        if config.enable_dual_exit and DUAL_EXIT_SUPPORTED:
            try:
                # 创建双向系统
                self.dual_system = DualSystemAdapter(
                    config, 
                    self.parking_lot, 
                    self.waiting_lane,
                    log_callback=self.log
                )
                # 创建双向系统UI
                self.dual_ui = DualExitParkingUI(self.status_left_container, self.dual_system, self.log_text)
                self.log(f"双门系统已启用，入口和出口分离", "info")
            except Exception as e:
                self.log(f"警告: 无法初始化双门系统: {str(e)}", "warning")
                config.enable_dual_exit = False  # 回退到单门系统
                self.mode_label.config(
                    text="当前模式: 单门系统 (双门系统初始化失败)", 
                    bg="#FF9800"  # 橙色警告
                )
                # 初始化单门系统UI
                self.init_single_system_ui()
        else:
            # 单门系统UI
            if config.enable_dual_exit and not DUAL_EXIT_SUPPORTED:
                self.log("警告: 系统不支持双门模式，已自动切换到单门系统", "warning")
                config.enable_dual_exit = False
                self.mode_label.config(
                    text="当前模式: 单门系统 (双门系统不支持)", 
                    bg="#FF9800"  # 橙色警告
                )
            
            # 初始化单门系统UI
            self.init_single_system_ui()
        
        # 刷新状态和启动定时刷新
        self.refresh_status()
        self.log(f"停车管理系统已启动 ({system_type})", "info")
        self.auto_refresh()
    
    def init_single_system_ui(self):
        """初始化单门系统UI组件"""
        # 停车场状态
        self.status_left = tk.LabelFrame(self.status_left_container, text="停车场状态", font=("Arial", 10, "bold"))
        self.status_left.pack(fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        status_scroll = tk.Scrollbar(self.status_left)
        status_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.status_text = tk.Text(self.status_left, height=15, yscrollcommand=status_scroll.set)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        status_scroll.config(command=self.status_text.yview)

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
        
        try:
            car = Car(car_id)
            
            if self.dual_system:
                # 使用双门系统
                status, position, _ = self.dual_system.enter(car)
                if status == "PARKED":
                    self.log(f"成功：车辆 {car_id} 停入{position}\n", "success")
                elif status == "IN_SIDE_ROAD":
                    self.log(f"提示：停车场已满，车辆 {car_id} 在{position}等待\n", "info")
                else:
                    self.log(f"失败：{position}\n", "warning")
            else:
                # 原有单出口逻辑
                if self.is_car_exists(car_id):
                    self.log(f"错误：车牌号 {car_id} 已存在\n", "error")
                    self.car_id_entry.delete(0, tk.END)
                    return
                
                if self.parking_lot.arrive(car):
                    position = len(self.parking_lot.stack)
                    self.log(f"成功：车辆 {car_id} 停入停车场（车位 {position}）\n", "success")
                elif self.waiting_lane.enqueue(car):
                    position = len(self.waiting_lane.queue)
                    self.log(f"提示：停车场已满，车辆 {car_id} 在便道等待（位置 {position}）\n", "info")
                else:
                    self.log(f"失败：停车场和便道均满，车辆 {car_id} 无法进入\n", "warning")
            
        except Exception as e:
            # 添加详细的错误日志
            self.log(f"车辆进入操作出错: {str(e)}\n", "error")
            import traceback
            traceback.print_exc()  # 在控制台打印完整堆栈
            
        finally:
            self.car_id_entry.delete(0, tk.END)
            self.refresh_status()

    def search_car(self):
        """搜索车辆"""
        car_id = self.car_id_entry.get().strip()
        if not car_id:
            self.log("错误：请输入车牌号进行搜索\n", "error")
            return
        
        # 创建搜索弹窗
        search_win = tk.Toplevel(self.master)
        search_win.title(f"车辆搜索 - {car_id}")
        search_win.geometry("600x400")
        center_window(search_win, 600, 400)
        
        # 创建表格
        columns = ("位置", "车牌号", "进入时间", "停留时长")
        tree = ttk.Treeview(search_win, columns=columns, show="headings")
        
        # 设置列宽
        tree.column("位置", width=100, anchor="center")
        tree.column("车牌号", width=150, anchor="center")
        tree.column("进入时间", width=200, anchor="center")
        tree.column("停留时长", width=150, anchor="center")
        
        # 设置表头
        for col in columns:
            tree.heading(col, text=col)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(search_win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 搜索停车场
        for i, car in enumerate(self.parking_lot.stack):
            if car.car_id == car_id:
                duration = time.time() - car.enter_time
                tree.insert("", "end", values=(
                    f"停车场 {i+1}",
                    car.car_id,
                    timestamp_to_str(car.enter_time),
                    self.billing.format_duration(duration)
                ))
        
        # 搜索便道
        for i, car in enumerate(self.waiting_lane.queue):
            if car.car_id == car_id:
                duration = time.time() - car.enter_time
                tree.insert("", "end", values=(
                    f"便道 {i+1}",
                    car.car_id,
                    timestamp_to_str(car.enter_time),
                    self.billing.format_duration(duration)
                ))
        
        # 搜索历史记录
        for record in self.config.history:
            if record["car_id"] == car_id:
                enter_time = record["enter_time"]
                exit_time = record["exit_time"]
                duration = exit_time - enter_time
                tree.insert("", "end", values=(
                    "历史记录",
                    record["car_id"],
                    timestamp_to_str(enter_time),
                    self.billing.format_duration(duration)
                ))
        
        # 如果启用了双向系统，添加最优路径显示
        if self.dual_system:
            try:
                exit_side, cost = self.dual_system.get_optimal_path(car_id)
                if exit_side:
                    tree.insert("", "end", values=(
                        "推荐出口",
                        car_id,
                        f"{exit_side.upper()}出口",
                        f"成本: {cost:.1f}"
                    ))
            except Exception as e:
                self.log(f"搜索最优路径失败: {str(e)}", "error")
        
        if not tree.get_children():
            tree.insert("", "end", values=("未找到", car_id, "", ""))
        
        # 添加关闭按钮
        tk.Button(search_win, text="关闭", command=search_win.destroy).pack(pady=10)
    
    def show_history(self):
        """显示历史记录"""
        history_win = tk.Toplevel(self.master)
        history_win.title("停车历史记录")
        history_win.geometry("800x500")
        center_window(history_win, 800, 500)
        
        # 创建表格
        columns = ("序号", "车牌号", "进入时间", "离开时间", "停留时长", "费用(¥)")
        tree = ttk.Treeview(history_win, columns=columns, show="headings")
        
        # 设置列宽
        col_widths = [50, 100, 180, 180, 120, 80]
        for col, width in zip(columns, col_widths):
            tree.column(col, width=width, anchor="center")
            tree.heading(col, text=col)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(history_win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 添加数据（按时间倒序）
        for i, record in enumerate(reversed(self.config.history)):
            enter_time = record["enter_time"]
            exit_time = record["exit_time"]
            duration = exit_time - enter_time
            
            tree.insert("", "end", values=(
                i + 1,
                record["car_id"],
                timestamp_to_str(enter_time),
                timestamp_to_str(exit_time),
                self.billing.format_duration(duration),
                f"{record['fee']:.2f}"
            ))
        
        # 添加底部按钮
        btn_frame = tk.Frame(history_win)
        btn_frame.pack(fill="x", pady=10)
        
        if self.user.role == "admin":
            tk.Button(btn_frame, text="清空历史", 
                     command=lambda: self.clear_history(history_win)).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="关闭", command=history_win.destroy).pack(side="right", padx=10)
    
    def clear_history(self, window):
        """清空历史记录"""
        if tk.messagebox.askyesno("确认", "确定要清空所有历史记录吗？此操作不可恢复！"):
            self.config.clear_history()
            window.destroy()
            self.log("历史记录已清空", "info")
    
    def export_data(self):
        """导出数据到CSV文件"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")],
                title="导出停车数据"
            )
            
            if not file_path:
                return
            
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    # 写入表头
                    writer.writerow(["类型", "车牌号", "进入时间", "停留时长", "状态"])
                    
                    # 导出停车场数据
                    for i, car in enumerate(self.parking_lot.stack):
                        duration = time.time() - car.enter_time
                        writer.writerow([
                            "停车场",
                            car.car_id,
                            timestamp_to_str(car.enter_time),
                            self.billing.format_duration(duration),
                            "停放中"
                        ])
                    
                    # 导出便道数据
                    for i, car in enumerate(self.waiting_lane.queue):
                        duration = time.time() - car.enter_time
                        writer.writerow([
                            "便道",
                            car.car_id,
                            timestamp_to_str(car.enter_time),
                            self.billing.format_duration(duration),
                            "等待中"
                        ])
                    
                    # 导出历史数据
                    for record in self.config.history:
                        duration = record["exit_time"] - record["enter_time"]
                        writer.writerow([
                            "历史记录",
                            record["car_id"],
                            timestamp_to_str(record["enter_time"]),
                            self.billing.format_duration(duration),
                            "已完成"
                        ])
                    
                    self.log(f"数据已成功导出到: {file_path}", "success")
                    return True
            
            except PermissionError:
                self.log("导出失败: 没有写入权限或文件被占用", "error")
            except Exception as e:
                self.log(f"导出失败: {str(e)}", "error")
        
        except Exception as e:
            self.log(f"导出失败: {str(e)}", "error")
            return False
    

    def car_depart(self):
        """处理车辆离开"""
        car_id = self.car_id_entry.get().strip()
        if not car_id:
            self.log("错误：请输入车牌号\n", "error")
            return
        
        self.car_id_entry.delete(0, tk.END)
        
        try:
            if self.dual_system:
                # 使用双向系统离开
                status, result = self.dual_system.leave(car_id)
                
                if status == "SUCCESS":
                    # 显示离开信息
                    duration = result["departed"]["duration"]
                    fee = self.billing.calculate_fee(duration)
                    self.log(f"车辆 {car_id} 已离开，费用: ¥{fee:.2f}\n", "success")
                    
                    # 显示补充车辆信息
                    if "entered" in result:
                        new_car = result["entered"]
                        self.log(f"车辆 {new_car['car'].car_id} 已从便道进入停车场\n", "info")
                else:
                    self.log(f"失败: {result}\n", "error")
            else:
                # 原有单出口逻辑
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
                
                # 计算费用
                current_time = time.time()
                duration = current_time - car.enter_time
                fee = self.billing.calculate_fee(duration)
                formatted = self.billing.format_duration(duration)
                
                # 添加详细计费信息
                detailed_calc = self.billing.detailed_calculation(duration)
                self.log(f"计费详情:\n{detailed_calc}", "fee")
                
                # 添加历史记录
                self.config.add_history(car_id, car.enter_time, current_time, fee)

                self.log(f"成功：车辆 {car_id} 停留 {formatted}", "success")
                self.log(f"车辆:{car_id}应缴费用: ¥{fee:.2f}\n", "fee")
                
                # 从便道移入一辆车到停车场
                next_car = self.waiting_lane.dequeue()
                if next_car:
                    # 更新车辆的进入时间为当前时间
                    next_car.update_enter_time(time.time())
                    
                    if self.parking_lot.arrive(next_car):
                        position = len(self.parking_lot.stack)
                        self.log(f"成功：车辆 {next_car.car_id} 已从便道移入停车场（车位 {position}）\n", "success")
                    else:
                        # 如果停车场已满（理论上不应该发生），将车放回便道
                        self.waiting_lane.enqueue(next_car)
                        self.log(f"错误：无法将车辆 {next_car.car_id} 移入停车场（已满），已放回便道\n", "error")
                else:
                    self.log("提示：便道中无等待车辆\n", "info")
            
            self.refresh_status()
        
        except Exception as e:
            self.log(f"车辆离开操作出错: {str(e)}\n", "error")
            import traceback
            traceback.print_exc()

    def refresh_status(self):
        """刷新状态显示 - 使用固定宽度格式对齐"""
        if self.dual_system and self.dual_ui:
            # 刷新双向系统UI
            self.dual_ui.refresh_status()
            return
        
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
        # 修复的f-string语法 - 使用单引号包裹整个字符串
        header = f'{"车牌号":<{id_width}} {"时间":<{time_width}} {"时长":<{duration_width}} {"费用":<{fee_width}}\n'
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
        # 修复的f-string语法 - 使用单引号包裹整个字符串
        header2 = f'{"车牌号":<{id_width}} {"时间":<{time_width}} {"时长":<{duration_width}} {"费用":<{fee_width}}\n'
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
        # 每5秒刷新一次
        self.master.after(5000, self.auto_refresh)

