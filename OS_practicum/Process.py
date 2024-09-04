"""
- 进程Process类:
- 构造需要进程名, 到达时间, 总时间, 归属队列id, 构造举例:
- process = Process(name='QQ', arrive_time=0, tot_time=5, que_id=1)
- 构造时会检查数据合法性

- 对外暴露的接口有:
- run_for_1clock(self), 进程运行一个时钟, 运行完会自动检查数据合法性
- get_pid, 返回pid
- get_que_id(self) -> int, 返回进程归属que_id
- is_dead(self) -> bool, 返回self._run_time == self._tot_time
- 一大堆time_get函数
- time_get_waiting(self) -> int, 等待时间
- time_get_rest(self) -> int, 距离完成任务剩余的时间
- time_get_arrive(self) -> int, 到达时间
- time_get_total(self) -> int, 总时间
- ime_get_run(self) -> int, 已经跑过的时间
- 这些函数在运行时候, 都会assert检查数据合法性

- 包含一个特殊的进程HANGING, 作为闲逛进程, 已经实例化
-
"""


class Process:
    # 自动增加的类变量(静态变量), 用以分配pid
    # 每次实例化自动+1
    _next_id = 0

    def __init__(self, name: str, arrive_time: int, tot_time: int, que_id: int):
        self._pid = Process._next_id  # 自动分配pid, 0已经分配给闲逛
        Process._next_id += 1

        self._name = name
        self._arrive_time = arrive_time
        self._tot_time = tot_time
        self._que_id = que_id

        self._run_time = 0  # 最开始已经运行时间是0
        self._check_consistency()

    def debug_brief(self):
        print(f'Process {self._name}:')
        print(f'pid={self._pid}, que_id={self._que_id}')
        print(f'arr_time={self._arrive_time}, tot_time={self._tot_time}, run_time={self._run_time}, rst_time={self.time_get_rest()}')

    def _check_consistency(self):
        assert self._pid >= 0 and self._arrive_time >= 0 and self._tot_time > 0 and self._run_time >= 0
        assert self._que_id >= 0
        assert isinstance(self._name, str)
        assert (self._tot_time - self._run_time >= 0)

    # 进程运行一个时钟单位
    def run_for_1clock(self):
        # assert self.run_time + add_time <= self.tot_time
        self._run_time += 1
        self._check_consistency()

    def get_pid(self) -> int:
        return self._pid

    def get_que_id(self) -> int:
        return self._que_id

    def get_name(self) -> str:
        return self._name

    # 是否已经完成
    def is_dead(self) -> bool:
        return self._run_time == self._tot_time

    # 很多关于时间的变量, 这里约定凡是查询时间的, 都用time_get开头的函数
    def time_get_waiting(self) -> int:
        def get_cpu_clock() -> int:
            import main
            return main.clock

        waiting_time = get_cpu_clock() - self._arrive_time
        assert waiting_time >= 0
        return waiting_time

    def time_get_rest(self) -> int:
        rest_time = self._tot_time - self._run_time
        assert rest_time >= 0
        return rest_time

    def time_get_arrive(self) -> int:
        assert self._arrive_time >= 0
        return self._arrive_time

    def time_get_total(self) -> int:
        assert self._tot_time >= 0
        return self._tot_time

    def time_get_run(self) -> int:
        assert self._run_time >= 0
        return self._run_time


# 闲逛进程
HANGING = Process(name='Hanging', arrive_time=0, tot_time=1, que_id=0)
