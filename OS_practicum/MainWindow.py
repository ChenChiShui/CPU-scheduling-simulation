import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import random
import string
from Process import Process

class MainWindow(tk.Tk):
    def __init__(self, ls1, ls2, cpu_core, process_generator, rq_list):
        super().__init__()  # 初始化父类
        
        self.ls1 = ls1
        self.ls2 = ls2
        self.cpu_core = cpu_core
        self.process_generator = process_generator
        self.rq_list = rq_list
        self.auto_gen = True
        self.user_require_interrupt = False

        # 设置窗口标题和大小
        self.title("操作系统课设——多级反馈队列调度模拟")
        self.geometry("900x700")

        # 初始化存储区域列表
        self.areas = []

        # 扩展渐变颜色列表
        self.area_colors = [
            "#0000FF", "#0033CC", "#0066CC", "#0099CC", "#00CCCC",
            "#00FFCC", "#33FFCC", "#66FFCC", "#99FFCC", "#CCFFCC",
            "#1E90FF", "#4169E1", "#4682B4", "#5F9EA0", "#6495ED",
            "#7B68EE", "#87CEFA", "#ADD8E6", "#B0C4DE", "#B0E0E6"
        ]

        # 创建上部分区域
        for i, area_info in enumerate(ls1):
            self.create_area(i, area_info[0])

        # 创建下部分区域
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)

        for i, area_info in enumerate(ls2, start=len(ls1)):
            self.create_area(i, area_info[0], parent=bottom_frame, side=tk.LEFT, width=300, height=100)

        # 创建CPU时钟显示区域
        self.cpu_clock_frame = ttk.Frame(bottom_frame, borderwidth=2, relief="groove", width=180, height=100)
        self.cpu_clock_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.cpu_clock_frame.pack_propagate(False)
        self.cpu_clock_label = ttk.Label(self.cpu_clock_frame, text="CPU_CLOCK: []", font=('Arial', 12))
        self.cpu_clock_label.pack(expand=True)

        # 创建两个框架来容纳按钮
        button_frame1 = ttk.Frame(self)
        button_frame1.pack(side=tk.BOTTOM, pady=(0, 5))
        
        button_frame2 = ttk.Frame(self)
        button_frame2.pack(side=tk.BOTTOM, pady=(0, 10))

        # 创建按钮
        tk.Button(button_frame1, 
                  text='Next Clock', 
                  command=self.refresh_content,
                  width=15,
                  height=2,
                  font=('Arial', 12)
                  ).pack(side=tk.LEFT, padx=5)

        self.auto_button = tk.Button(button_frame1, 
                  text='Auto Start', 
                  command=self.toggle_auto_refresh,
                  width=15,
                  height=2,
                  font=('Arial', 12)
                  )
        self.auto_button.pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame2, 
                  text='Add A Process', 
                  command=self.add_process_dialog,
                  width=15,
                  height=2,
                  font=('Arial', 12)
                  ).pack(side=tk.LEFT, padx=5)

        self.gen_button = tk.Button(button_frame2, 
                  text='Stop Gen', 
                  command=self.toggle_gen,
                  width=15,
                  height=2,
                  font=('Arial', 12)
                  )
        self.gen_button.pack(side=tk.LEFT, padx=5)

        self.unjam_button = tk.Button(button_frame2, 
                  text='Unjam Waiting List', 
                  command=self.toggle_jam_waiting_list,
                  width=15,
                  height=2,
                  font=('Arial', 12)
                  )
        self.unjam_button.pack(side=tk.LEFT, padx=5)

        self.interrupt_button = tk.Button(button_frame2, 
                  text='Interrupt', 
                  command=self.set_interrupt,
                  width=15,
                  height=2,
                  font=('Arial', 12)
                  )
        self.interrupt_button.pack(side=tk.LEFT, padx=5)

        self.save_table_button = tk.Button(button_frame2, 
                  text='Save Table', 
                  command=self.save_table,
                  width=15,
                  height=2,
                  font=('Arial', 12)
                  )
        self.save_table_button.pack(side=tk.LEFT, padx=5)


        # 初始化内容
        self.refresh_content()

        # 自动刷新标志和任务ID
        self.auto_refresh = False
        self.auto_refresh_task = None

    def save_table(self):
        # 调用CPU的方法来生成和保存表格
        filename = "completed_processes.txt"  
        self.cpu_core.generate_and_save_table(filename)
        messagebox.showinfo("保存成功", f"表格已保存至 {filename}")


    def create_area(self, index, label, parent=None, side=None, width=380, height=150):
        if parent:
            area = ttk.Frame(parent, borderwidth=2, relief="groove", width=width, height=height)
            area.pack(side=side, fill=tk.BOTH, expand=True, padx=5, pady=5)
        else:
            area = ttk.Frame(self, borderwidth=2, relief="groove")
            area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        area.pack_propagate(False)
        
        label_widget = ttk.Label(area, text=label)
        label_widget.pack(pady=5)
        
        inner_frame = ttk.Frame(area)
        inner_frame.pack(expand=True, fill=tk.BOTH)
        
        self.areas.append(inner_frame)

    def add_process_dialog(self):
        while True:
            name = simpledialog.askstring("Input", "Enter process name:")
            if name is None:
                return  # User cancelled
            if name.strip() == "":
                messagebox.showerror("Error", "Process name cannot be empty. Please try again.")
                continue
            break

        while True:
            total_time = simpledialog.askinteger("Input", "Enter total time (must be an integer greater than 1):")
            if total_time is None:
                return  # User cancelled
            if not isinstance(total_time, int) or total_time <= 1:
                messagebox.showerror("Error", "Total time must be an integer greater than 1. Please try again.")
                continue
            break
        t = self.cpu_core.get_cpu_clock()
        p = Process(name=name, arrive_time=t, tot_time=total_time, que_id=0)
        self.rq_list[0].offer(p)

        print(f"Adding new process: Name = {name}, Total Time = {total_time}")
        # Here you can add the logic to actually add the process to your system
        
    def refresh_content(self):
        self.cpu_core.run_for_1clk()
        if self.auto_gen:
            self.process_generator.run_for_1clk()

        # hard code
        for i in range(5):
            self.ls1[i][1] = self.rq_list[i].get_que_list()
        # waiting list
        self.ls2[0][1] = self.cpu_core.get_waiting_list()
        # CPU current
        self.ls2[1][1] = self.cpu_core.get_now_onboard()

        for i, area in enumerate(self.areas):
            for widget in area.winfo_children():
                widget.destroy()
            
            if i < len(self.ls1):
                content = self.ls1[i][1]
            else:
                content = self.ls2[i - len(self.ls1)][1]
            
            color = self.area_colors[i % len(self.area_colors)]
            
            if i == len(self.areas) - 1:  # CPU区域
                if content:  # 如果有内容
                    item = content[0]
                    if item[0] == 'HANGING':
                        square_color = 'green'
                    elif 'Interrupt' in item[0]:
                        square_color = 'red'
                    else:
                        square_color = 'orange'

                    square = tk.Frame(area, width=120, height=60, bg=square_color, highlightbackground="black", highlightthickness=1)
                    square.pack(expand=True)
                    square.pack_propagate(False)

                    tk.Label(square, text=item[0], bg=square_color, fg="white").pack(fill=tk.X)
                    tk.Label(square, text=f"arrive_time: [{item[1]}]", bg=square_color, fg="white").pack(fill=tk.X)
                    tk.Label(square, text=f"rest_time: [{item[2]}]", bg=square_color, fg="white").pack(fill=tk.X)
            else:
                for item in content:
                    square = tk.Frame(area, width=120, height=60, bg=color, highlightbackground="black", highlightthickness=1)
                    square.pack(side=tk.LEFT, padx=2, pady=2)
                    square.pack_propagate(False)

                    tk.Label(square, text=item[0], bg=color, fg="white").pack(fill=tk.X)
                    tk.Label(square, text=f"arrive_time: [{item[1]}]", bg=color, fg="white").pack(fill=tk.X)
                    tk.Label(square, text=f"rest_time: [{item[2]}]", bg=color, fg="white").pack(fill=tk.X)

        # 更新 CPU 时钟显示
        self.cpu_clock_label.config(text=f"CPU_CLOCK: [{self.cpu_core.get_cpu_clock()}]")

    def toggle_auto_refresh(self):
        if self.auto_refresh:
            self.auto_refresh = False
            if self.auto_refresh_task:
                self.after_cancel(self.auto_refresh_task)
                self.auto_refresh_task = None
            self.auto_button.config(text="Auto Start")
        else:
            self.auto_refresh = True
            self.auto_button.config(text="Stop Auto")
            self.auto_refresh_content()

    def auto_refresh_content(self):
        if self.auto_refresh:
            self.refresh_content()
            self.auto_refresh_task = self.after(100, self.auto_refresh_content)

    def toggle_gen(self):
        self.auto_gen = not self.auto_gen
        if self.auto_gen:
            self.gen_button.config(text="Stop Gen")
        else:
            self.gen_button.config(text="Start Gen")
    
    def toggle_jam_waiting_list(self):
        self.cpu_core.jam_waiting_list = not self.cpu_core.jam_waiting_list
        if self.cpu_core.jam_waiting_list:
            self.unjam_button.config(text="Unjam Waiting List")
        else:
            self.unjam_button.config(text="Jam Waiting List")

    def set_interrupt(self):
        self.cpu_core.user_require_interrupt = True
        print("User interrupt requested")