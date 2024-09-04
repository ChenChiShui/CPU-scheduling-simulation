from CPU import CPU
from ReadyQue import ReadyQue
from Process import Process
from Process import HANGING  # 闲逛进程
clock = int(1000)

readyQueue1 = ReadyQue("FIFO", 2, 1)
if __name__ == '__main__':
    # cpu = CPU(0)
    # for i in range(100):
    #     clock = cpu.clock_next()
    # print('main')

    # 这里测试功能
    print('======SJF======')
    ready_que_sjf = ReadyQue(algo='SJF', priority=2, time_clip=5)
    ready_que_sjf.offer(Process(name='p1', arrive_time=3, tot_time=5, que_id=0))
    ready_que_sjf.offer(Process(name='p2', arrive_time=5, tot_time=2, que_id=0))
    ready_que_sjf.offer(Process(name='p3', arrive_time=6, tot_time=3, que_id=0))
    ready_que_sjf.offer(Process(name='p4', arrive_time=9, tot_time=1, que_id=0))

    for i in range(10):
        top, t = ready_que_sjf.pop()
        top.debug_brief()
        print(f'time_clip={t}')
        print('---------------')

