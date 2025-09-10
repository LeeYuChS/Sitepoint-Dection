import tkinter as tk
from gui_setting import YOLO_GUI
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import CONFIG


def main():
    win = tk.Tk()
    app = YOLO_GUI(win, CONFIG.best_model_weight)
    win.mainloop()

if __name__ == "__main__":
    main()