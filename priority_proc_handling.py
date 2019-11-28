class PCB(object):
    # 初始化PCB，定义0为最高优先级，31为最低优先级。
    def __init__(self, name, required, priority):
        if priority < 0 or priority > 31:
            raise ValueError("priority must be in range 0-31")
        self.name = name
        self.required = required
        self.priority = priority
        self.status = "R"
        self.obtained = 0

    # 运行一个时间单位。
    def run_one_time(self):
        if self.status == "E":
            return False
        self.obtained += 1
        if self.priority < 31:
            self.priority += 1
        if self.obtained >= self.required:
            self.status = "E"
            return False
        return True

    # 判断该进程是否已经运行完毕。
    def isOver(self):
        return self.obtained >= self.required

    # 获得当前PCB的描述。
    def __str__(self):
        return "<PCB|name:" + self.name + "|required:" + str(
            self.required) + "|obtained:" + str(
                self.obtained) + "|priority:" + str(
                    self.priority) + "|status:" + self.status + ">"


class PriorityQueue(object):
    # 初始化优先队列。
    def __init__(self, start, stop):
        if stop <= start:
            raise ValueError("stop not greater than start")
        self.start = start
        self.stop = stop
        self.queue = [[] for i in range(start, stop)]
        self.size = 0

    # 向队列中加入一个PCB。
    def add(self, pcb):
        if pcb.priority < self.start or pcb.priority >= self.stop:
            raise ValueError("priority of pcb must be in range(start, stop)")
        self.queue[pcb.priority - self.start].append(pcb)
        self.size += 1

    # 判断队列是否为空。
    def is_empty(self):
        return self.size == 0

    # 从队列中取出一个具有最高优先级且最先进入队列的PCB。
    def select(self):
        for single_queue in self.queue:
            if single_queue:
                return single_queue[0]

    # 从队列中取出一个具有最高优先级且最先进入队列的PCB，
    # 并将其从队列中移出。
    def select_and_remove(self):
        for single_queue in self.queue:
            if single_queue:
                pcb = single_queue[0]
                single_queue.pop(0)
                self.size -= 1
                return pcb

    # 获得当前优先队列的描述信息。
    def __str__(self):
        s = "<PriorityQueue|start:" + str(self.start) + "|stop:" + str(
            self.stop) + "|size:" + str(self.size)
        for single_queue in self.queue:
            for pcb in single_queue:
                s += ("\n" + str(pcb))
        s += ">"
        return s


class ProcHandler(object):
    # 初始化处理机调度器。
    def __init__(self):
        self.priority_queue = PriorityQueue(0, 32)

    # 加入一个进程。
    def add(self, pcb):
        print("add PCB to priority queue, PCB info:\n" + str(pcb))
        self.priority_queue.add(pcb)

    # 选择一个合适的进程，运行一个时间单位。
    def run_one_time(self):
        if self.priority_queue.is_empty():
            print("priority queue is empty, cannot run one time")
            return False
        print("current priority queue:\n" + str(self.priority_queue))
        pcb = self.priority_queue.select_and_remove()
        print("ready to run one time, process info:\n" + str(pcb))
        if pcb.run_one_time():
            print("precess unfinished, back to the priority queue")
            self.priority_queue.add(pcb)
        else:
            print("process finished")
        return True

    # 持续运行。
    def run(self):
        while self.run_one_time():
            pass


# 用户交互界面，提示用户输入并处理。
def main():
    proc_handler = ProcHandler()
    count = 0
    print("enter process' priority and required time, format:")
    print("[priority] [required time]")
    print(
        "note that priority must be in range 0-31, and required time cannot be \
        negative")
    while True:
        count += 1
        print("type q to leave loop")
        s = input()
        if s == "q":
            break
        priority, required = s.split()
        priority = int(priority)
        required = int(required)
        name = "p" + str(count)
        pcb = PCB(name, required, priority)
        proc_handler.add(pcb)
    print("processes started to run, press enter to run one time")
    while True:
        input()
        if not proc_handler.run_one_time():
            break


if __name__ == "__main__":
    main()
