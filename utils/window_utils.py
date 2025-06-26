# utils/window_utils.py

import tkinter as tk

def center_window(window, width=None, height=None):
    """
    将窗口居中显示在屏幕上
    
    参数:
    window: Tkinter 窗口对象
    width: 窗口宽度（可选）
    height: 窗口高度（可选）
    """
    # 获取窗口尺寸（如果未提供）
    if width is None or height is None:
        window.update_idletasks()  # 确保窗口尺寸已计算
        width = window.winfo_width()
        height = window.winfo_height()
    
    # 获取屏幕尺寸
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # 计算居中位置
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # 设置窗口位置
    window.geometry(f"{width}x{height}+{x}+{y}")