import tkinter as tk
from ui.login import LoginUI
import sys
import os
sys.path.append(os.path.dirname(__file__))


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginUI(root)
    root.mainloop()