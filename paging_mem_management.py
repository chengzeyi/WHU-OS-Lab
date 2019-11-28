# 比特位的表示。
class Bit(object):
    def __init__(self):
        self.value = "0"

    def __str__(self):
        return self.value


# 字节的表示。
class Byte(object):
    def __init__(self):
        self.bits = [Bit() for i in range(8)]

    def __str__(self):
        s = ""
        for bit in self.bits:
            s += str(bit)
        return s


# 位示图的表示。
class BitMap(object):
    def __init__(self, byte_num):
        self.byte_num = byte_num
        self.storage = [Byte() for i in range(byte_num)]

    # 获得一个比特的值。
    def get_bit(self, index, offset):
        return self.storage[index].bits[offset].value

    # 设置一个比特为0。
    def set_bit0(self, index, offset):
        self.storage[index].bits[offset].value = "0"

    # 设置一个比特为1.
    def set_bit1(self, index, offset):
        self.storage[index].bits[offset].value = "1"

    # 获得位示图的描述。
    def __str__(self):
        s = "<BitMap|storage:"
        for byte in self.storage:
            s += str(byte)
        s += ">"
        return s


# 页表的表示。
class PageTable(object):
    def __init__(self, size):
        self.page2block = [-1 for i in range(size)]
        self.size = size

    # 设置页表中的一项。
    def set_page(self, page_index, block_index):
        self.page2block[page_index] = block_index

    # 获得页表中的一项。
    def get_page(self, page_index):
        return self.page2block[page_index]

    # 获得页表的状态描述。
    def __str__(self):
        s = "<PageTable|size:" + str(self.size) + "|"
        for i in range(self.size):
            s += ("[" + str(i) + "->" + str(self.page2block[i]) + "]")
        s += ">"
        return s


# 内存管理装置。
class MemManager(object):
    def __init__(self, byte_num):
        self.bitmap = BitMap(byte_num)
        self.page_tables = []
        self.total_blocks = byte_num * 8
        self.free_blocks = self.total_blocks

    # 分配内存。
    def alloc(self, size):
        # 所要分配的内存大于剩余空闲内存。
        if size > self.free_blocks:
            print("no enough free blocks, failed to allocate")
            return False
        free_blocks = []
        # 遍历位示图，寻找可分配的内存。
        for index in range(self.bitmap.byte_num):
            for offset in range(8):
                if self.bitmap.get_bit(index, offset) == "0":
                    free_blocks.append(index * 8 + offset)
        # 建立页表。
        page_table = PageTable(size)
        # 设置页表。
        for page_index in range(size):
            block_index = free_blocks[page_index]
            page_table.set_page(page_index, block_index)
            self.bitmap.set_bit1(block_index // 8, block_index % 8)
        # 将页表加入内存管理器中。
        self.page_tables.append(page_table)
        self.free_blocks -= size
        print("allocation finished, page table info:\n" + str(page_table))
        return True

    # 回收内存。
    def free(self, page_table_index):
        # 取得页表。
        page_table = self.page_tables[page_table_index]
        print("info of the page table to free:\n" + str(page_table))
        # 回收页表中分配的内存。
        for page_index in range(page_table.size):
            block_index = page_table.get_page(page_index)
            self.bitmap.set_bit0(block_index // 8, block_index % 8)
            page_table.set_page(page_index, -1)
        self.free_blocks += page_table.size
        self.page_tables.pop(page_table_index)

    # 打印当前内存管理器的状态。
    def show(self):
        print("bitmap:\n" + str(self.bitmap))
        print("page tables:")
        for page_table in self.page_tables:
            print(str(page_table))


# 处理用户交互。
def main():
    mem_manager = MemManager(8)
    print("this is the memory management interface")
    print("to show current status, enter 'show'")
    print("to allocate, snter 'alloc [size]'")
    print("to free, enter 'free [page_table_index]")
    print("to exit, enter 'exit'")
    while True:
        s = input().split()
        if s[0] == "exit":
            break
        elif s[0] == "show":
            mem_manager.show()
        elif s[0] == "alloc":
            size = int(s[1])
            mem_manager.alloc(size)
        elif s[0] == "free":
            page_table_index = int(s[1])
            mem_manager.free(page_table_index)
        else:
            print("unknown commamd")


if __name__ == "__main__":
    main()
