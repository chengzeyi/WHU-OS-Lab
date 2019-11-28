import re


# 银行家算法实现。
class BankerAlgo(object):
    def __init__(self):
        # 初始化可用资源。
        self.available = [3, 3, 2]
        # 初始化最大需求矩阵
        self.max = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
        # 初始化已分配矩阵。
        self.allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1],
                           [0, 0, 2]]
        # 初始化需求矩阵。
        self.need = [[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]]

    # 检查分配后是否处于安全状态。
    def check(self):
        safe_list = []
        # 初始化工作矩阵。
        work = self.available.copy()
        finish = [False for i in range(5)]
        while True:
            flag = False
            for i in range(5):
                # 判断当前进程没有完成且所需资源小于可分配资源。
                if not finish[i] and all(
                        map(lambda x, y: x <= y, self.need[i], work)):
                    # 重新设置可分配资源。
                    for m in range(3):
                        work[m] = work[m] + self.allocation[i][m]
                    finish[i] = True
                    flag = True
                    # 加入安全路径中。
                    safe_list.append(i)
                    break
            if not flag:
                break
        if False in finish:
            print("this status is not safe")
            return False
        else:
            print("solution found, safe list:\n" + str(safe_list))
            return True

    # 请求分配资源。
    def request(self, proc_index, res_nums):
        for res_type in range(3):
            res_num = res_nums[res_type]
            if res_num > self.need[proc_index][res_type]:
                print("error, requested resources are more than need")
                return False
            if res_num > self.available[res_type]:
                print("no enough resources left, failed to request")
                return False
        # 重新构造资源向量、分配矩阵、需求矩阵。
        for res_type in range(3):
            res_num = res_nums[res_type]
            self.available[res_type] -= res_num
            self.allocation[proc_index][res_type] += res_num
            self.need[proc_index][res_type] -= res_num
        if self.check():
            print("request succeeded")
            return True
        else:
            # 分配失败，恢复资源向量、分配矩阵、需求矩阵。
            for res_type in range(3):
                res_num = res_nums[res_type]
                self.available[res_type] += res_num
                self.allocation[proc_index][res_type] -= res_num
                self.need[proc_index][res_type] += res_num
            print("request failed")
            return False

    # 尝试结束进程。
    def try_finish_proc(self, proc_index):
        if all(map(lambda x: x == 0, self.need[proc_index])):
            print("peocess can be finished, free resources")
            for i in range(3):
                # 重新设置最大需求矩阵、可用资源向量、分配矩阵。
                self.max[proc_index][i] = 0
                self.available[i] += self.allocation[proc_index][i]
                self.allocation[proc_index][i] = 0
            return True
        else:
            print("process cannot be finished")
            return False

    # 显示当前所有进程和资源的状态。
    def show(self):
        print("available:\n" + str(self.available))
        print("max:\n" + str(self.max))
        print("allocation:\n" + str(self.allocation))
        print("need:\n" + str(self.need))


# 处理用户交互。
def main():
    banker_algo = BankerAlgo()
    print("this is the banker algorithm interactive interface")
    print("enter 'exit' to leave loop")
    print("enter 'show' to show current status")
    print(
        "enter 'request [process index] [res 0 num] [res 1 num] [res 2 num]' \
        to make a request")
    print("enter 'finish [process index]' to try finishing a process")
    while True:
        s = input()
        if re.match("exit$", s):
            break
        elif re.match("show$", s):
            banker_algo.show()
        elif re.match("request \\d+ \\d+ \\d+ \\d+$", s):
            s = s.split()
            banker_algo.request(int(s[1]), (int(s[2]), int(s[3]), int(s[4])))
        elif re.match("finish \\d+$", s):
            s = s.split()
            banker_algo.try_finish_proc(int(s[1]))
        else:
            print("invalid command")


if __name__ == "__main__":
    main()
