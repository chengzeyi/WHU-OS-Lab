# 磁盘管理器。
class DiskManager(object):
    def __init__(self):
        # 初始化超级块。
        self.super = [3, 0, 1, 2]
        # 初始化磁盘空间。
        self.disk_space = [[3, 3, 4, 5], [0, 0, -0, -0], [0, 0, 0, 0],
                           [3, -1, 6, 7], [0, 0, 0, 0], [0, 0, 0, 0],
                           [0, 0, 0, 0], [0, 0, 0, 0]]
        self.total = 8
        # 记录已分配的块。
        self.allocated_list = []

    # 获得已经分配的块的数量。
    @property
    def allocated_num(self):
        return len(self.allocated_list)

    # 显示当前磁盘管理器的状态。
    def show(self):
        print("super:\n" + str(self.super))
        print("disk space:\n" + str(self.disk_space))
        print("allocated list:\n" + str(self.allocated_list))

    # 分配磁盘块。
    def assign(self):
        # 判断当前超级快是否为空。
        if self.super[0] > 1:
            print("super is not empty, no need to switch")
            # 获得要分配的磁盘块号。
            block_index = self.super[self.super[0]]
            # 将这个块加入已分配列表中。
            self.allocated_list.append(block_index)
            self.super[0] -= 1
            print("assignment finished, block index is " + str(block_index))
            return True
        elif self.super[0] == 1 and self.super[1] != -1:
            print("super is empty, switch it")
            # 获得要分配的磁盘块号。
            block_index = self.super[1]
            # 将这个块加入已分配列表中。
            self.allocated_list.append(block_index)
            for i in range(4):
                self.super[i] = self.disk_space[block_index][i]
            print("assignment finished, block index is " + str(block_index))
            return True
        else:
            # 没有可分配的磁盘块。
            print("assignment failed, no free block")
            return False

    # 释放指定的磁盘块。
    def free(self, block_index):
        if block_index not in self.allocated_list:
            print("cannot free, block index is not in the allocated list")
            return False
        self.allocated_list.remove(block_index)
        if self.super[0] < 3:
            print("super is not full, no need to switch")
            self.super[self.super[0] + 1] = block_index
            self.super[0] += 1
        else:
            print("super is full, switch it")
            # 切换超级快的内容。
            for i in range(4):
                self.disk_space[block_index][i] = self.super[i]
                self.super[0] = 1
                self.super[1] = block_index
        print("finished to free disk block, block index is " +
              str(block_index))
        return True


# 处理用户交互。
def main():
    disk_manager = DiskManager()
    print("this is the disk manager interactive interface")
    print("enter 'exit' to leave loop")
    print("enter 'show' to see current status")
    print("enter 'assign' to make assignment")
    print("enter 'free [block index]' to free a specific block")
    while True:
        s = input().split()
        if s[0] == "exit":
            break
        elif s[0] == "show":
            disk_manager.show()
        elif s[0] == "assign":
            disk_manager.assign()
        elif s[0] == "free":
            disk_manager.free(int(s[1]))
        else:
            print("unknown command")


if __name__ == "__main__":
    main()
