from Process import Process
from Process import HANGING
import random
import heapq
from typing import Optional

"""
- 就绪队列ReadyQue类:
- 构造需要算法('FIFO', 'SJF', 'HRRN'), 队列优先级(用于区分多级反馈队列), 队列时间片长度, 举例构造:
- ready_que = ReadyQue(algo='SJF', priority=2, time_clip=5), 约定优先级越小越优先
- 下划线开头的变量/方法都是私有的

- 对外暴露的接口有这些:
- offer(self, process: Process), 给当前队列加入一个进程
- pop(self) -> [Process, int], 当前队列根据算法弹出一个进程, 并返回计划时间片, 计划时间片是队列时间片和进程剩余时间的最小值
- get_que_tot_time(self) -> int, 返回队列中所有进程的剩余时间

- ReadyQue类里面没有que_id, 这个在主函数做比较好
- main里随意实例化几个que都可以, 然后主函数做个字典之类的, 来决定每个队列的id
"""


class _PCB:
    ...


class _PCBHeap:
    ...


class ReadyQue:
    # 构建一个就绪队列需要: 算法, 队列优先级, 时间片长度
    def __init__(self, algo: str, priority: int, time_clip: int):
        if algo != 'SJF' and algo != 'FIFO' and algo != 'HRRN':
            raise TypeError(f'{algo} is not a supported algorithm(FIFO, SJF, HRRN)')

        self._algorithm = algo
        self._que_priority = priority
        self._time_clip = time_clip

        self._pcb_heap = _PCBHeap()
        self._que_tot_time = 0

    # 将进程转换为pcb, 实际上是根据_algorithm变量打包一个优先级
    def _process2pcb(self, process: Process) -> _PCB:
        # 优先级越小, 越靠前, 这样heap时候就统一用小根堆了
        def get_priority(p: Process) -> float:
            if self._algorithm == 'FIFO':
                # 越早到达越优先
                return p.time_get_arrive()
            elif self._algorithm == 'SJF':
                # 剩余时间越少越优先
                return p.time_get_rest()
            elif self._algorithm == 'HRRN':
                # 响应比 = (等待时间 + 估计运行时间) / 估计运行时间
                # 估计运行时间在剩余时间上加一个[0, 1)的噪音来模拟, 不用负数防止出错
                runtime_assume = p.time_get_rest() + random.uniform(0, 1)
                response_ratio = (p.time_get_waiting() + runtime_assume) / runtime_assume
                # HRRN是最高相应比优先, 为了配合小根堆, 取个负数
                return -response_ratio

        return _PCB(process=process, priority=get_priority(process))

    # 向就绪队列中加入一个新的进程
    def offer(self, process: Process):
        pcb = self._process2pcb(process)
        self._pcb_heap.push(pcb)
        self._que_tot_time += process.time_get_rest()

    # 根据算法, 在队列中选择一个进程, 如果队列是空的, 返回一个闲逛进程的单例
    # 返回的是[进程, 计划时间]
    def pop(self) -> [Process, int]:
        top = self._pcb_heap.pop()
        # top是None的话, 返回一个T=1的闲逛进程
        if not top:
            return HANGING, 1
        self._que_tot_time -= top.process.time_get_rest()
        assert self._que_tot_time >= 0
        return top.process, min(self._time_clip, top.process.time_get_rest())

    def get_que_tot_time(self) -> int:
        return self._que_tot_time

    def get_que_priority(self) -> int:
        return self._que_priority

# 就绪队列里实际上是PCB,只有两个内容, 进程和优先级
# 就绪队列会对PCB的优先级建堆
class _PCB:
    def __init__(self, process: Process, priority: float):
        self.process = process
        self.priority = priority

    # 自定义比较函数lt == less than, 重载 <
    def __lt__(self, other):
        return self.priority < other.priority


# 一个只能接受PCB类型的小根堆
class _PCBHeap:
    def __init__(self):
        self._heap = []

    def push(self, pcb: _PCB) -> None:
        if not isinstance(pcb, _PCB):
            raise TypeError("Only PCB objects can be added to this heap")
        heapq.heappush(self._heap, pcb)

    def pop(self) -> Optional[_PCB]:
        if not self._heap:
            return None
        return heapq.heappop(self._heap)

    def peek(self) -> Optional[_PCB]:
        if not self._heap:
            return None
        return self._heap[0]

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)
