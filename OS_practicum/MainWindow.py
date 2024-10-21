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
        self.open_random_interrupt = False

        # 设置窗口标题和大小
        self.title("操作系统课设——多级反馈队列调度模拟")
        self.geometry("900x700")
        self.configure(bg="#f0f0f0")  # 设置背景颜色

        # 初始化存储区域列表
        self.areas = []

        # 扩展渐变颜色列表
        self.area_colors = [
            "#0000FF", "#0033CC", "#0066CC", "#0099CC", "#00CCCC",
            "#00FFCC", "#33FFCC", "#66FFCC", "#99FFCC", "#CCFFCC",
            "#1E90FF", "#4169E1", "#4682B4", "#5F9EA0", "#6495ED",
            "#7B68EE", "#87CEFA", "#ADD8E6", "#B0C4DE", "#B0E0E6"
        ]

        # 创建样式
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=6, background='#4CAF50', foreground='white')
        style.configure('TLabel', font=('Arial', 12), padding=6, background='#f0f0f0')

        # 创建上部分区域
        for i, area_info in enumerate(ls1):
            self.create_area(i, area_info[0])

        # 创建下部分区域
        bottom_frame = ttk.Frame(self, padding=10)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)

        # 修改 ls2 的标签为 "waitQ" (等待队列)
        ls2[0][0] = "waitQ"

        for i, area_info in enumerate(ls2, start=len(ls1)):
            self.create_area(i, area_info[0], parent=bottom_frame, side=tk.LEFT, width=300, height=100)

        # 创建CPU时钟显示区域
        self.cpu_clock_frame = ttk.Frame(bottom_frame, borderwidth=2, relief="groove", width=180, height=100)
        self.cpu_clock_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.cpu_clock_frame.pack_propagate(False)
        self.cpu_clock_label = ttk.Label(self.cpu_clock_frame, text="CPU_CLOCK: []", font=('Arial', 16),
                                         background="#FF5733", foreground="white")
        self.cpu_clock_label.pack(expand=True)

        # 创建两个框架来容纳按钮
        button_frame1 = ttk.Frame(self, padding=10)
        button_frame1.pack(side=tk.BOTTOM, pady=(0, 5))

        button_frame2 = ttk.Frame(self, padding=10)
        button_frame2.pack(side=tk.BOTTOM, pady=(0, 10))

        # 定义统一的浅色系颜色
        button_color = "#ADD8E6"  # 这里使用浅蓝色作为统一颜色，你可以根据需求更改

        # 创建按钮
        tk.Button(button_frame1,
                  text='Next Clock',
                  command=self.refresh_content,
                  width=15,
                  height=2,
                  font=('Arial', 12),
                  bg="#4CAF50", fg="white", relief="raised"
                  ).pack(side=tk.LEFT, padx=5)

        self.auto_button = tk.Button(button_frame1,
                                     text='Auto Start',
                                     command=self.toggle_auto_refresh,
                                     width=15,
                                     height=2,
                                     font=('Arial', 12),
                                     bg="#4CAF50", fg="white", relief="raised"
                                     )
        self.auto_button.pack(side=tk.LEFT, padx=5)

        # 统一使用浅色系颜色（浅蓝色）
        tk.Button(button_frame2,
                  text='Add A Process',
                  command=self.add_process_dialog,
                  width=15,
                  height=2,
                  font=('Arial', 12),
                  bg=button_color, fg="black", relief="raised"
                  ).pack(side=tk.LEFT, padx=5)

        self.gen_button = tk.Button(button_frame2,
                                    text='Stop Gen',
                                    command=self.toggle_gen,
                                    width=15,
                                    height=2,
                                    font=('Arial', 12),
                                    bg=button_color, fg="black", relief="raised"
                                    )
        self.gen_button.pack(side=tk.LEFT, padx=5)

        self.unjam_button = tk.Button(button_frame2,
                                      text='Jam Waiting List',
                                      command=self.toggle_jam_waiting_list,
                                      width=15,
                                      height=2,
                                      font=('Arial', 12),
                                      bg=button_color, fg="black", relief="raised"
                                      )
        self.unjam_button.pack(side=tk.LEFT, padx=5)

        self.interrupt_button = tk.Button(button_frame2,
                                          text='Interrupt',
                                          command=self.set_interrupt,
                                          width=15,
                                          height=2,
                                          font=('Arial', 12),
                                          bg=button_color, fg="black", relief="raised"
                                          )
        self.interrupt_button.pack(side=tk.LEFT, padx=5)

        self.save_table_button = tk.Button(button_frame2,
                                           text='Save Table',
                                           command=self.save_table,
                                           width=15,
                                           height=2,
                                           font=('Arial', 12),
                                           bg=button_color, fg="black", relief="raised"
                                           )
        self.save_table_button.pack(side=tk.LEFT, padx=5)

        # 添加新的 "Open Random" 按钮，使用统一的浅色系
        self.random_button = tk.Button(button_frame2,
                                       text='Open Random: False',
                                       command=self.toggle_open_random,
                                       width=20,
                                       height=2,
                                       font=('Arial', 12),
                                       bg=button_color, fg="black", relief="raised"
                                       )
        self.random_button.pack(side=tk.LEFT, padx=5)

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

        # 创建一个装载标签和内容的框架
        container = ttk.Frame(area)
        container.pack(fill=tk.BOTH, expand=True)

        # 左侧为标签，设置为固定宽度
        label_frame = ttk.Frame(container, width=100)  # 固定宽度
        label_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        label_frame.pack_propagate(False)  # 禁止调整大小

        label_widget = ttk.Label(label_frame, text=label, font=('Arial', 12, 'bold'))
        label_widget.pack(expand=True, fill=tk.BOTH)

        # 右侧为进程内容
        inner_frame = ttk.Frame(container)
        inner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.areas.append(inner_frame)

    def add_process_dialog(self):
        # 获取进程名称
        while True:
            name = simpledialog.askstring("Input", "Enter process name:")
            if name is None:
                return  # 用户取消输入
            if name.strip() == "":
                messagebox.showerror("Error", "Process name cannot be empty. Please try again.")
                continue
            break

        # 获取进程的总运行时间
        while True:
            total_time = simpledialog.askinteger("Input", "Enter total time (must be an integer greater than 1):")
            if total_time is None:
                return  # 用户取消输入
            if not isinstance(total_time, int) or total_time <= 1:
                messagebox.showerror("Error", "Total time must be an integer greater than 1. Please try again.")
                continue
            break

        # 获取队列编号（1-5）
        while True:
            queue_number = simpledialog.askinteger("Input", "Enter queue number (1-5):")
            if queue_number is None:
                return  # 用户取消输入
            if queue_number not in range(1, 6):
                messagebox.showerror("Error", "Queue number must be between 1 and 5. Please try again.")
                continue
            break

        # 获取当前 CPU 时钟时间
        t = self.cpu_core.get_cpu_clock()

        # 创建进程对象，队列ID设为用户选择的队列编号减1（因为队列通常从0开始）
        p = Process(name=name, arrive_time=t, tot_time=total_time, que_id=queue_number - 1)

        # 将进程添加到指定的队列中
        self.rq_list[queue_number - 1].offer(p)

        print(f"Adding new process: Name = {name}, Total Time = {total_time}, Queue = {queue_number}")

    def refresh_content(self):
        self.cpu_core.run_for_1clk()
        if self.auto_gen:
            self.process_generator.run_for_1clk()

        # 更新队列信息
        for i in range(5):
            self.ls1[i][1] = self.rq_list[i].get_que_list()
        # 更新等待列表
        self.ls2[0][1] = self.cpu_core.get_waiting_list()
        # 更新当前CPU正在处理的进程
        self.ls2[1][1] = self.cpu_core.get_now_onboard()

        for i, area in enumerate(self.areas):
            # 清理现有的内容
            for widget in area.winfo_children():
                widget.destroy()

            if i < len(self.ls1):
                content = self.ls1[i][1]
            else:
                content = self.ls2[i - len(self.ls1)][1]

            color = self.area_colors[i % len(self.area_colors)]

            # CPU区域的特殊处理
            if i == len(self.areas) - 1:
                if content:
                    item = content[0]
                    if item[0] == 'HANGING':
                        square_color = 'green'
                    elif 'Interrupt' in item[0]:
                        square_color = 'red'
                    else:
                        square_color = '#FFDAB9'  # 浅橙色 (PeachPuff)

                    square = tk.Frame(area, width=120, height=60, bg=square_color, highlightbackground="black",
                                      highlightthickness=1)
                    square.pack(expand=True)
                    square.pack_propagate(False)

                    tk.Label(square, text=item[0], bg=square_color, fg="white").pack(fill=tk.X)
                    tk.Label(square, text=f"arrive_time: [{item[1]}]", bg=square_color, fg="white").pack(fill=tk.X)
                    tk.Label(square, text=f"rest_time: [{item[2]}]", bg=square_color, fg="white").pack(fill=tk.X)
            else:
                # 普通区域的进程展示
                for item in content:
                    square = tk.Frame(area, width=120, height=60, bg=color, highlightbackground="black",
                                      highlightthickness=1)
                    square.pack(side=tk.LEFT, padx=2, pady=2)
                    square.pack_propagate(False)

                    # 显示进程名、到达时间和剩余时间
                    tk.Label(square, text=item[0], bg=color, fg="white").pack(fill=tk.X)
                    tk.Label(square, text=f"arrive_time: [{item[1]}]", bg=color, fg="white").pack(fill=tk.X)
                    tk.Label(square, text=f"rest_time: [{item[2]}]", bg=color, fg="white").pack(fill=tk.X)

        # 更新CPU时钟显示
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

    def toggle_open_random(self):
        # 切换 open_random 的布尔值
        self.cpu_core.open_random_interrupt = not self.cpu_core.open_random_interrupt
        # 更新按钮的文本
        self.random_button.config(text=f"Random Interrupt: {self.cpu_core.open_random_interrupt}")