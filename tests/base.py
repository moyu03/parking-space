import os
import sys
"""
停车场管理系统详细设计
数据结构：
1.Stack类 - 模拟停车场（顺序存储）
2.Queue类 - 模拟便道（链式存储）
3.ParkingSystem类 - 系统主控（组合模式）
"""

class Stack:
    """停车场栈实现（顺序结构）"""
    def __init__(self, size):
        """
        初始化停车场
        :param size: 停车场容量（车位数）
        """
        self.carNumber = [0] * 100  # 车牌号存储数组，最多100辆车
        self.arriveTime = [0] * 100  # 车辆到达时间数组
        self.top = -1  # 栈顶指针（-1表示空栈）
        self.size = size  # 停车场容量

    # 检查栈（停车场）是否为空
    def emptyStack(self):
        return self.top == -1

    # 检查栈（停车场）是否已满
    def isFull(self):
        return self.top == self.size - 1

    # 入栈操作
    def push(self, carNumber, arriveTime):
        """
        车辆进入停车场
        :param carNumber: 车牌号
        :param arriveTime: 进入时间
        """
        self.top += 1
        self.carNumber[self.top] = carNumber
        self.arriveTime[self.top] = arriveTime

    # 出栈操作
    def pop(self):
        """
        车辆离开停车场
        返回: （车牌号，到达时间）
        """
        if self.emptyStack():
            return None, None
        carNumber = self.carNumber[self.top]
        arriveTime = self.arriveTime[self.top]
        self.top -= 1
        return carNumber, arriveTime


class qNode:
    """便道节点（链式结构基础单元）"""
    def __init__(self, carNumber, arriveTime):
        """
        初始化便道节点
        :param carNumber: 车牌号
        :param arriveTime: 进入便道时间
        """
        self.carNumber = carNumber
        self.arriveTime = arriveTime
        self.next = None


class Queue:
    """便道队列实现（链式结构）"""
    def __init__(self):
        """初始化便道"""
        self.front = qNode(0, 0)  # 头节点
        self.rear = self.front # 尾指针初始化
        self.position = 0  # 便道位置计数器

    # 检查队列（便道）是否为空
    def emptyQueue(self):
        return self.front == self.rear

    # 入队操作
    def enqueue(self, carNumber, arriveTime):
        """
        车辆进入便道（队尾插入）
        :param carNumber: 车牌号
        :param arriveTime: 进入时间
        """
        new_node = qNode(carNumber, arriveTime)
        self.rear.next = new_node
        self.rear = new_node
        self.position += 1

    # 出队操作
    def dequeue(self):
        """
        车辆离开便道（队首移除）
        返回: （车牌号，到达时间）
        """
        if self.emptyQueue():
            return None, None

        temp = self.front.next
        carNumber = temp.carNumber
        arriveTime = temp.arriveTime

    # 更新队列指针
        if temp == self.rear:
            self.rear = self.front # 队列空时重置
        self.front.next = temp.next
        self.position -= 1 # 更新便道车辆计数
        return carNumber, arriveTime


