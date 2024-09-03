# 就绪队列类, 算法有FIFO, SFU,


from Process import Process
class ReadyQue:
    # 构建一个就绪队列需要: 算法, 队列优先级
    def __init__(self, algo:str, priority:int):
        self.algorithm = algo
        self.priority = priority

        self.ready_list = []
        self.que_tot_time = 0

    # 向就绪队列中加入一个新的进程
    def offer(self, proccess:Process):
        self.ready_list.append(proccess)
        self.que_tot_time += proccess.get_rest_time()

    # 根据算法, 在队列中选择一个进程, 如果队列是空的, 返回一个闲逛进程的单例
    def pop(self) -> Process:
        return Process(1084, "TEST", 3, 1)

    def get_que_tot_time(self) -> int:

        return self.que_tot_time

readyQueue1 = ReadyQue("FIFO", 1)