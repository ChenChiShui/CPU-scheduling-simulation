class Process:
    # 构造一个进程需要这些信息: id, 名字, 总时间, 初始队列ID
    # 除此之外, 还有已经运行的时间, 颜色, 和各种表格信息
    def __init__(self, id:int, name:str, tot_time:int, que_id:int):
        self.id = id
        self.name = name
        self.tot_time = tot_time
        self.que_id = que_id

        self.run_time = 0 # 最开始已经运行时间是0

    # 进程运行一段时间, 如果超过总时间会报错
    def run(self, add_time:int):
        # assert self.run_time + add_time <= self.tot_time
        self.run_time += add_time

    def get_rest_time(self) -> int:
        rest_time = self.tot_time - self.run_time
        assert rest_time >= 0
        return rest_time

    def get_que_id(self) -> int:
        return self.que_id

