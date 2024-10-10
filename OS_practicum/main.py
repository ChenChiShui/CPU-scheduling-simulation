from ReadyQue import ReadyQue
from Process import Process
from CPU_Core import CPU_Core
from ProcessGenerator import ProcessGenerator

from MainWindow import MainWindow

if __name__ == '__main__':
    rq_fifo1 = ReadyQue(algo='FIFO', priority=0, time_clip=2)
    rq_fifo2 = ReadyQue(algo='FIFO', priority=0, time_clip=3)
    rq_sjf1 = ReadyQue(algo='SJF', priority=1, time_clip=1)
    rq_sjf2 = ReadyQue(algo='SJF', priority=1, time_clip=2)
    rq_hrrn = ReadyQue(algo='HRRN', priority=2, time_clip=1)
    rq_list = [rq_fifo1, rq_fifo2, rq_sjf1, rq_sjf2, rq_hrrn]
    
    cpu_core = CPU_Core(rq_list)
    process_generator = ProcessGenerator(rq_list)

    ls1 = [
        ['FIFO1', []], 
        ['FIFO2', []],
        ['SJF1', []],
        ['SJF2', []], 
        ['HRRN', []]
    ]
    ls2 = [
        ['Waiting Queue', []],
        ['CPU', []]
    ]

    app = MainWindow(ls1=ls1, ls2=ls2, cpu_core=cpu_core, process_generator=process_generator, rq_list=rq_list)
    app.mainloop()