class ParkingSystem:
    """停车场系统主控类"""
    def __init__(self):
        """系统初始化"""
        # 系统配置参数
        self.parkingSize = 0 # 停车场容量
        self.parkingFee = 0 # 停车场费率（元/小时）
        self.pavementFee = 0 # 便道费率（元/小时）
        # 状态跟踪变量
        self.position = 0 # 便道位置计数器
        self.count = 0 # 便道车辆计数器
        self.time = [] # 便道车辆车牌记录
        self.stopTime = [] # 便道车辆离开时间记录
        self.startTime = [] # 便道车辆进入时间记录

        # 初始化停车场和临时栈
        self.S = Stack(0) # 停车场栈（初始容量0）
        self.LS = Stack(0) # 临时栈（让路车辆暂存）
        self.Q = Queue() # 便道队列

    # 验证输入是否为有效数字
    def validNumber(self, input_str):
        try:
            num = int(input_str)
            return True, num
        except ValueError:
            return False, 0

    # 检查停车场是否已有该车辆
    def judgeParking(self, state, carNumber):
        if state != 'A':
            return True

        for i in range(self.S.top + 1):
            if carNumber == self.S.carNumber[i]:
                print("停车场里已经有该车，请重新进入输入界面！")
                return False
        return True

    # 检查便道是否已有该车辆
    def judgePavement(self, state, carNumber):
        if state != 'A':
            return True

        current = self.Q.front.next
        while current:
            if carNumber == current.carNumber:
                print("便道上已经有该车，请重新进入输入界面！")
                return False
            current = current.next
        return True

    # 核心算法模块
    def load(self):
        """
        功能1：车辆进出管理
        算法流程：
        1.输入车辆状态（A/D）、车牌号、时间
        2.A状态处理：
          2.1 停车场未满：入栈（S.push）
          2.2 停车场已满：入队（Q.enqueue）
        3.D状态处理：
          3.1 定位目标车辆（暂存让路车辆到临时栈）
          3.2 计算停留时间和费用
          3.3 让路车辆归位
          3.4 便道车辆补位
        4.E状态：返回主菜单
        """
        print("请输入车的状态（A进站/D出站），车牌号(整数) 和 时间整数（进站时间/出站时间）：")
        print("输入 E 0 0 结束输入\n")

        while True:
            data = input().split()
            if not data:
                continue

            if len(data) < 3:
                print("输入格式错误，请重新输入")
                continue

            state = data[0].upper()
            carNum_str, time_str = data[1], data[2]

            # 验证车牌号和时间
            valid_car, carNumber = self.validNumber(carNum_str)
            valid_time, arriveTime = self.validNumber(time_str)

            if not valid_car or not valid_time:
                print("*** 输入内容不为数字，不符合要求，请重新输入! ***")
                continue

            if state == 'E':
                break

            # 验证车辆是否已存在
            if not self.judgeParking(state, carNumber) or not self.judgePavement(state, carNumber):
                continue

            # 车辆进入处理
            if state == 'A':
                # 停车场未满：直接进入
                if not self.S.isFull() and self.S.size > 0:
                    self.S.push(carNumber, arriveTime)
                    print(f"车牌号是 {carNumber} 的车停在停车场的位置是 {self.S.top + 1}")
                # 停车场已满：进入便道
                else:
                    print(f"当前车子进入便道 = {self.count}")
                    # 记录便道车辆时间信息
                    self.startTime.append(arriveTime)
                    self.time.append(carNumber)
                    self.count += 1
                    self.Q.enqueue(carNumber, arriveTime)
                    print(f"车牌号是 {carNumber} 的车在便道的位置是 {self.Q.position}")

            # 车辆离开处理
            elif state == 'D':
                # 检查车辆是否在停车场
                found = False
                for i in range(self.S.top + 1):
                    if self.S.carNumber[i] == carNumber:
                        found = True
                        break

                if not found:
                    print(f"停车场无车牌号为 {carNumber} 的车！")
                    continue

                # 处理车辆离开
                temp_stack = Stack(self.S.size)
                current_car = None
                current_time = None

                # 寻找目标车辆
                while not self.S.emptyStack():
                    car, time_val = self.S.pop()
                    # 找到目标车辆
                    if car == carNumber:
                        current_car, current_time = car, time_val
                        break
                    # 未找到则暂存让路车辆
                    temp_stack.push(car, time_val)

                # 将临时栈中的车辆移回停车场
                while not temp_stack.emptyStack():
                    car, time_val = temp_stack.pop()
                    self.S.push(car, time_val)

                if current_car is not None:
                    # 计算便道停留费用
                    fee_paid = False
                    for i in range(self.count):
                        if carNumber == self.time[i]:
                            stay_time = arriveTime - self.startTime[i]
                            print(
                                f"车牌号是 {carNumber} 的车离开便道，停留时间是：{stay_time}小时，共花费了 {self.pavementFee * stay_time} 元。")
                            fee_paid = True
                            break

                    # 计算停车场费用
                    stay_time = arriveTime - current_time
                    print(
                        f"车牌号是 {carNumber} 的车离开停车场，停留时间是：{stay_time}小时，共花费了 {self.parkingFee * stay_time} 元。")

                    # 便道车辆进入停车场
                    if not self.Q.emptyQueue():
                        car, arrive_time = self.Q.dequeue()
                        if car is not None:
                            self.S.push(car, arriveTime)
                            print(f"车牌号是 {car} 的车从便道进入停车场位置 {self.S.top + 1}")

    """功能2：显示停车场信息"""
    def parkInformation(self):
        print("\n 名称：临时停车场")
        print(f" 车位数：{self.parkingSize}")
        print(f" 收费情况：{self.parkingFee}元/时")

    """功能3：查看停车场车辆信息"""
    def seeCarInformation(self):
        if self.S.emptyStack():
            print("\n停车场内无车辆存在！")
            return

        print("---------------------------------------------------------------------")
        print("  状态(A/D)    |    车牌号     |     所在车位     |     进入时间     ")

        for i in range(self.S.top, -1, -1):
            print(
                f"      A        |      {self.S.carNumber[i]}        |         {i + 1}        |         {self.S.arriveTime[i]}")

        print("---------------------------------------------------------------------\n")

    """功能4：查看便道车辆信息"""
    def pavementCarInformation(self):
        if self.Q.emptyQueue():
            print("\n便道内无车辆存在！")
            return

        print("-----------------------------------------------------")
        print("    车牌号     |      便道位置    |      进入时间    ")

        current = self.Q.front.next
        pos = 1
        while current:
            print(f"      {current.carNumber}        |         {pos}        |         {current.arriveTime}")
            current = current.next
            pos += 1

        print("-----------------------------------------------------\n")

    """功能5：清空停车场"""
    def emptyParking(self):
        self.S.top = -1
        print("停车场车辆已清空！")

    """功能6：查看停车位余量"""
    def parkingPosition(self):
        if self.parkingSize == 0:
            print("停车场车位剩余 0 个\n")
        else:
            remaining = self.parkingSize - (self.S.top + 1)
            print(f"停车场车位剩余 {remaining} 个\n")

    """功能7：清空便道车辆"""
    def emptyPavement(self):
        self.Q.front.next = None
        self.Q.rear = self.Q.front
        self.Q.position = 0
        print("便道车辆已清空！")

    """功能8：关闭停车场"""
    def closeParking(self):
        self.emptyParking()
        self.emptyPavement()
        self.parkingSize = 0
        self.parkingFee = 0
        self.pavementFee = 0
        self.position = 0
        self.count = 0
        print("停车场内已无任何车辆......\n停车场已关闭！")

    """功能0：设置停车场信息"""
    def setParkingInformation(self):
        # 容量设置
        while True:
            size_str = input("请输入停车场最大容量：")
            valid, size = self.validNumber(size_str)
            if valid and size > 0:
                self.parkingSize = size
                self.S = Stack(size) # 重新初始化停车场
                self.LS = Stack(size) # 重新初始化临时栈
                break
            print("输入无效，请重新输入！")

        # 停车场费率设置
        while True:
            fee_str = input("请输入车在'停车场'每小时的费用（元/时）：")
            valid, fee = self.validNumber(fee_str)
            if valid:
                self.parkingFee = fee
                break
            print("输入无效，请重新输入！")

        # 便道费率设置
        choice = input("\n请选择车在'便道'上停留是否收费[ Y 或 N ]：").upper()
        if choice == 'Y':
            while True:
                fee_str = input("请输入车在'便道'每小时的费用（元/时）：")
                valid, fee = self.validNumber(fee_str)
                if valid:
                    self.pavementFee = fee
                    break
                print("输入无效，请重新输入！")
        else:
            self.pavementFee = 0

    """显示主菜单"""
    def display(self):
        print("\n\n*** 欢迎您进入 简洁版停车场管理系统功能界面 ***\n")
        print("输入序号选择您需要的功能：\n")
        print("0.设置 停车场车位数、收费情况 + 便道收费情况")
        print("1.车辆 进/出 停车场              2.显示停车场基本信息")
        print("3.查询当前停车场内车辆信息       4.查看便道车辆信息")
        print("5.清空停车场车辆                 6.查看停车场车位余量")
        print("7.清空便道车辆                   8.界面清屏，保留菜单说明")
        print("9.停止停车场开放                 10.退出系统")

    # 管理员功能界面
    def functionWindow(self):
        """主控制循环：系统入口"""
        self.display()

        while True:
            choice_str = input("\n请选择功能：")
            valid, choice = self.validNumber(choice_str)

            if not valid:
                print("*** 输入内容不为数字，不符合要求，请重新输入! ***")
                continue

            # 检查停车场是否初始化
            if self.parkingSize == 0 and choice not in [0, 8, 10]:
                print("\n*** 停车场容量为0，请先设置车位数! (当前只可选择0、8、10操作) ***")
                continue

            # 功能路由
            if choice == 0:
                self.setParkingInformation()
            elif choice == 1:
                self.load()
            elif choice == 2:
                self.parkInformation()
            elif choice == 3:
                self.seeCarInformation()
            elif choice == 4:
                self.pavementCarInformation()
            elif choice == 5:
                self.emptyParking()
            elif choice == 6:
                self.parkingPosition()
            elif choice == 7:
                self.emptyPavement()
            elif choice == 8:
                os.system('cls' if os.name == 'nt' else 'clear')
                self.display()
            elif choice == 9:
                self.closeParking()
            elif choice == 10:
                print("\n***系统退出成功，欢迎您下次使用! ***")
                sys.exit()
            else:
                print("无效选择，请重新输入！")

    """管理员登录"""
    def adminLogin(self):
        print("*** 管理员您好，欢迎您使用停车场管理系统 ***\n")
        print("请先进行登录 (user:123456,password:000000)：\n")

        while True:
            user_str = input("请输入账号：")
            valid_user, username = self.validNumber(user_str)

            if not valid_user:
                print("*** 输入内容不为数字，不符合要求，请重新输入! ***")
                continue

            if username == 123456:
                break
            print("账号错误，请重新输入：")

        while True:
            pwd_str = input("请输入密码：")
            valid_pwd, password = self.validNumber(pwd_str)

            if not valid_pwd:
                print("*** 输入内容不为数字，不符合要求，请重新输入! ***")
                continue

            if password == 000000:
                self.functionWindow()
                break
            print("密码错误，请重新输入：")

# 主程序入口
if __name__ == "__main__":
    system = ParkingSystem()
    system.adminLogin()