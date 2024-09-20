from ReadyQue import ReadyQue
from Process import Process
from typing import Any
from typing import List
from typing import Union
import random

CPU_core_clock = 0

class CPU_Core:
    def __init__(self, que_list: List[ReadyQue]) -> None:
        if not que_list:
            raise ValueError(f'Waiting queue list cannot be empty!')
        
        self._que_list = que_list
        self._process_on_core: Process = None
        self._scheduled_time = 0 # 当前进程计划再跑多长时间
        self._open_4interrupt = True # 初始情况可以中断

        # 等待队列用来存放被打断的进程, 等待队列出来的进程不会上cpu, 而是回到ReadyQue
        self._waiting_list = ReadyQue(algo='FIFO', priority=0, time_clip=1) 

    # if que 有问题
    def _get_next_process(self) -> Union[Process, int]:
        for que in self._que_list:
            if que:
                return que.pop()
        return self._que_list[0].pop()
            
    
    def run_for_1clk(self) -> None:
        """
        每个时钟都要做这些事:
        - 时钟加1
        - 维护队列内所有任务的信息
        - 检查当前任务, 如果做完了, 丢弃掉
            - 如果这个任务是中断, 唤醒等待队列头, 开中断
        - 如果当前有中断, 且开中断
            - 发生抢占, 现在跑的任务(如果有)拿到waiting_list
            - 中断上CPU
            - 关中断
        - 否则在等待队列里取出一个任务
        - 当前的任务跑一个时钟
        - 打印这个时钟的报告信息
        """
        global CPU_core_clock
        CPU_core_clock += 1
        # for que in self._que_list:
        #     que.maintain(CPU_core_clock)
        if self._scheduled_time <= 0:
            # 如果当前进程时间耗尽
            if self._process_on_core and self._process_on_core.get_name().startswith("Interrupt"):
                # 如果做完的任务是中断, 唤醒, 开中断
                self._awake_waiting_list()
                self._open_4interrupt = True
            self._throw_away()
            interrupt, scheduled_time = self._interrupt_happen()
            if interrupt != None and self._open_4interrupt:
                # 如果来了新中断, 且开中断, 就安排新中断
                self._scheduled_time = scheduled_time
                self._process_on_core = interrupt
                self._open_4interrupt = False
            if not self._process_on_core:
                # 如果还没事做, 就问反馈队列要一个
                self._process_on_core, self._scheduled_time = self._get_next_process()
        # 跑一个时钟
        self._scheduled_time -= 1
        self._process_on_core.run_for_1clock()
        self._brief()
                
    # 打印当前时钟的进程信息
    def _brief(self):
        global CPU_core_clock
        print(f'clock {CPU_core_clock}: {self._process_on_core.get_name()}, ', end='')
        print(f'scheduled_time={self._scheduled_time}')       

    # 唤醒一个等待队列的进程     
    def _awake_waiting_list(self):
        if self._waiting_list:
            process, _ = self._waiting_list.pop()
            self._que_list[0].offer(process=process)            

    # 丢弃当前在CPU上的进程到统计列表
    def _throw_away(self):
        self._process_on_core = None
        ...    
                
    # 返回None, None 或者[Process, int]
    def _interrupt_happen(self):
        global CPU_core_clock
        if random.randint(1, 3) == 1:
            t = random.randint(1, 5)
            return Process(name="Interrupt", arrive_time=CPU_core_clock, tot_time=t, que_id=0), t
        return None, None
