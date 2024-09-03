from CPU import CPU
clock = int(0)
if __name__ == '__main__':
    cpu = CPU(0)
    for i in range(100):
        clock = cpu.clock_next()
    print('main')