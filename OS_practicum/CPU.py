import random
from time import sleep
# from ReadyQue import readyQueue1
from ReadyQue import ReadyQue
from Process import Process

class CPU:
    def __init__(self, clock: int):
        self.clock = clock
        self.interrupt_status = True
        # 空闲英文 idle
        self.idle = True
        # 初始闲逛进程
        self.working_process = Process(0, "init", 0, 0, 0)
        # 等待队列先放这里
        self.wait_queue = []
        pass

    def clock_next(self) -> int:
        self.clock += 1
        print("clock:", self.clock)
        print("working_process:", self.working_process.id if self.interrupt_status else "solving I/O")
        print("I/O:", self.interrupt_status)
        print("------------------")

        # 如果开中断
        if self.interrupt_status:
            # 此处添加维护一切信息的方法

            # 如果 CPU 当前空闲
            if self.idle:
                self.get_next_process()
            # 某种办法激活 io 现在先 random

            if random.randint(1, 3) == 1:
                self.interrupt_happen(random.randint(1, 1))
            pass

        sleep(1)
        # 调试信息

        return self.clock

    def get_interrupt_status(self) -> bool:
        return self.interrupt_status

    def get_idle(self) -> bool:
        return self.idle

    # io 开始，传入 io 所需时间
    def interrupt_happen(self, interrupt_time: int):
        if self.interrupt_status :
            self.interrupt_status = False
            self.wait_queue.append(self.working_process)
            self.working_process = Process(0, "init", 0, 0, 0)
            # 此处开始走时钟，但实际上啥也不变
            for i in range(interrupt_time):
                # 此处需要图形化？
                self.clock_next()
            target_queue = self.wait_queue[0].get_que_id
            # -----------
            # 此处还要维护 wait_queue[0] 回到 ready_queue
            # -----------
            self.get_next_process()
            self.interrupt_status = True
        else:
            # 表示在 io 中间来了另一个 io
            pass

    # 先遍历 ReadyQue 维护 idle
    # 在此处进行进程选择
    def get_next_process(self):
        # ------------ 下面是一个例子
        import main
        p = main.readyQueue1.pop()
        self.working_process = p
        p.run(self.clock)
        return
