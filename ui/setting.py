# ui/settings.py

import tkinter as tk
from tkinter import messagebox

class SettingsUI:
    def __init__(self, master, config, user):
        self.master = master
        self.config = config
        self.user = user
        self.master.title("设置")
        self.master.geometry("400x300")

        tk.Label(master, text="停车场容量:").pack()
        self.parking_entry = tk.Entry(master)
        self.parking_entry.insert(0, str(config.parking_capacity))
        self.parking_entry.pack()

        tk.Label(master, text="便道容量:").pack()
        self.waiting_entry = tk.Entry(master)
        self.waiting_entry.insert(0, str(config.waiting_capacity))
        self.waiting_entry.pack()

        tk.Label(master, text="计费模式:").pack()
        self.billing_var = tk.StringVar(value=config.billing_mode)
        tk.OptionMenu(master, self.billing_var, "per_minute", "per_hour", "fixed").pack()

        tk.Label(master, text="计费金额:").pack()
        self.rate_entry = tk.Entry(master)
        default_rate = config.fee_per_minute if config.billing_mode == "per_minute" \
            else config.fee_per_hour if config.billing_mode == "per_hour" \
            else config.fixed_fee
        self.rate_entry.insert(0, str(default_rate))
        self.rate_entry.pack()

        tk.Button(master, text="保存设置", command=self.save).pack(pady=10)
        tk.Button(master, text="返回主菜单", command=self.return_main).pack()

        
        # 添加计费模式说明
        billing_frame = tk.LabelFrame(master, text="当前计费模式说明")
        billing_frame.pack(fill="x", padx=10, pady=5)
        
        billing_text = tk.Text(billing_frame, height=4, wrap="word")
        billing_text.pack(fill="x", padx=5, pady=5)
        
        # 根据配置显示计费模式说明
        if config.billing_mode == "per_minute":
            msg = f"当前计费模式: 按分钟计费\n费率: ¥{config.fee_per_minute}/分钟\n示例: 停车30分钟费用 = 30 × {config.fee_per_minute} = ¥{30 * config.fee_per_minute:.2f}"
        elif config.billing_mode == "per_hour":
            msg = f"当前计费模式: 按小时计费\n费率: ¥{config.fee_per_hour}/小时\n示例: 停车1.5小时费用 = 1.5 × {config.fee_per_hour} = ¥{1.5 * config.fee_per_hour:.2f}"
        else:
            msg = f"当前计费模式: 固定费率\n费用: ¥{config.fixed_fee}\n无论停车时长多久，费用固定"
        
        billing_text.insert("1.0", msg)
        billing_text.config(state="disabled")  # 设置为只读

    def save(self):
        try:
            pc = int(self.parking_entry.get())
            wc = int(self.waiting_entry.get())
            rate = int(self.rate_entry.get())
            self.config.set_capacity(pc, wc)
            self.config.set_billing(self.billing_var.get(), rate)
            messagebox.showinfo("成功", "设置已保存")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")

    def return_main(self):
        self.master.destroy()
        from .main_menu import MainMenu
        root = tk.Tk()
        MainMenu(root, self.user, self.config)
        root.mainloop()
