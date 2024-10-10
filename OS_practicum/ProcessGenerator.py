from Process import Process
from ReadyQue import ReadyQue
import random

process_cnt = 0

class ProcessGenerator:
    def __init__(self, ls: list[ReadyQue]) -> None:
        self._rq_list = ls
    def run_for_1clk(self) -> None:
        n = len(self._rq_list)
        for que in self._rq_list:
            if random.randint(1, n + 1) % n == 0:
                from CPU_Core import CPU_core_clock
                global process_cnt
                process_cnt += 1
                t = random.randint(1, 3)
                que.offer(Process(name=f't{process_cnt}', arrive_time=CPU_core_clock, tot_time=t, que_id=0))