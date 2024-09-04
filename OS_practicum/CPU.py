import random
from time import sleep
from ReadyQue import ReadyQue
from Process import Process
from ReadyQue import HANGING

class CPU_class:
    def __init__(self, clock: int):
        self.clock = clock
        self.interrupt_status = True
        # 空闲英文 idle
        self.idle = True
        # 初始闲逛进程
        self.working_process = HANGING
        # 等待队列先放这里
        self.wait_queue = []
        self.ready_queues = {}
        self.creat_queue()
        pass

    # 此处设置初始样例
    def creat_queue(self):
        ready_que_sjf = ReadyQue(algo='SJF', priority=2, time_clip=5)
        ready_que_sjf.offer(Process(name='p1', arrive_time=3, tot_time=5, que_id=0))
        ready_que_sjf.offer(Process(name='p2', arrive_time=5, tot_time=2, que_id=0))
        ready_que_sjf.offer(Process(name='p3', arrive_time=6, tot_time=3, que_id=0))
        ready_que_sjf.offer(Process(name='p4', arrive_time=9, tot_time=1, que_id=0))
        self.ready_queues[0] = ready_que_sjf

        ready_que_fifo = ReadyQue(algo='FIFO', priority=1, time_clip=5)
        ready_que_fifo.offer(Process(name='pp1', arrive_time=3, tot_time=2, que_id=1))
        ready_que_fifo.offer(Process(name='pp2', arrive_time=5, tot_time=2, que_id=1))
        ready_que_fifo.offer(Process(name='pp3', arrive_time=6, tot_time=3, que_id=1))
        ready_que_fifo.offer(Process(name='pp4', arrive_time=9, tot_time=1, que_id=1))
        self.ready_queues[1] = ready_que_fifo


        self.ready_queues = dict(sorted(self.ready_queues.items(), key=lambda item: item[1].get_que_priority()))

    def clock_next(self) -> int:
        self.clock += 1
        print("clock:", self.clock)
        print("working_process:", self.working_process.get_name() if self.interrupt_status else "solving I/O")
        print("I/O:", self.interrupt_status)
        print("------------------")



        # 如果开中断
        if self.interrupt_status:
            # 此处添加维护一切信息的方法
            self.idle = True if self.working_process.is_dead() or self.working_process == HANGING else False

            # 如果 CPU 当前空闲
            if self.idle:
                self.get_next_process()

            # # 某种办法激活 io 现在先 random
            # if random.randint(1, 3) == 1:
            #     self.interrupt_happen(random.randint(1, 1))

            self.working_process.run_for_1clock()
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
            self.working_process = HANGING
            # 此处开始走时钟，但实际上啥也不变
            for i in range(interrupt_time):
                # 此处需要图形化？
                self.clock_next()
            target_queue_id = self.wait_queue[0].get_que_id()
            self.ready_queues[target_queue_id].offer(self.wait_queue[0])
            self.wait_queue.pop()
            self.get_next_process()
            self.interrupt_status = True
        else:
            # 表示在 io 中间来了另一个 io
            pass

    # 先遍历 ReadyQue 维护 idle
    # 在此处进行进程选择
    def get_next_process(self):
        n = len(self.ready_queues)
        solving_p = HANGING
        rest_time = 0
        # ready_queue 是按照优先级排序的
        for _, q in self.ready_queues.items():
            # 该队列中有元素
            if q.get_que_tot_time() > 0:
                solving_p, rest_time = q.pop()
                break
        self.working_process = solving_p
        return
