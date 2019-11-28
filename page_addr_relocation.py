import re


# 页表结构。
class PageTable(object):
    def __init__(self, size):
        # 定义-1代表空值。
        self.page2block = [-1 for i in range(size)]
        self.size = size

    # 设定页表中的一项。
    def set_page(self, page_index, block_index):
        self.page2block[page_index] = block_index

    # 获得页表中的一项。
    def get_page(self, page_index):
        return self.page2block[page_index]

    # 显示当前页表状态。
    def __str__(self):
        s = "<PageTable|size:" + str(self.size) + "|"
        for i in range(self.size):
            s += ("[" + str(i) + "->" + str(self.page2block[i]) + "]")
        s += ">"
        return s


# 虚拟地址到物理地址转换系统。
class V2R(object):
    def __init__(self, page_table_size):
        # 初始化页表。
        self.page_table = PageTable(page_table_size)

    # 尝试进行转换。
    def try_v2r(self, page_index, offset):
        block_index = self.page_table.get_page(page_index)
        if block_index == -1:
            print(
                "missing page, cannot convert virtual address to real address")
        else:
            print("page found, block index is " + str(block_index) +
                  ", offset is " + str(offset))

    # 设置页表中的一项。
    def set_v2r(self, page_index, block_index):
        self.page_table.set_page(page_index, block_index)
        print("set page comvertion, page_index is " + str(page_index) +
              ", block index is " + str(block_index))

    # 显示当前虚拟地址到物理地址转换状态。
    def show(self):
        print(str(self.page_table))


# 处理用户交互。
def mian():
    v2r = V2R(32)
    print("this is the vaddr to raddr convertion interactive interface")
    print("enter 'exit' to leave loop")
    print("enter 'show' to see current page table")
    print("enter 'set [page_index] [block_index]' to set page table")
    print("enter 'try [page_index] [offset]' to make a convertion")
    while True:
        s = input()
        if re.match("exit$", s):
            break
        elif re.match("show$", s):
            v2r.show()
        elif re.match("set \\d+ \\d+$", s):
            s = s.split()
            v2r.set_v2r(int(s[1]), int(s[2]))
        elif re.match("try \\d+ \\d+$", s):
            s = s.split()
            v2r.try_v2r(int(s[1]), int(s[2]))
        else:
            print("invalid command")


if __name__ == "__main__":
    mian()
