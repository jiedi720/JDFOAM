import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
import os

class GmshConverterGUI:
    def __init__(self, root, update_func):
        self.root = root
        self.update_func = update_func
        self.root.title("OpenFOAM Gmsh转换工具")
        
        # 居中逻辑
        width, height = 650, 600 # 稍微增加高度
        scr_w = self.root.winfo_screenwidth()
        scr_h = self.root.winfo_screenheight()
        x = (scr_w - width) // 2
        y = (scr_h - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # 默认路径
        default_msh_dir = r"C:\WSL\WSLDesktop\Gmsh"
        self.msh_path = tk.StringVar(value=default_msh_dir if os.path.exists(default_msh_dir) else "")
        self.case_path = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        # 真正的代码块作用：
        # 使用 pack 布局时，通过 side="top" 和 side="bottom" 明确元素顺序。
        # fill="both" 和 expand=True 确保日志区域占据剩余的所有空间。
        
        pad = {'padx': 15, 'pady': 5}
        
        # 1. 顶部路径配置区
        top = tk.LabelFrame(self.root, text=" 路径配置 ", padx=10, pady=10)
        top.pack(side="top", fill="x", **pad)
        
        tk.Label(top, text="MSH 文件/路径:").grid(row=0, column=0, sticky="w")
        tk.Entry(top, textvariable=self.msh_path, width=55).grid(row=0, column=1, padx=5)
        tk.Button(top, text="选择文件", command=self.select_msh).grid(row=0, column=2)
        
        tk.Label(top, text="算例目录:").grid(row=1, column=0, sticky="w")
        tk.Entry(top, textvariable=self.case_path, width=55).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(top, text="选择目录", command=self.select_case).grid(row=1, column=2)

        # 2. 底部按钮区 (先放置底部，确保它永远可见)
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side="bottom", fill="x", **pad)
        
        self.btn = tk.Button(bottom_frame, text="开始执行 (WSL)", command=self.start, 
                             bg="#0078d4", fg="white", height=2, font=("微软雅黑", 10, "bold"))
        self.btn.pack(fill="x", pady=10)

        # 3. 中间进度条和日志区 (占用剩余空间)
        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="indeterminate")
        self.progress.pack(side="top", fill="x", **pad)

        self.log_area = scrolledtext.ScrolledText(self.root, font=("Consolas", 9))
        self.log_area.pack(side="top", fill="both", expand=True, **pad)

    def select_msh(self):
        initial_dir = self.msh_path.get() if os.path.isdir(self.msh_path.get()) else None
        p = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Gmsh Files", "*.msh")])
        if p: self.msh_path.set(p)

    def select_case(self):
        p = filedialog.askdirectory()
        if p: self.case_path.set(p)

    def log_msg(self, msg):
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.see(tk.END)

    def start(self):
        if not os.path.isfile(self.msh_path.get()):
            messagebox.showwarning("提示", "请选择具体的 .msh 文件")
            return
        if not self.case_path.get():
            messagebox.showwarning("提示", "请选择算例目录")
            return
        
        self.btn.config(state="disabled", text="正在处理...")
        self.log_area.delete(1.0, tk.END)
        self.progress.start(10)
        
        t = threading.Thread(target=self.run_worker, daemon=True)
        t.start()

    def run_worker(self):
        success = self.update_func(self.msh_path.get(), self.case_path.get(), logger=self.log_msg)
        self.progress.stop()
        self.btn.config(state="normal", text="开始执行 (WSL)")
        if success:
            messagebox.showinfo("完成", "网格转换及边界修正成功！")