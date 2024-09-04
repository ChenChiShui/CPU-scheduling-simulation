from CPU import CPU_class
from ReadyQue import ReadyQue
from Process import Process

from Process import HANGING  # 闲逛进程
clock = int(1000)

readyQueue1 = ReadyQue("FIFO", 2, 1)
if __name__ == '__main__':

    cpu = CPU_class(0)
    for i in range(100):
        clock = cpu.clock_next()
    print('main')

    # for i in range(10):
    #     top, t = ready_que_sjf.pop()
    #     top.debug_brief()
    #     print(f'time_clip={t}')
    #     print('---------------')

