from ReadyQue import ReadyQue
from Process import Process
from CPU_Core import CPU_Core
from ProcessGenerator import ProcessGenerator


if __name__ == '__main__':
    rq_fifo = ReadyQue(algo='FIFO', priority=0, time_clip=2)
    rq_sjf = ReadyQue(algo='SJF', priority=1, time_clip=1)
    rq_hrrn = ReadyQue(algo='HRRN', priority=2, time_clip=1)
    rq_list = [rq_fifo, rq_sjf, rq_hrrn]
    cpu_core = CPU_Core(rq_list)
    process_generator = ProcessGenerator(rq_list)

    for t in range(100):
        cpu_core.run_for_1clk()
        process_generator.run_for_1clk()
    

