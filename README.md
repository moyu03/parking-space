# parking-space停车场管理
## 项目简介
设停车场是一个可以停放n辆汽车的南北方向的狭长通道，且只有一个大门可供汽车进出。汽车在停车场内按车辆到达时间的先后顺序，依次由北向南排列（大门在最南端，最先到达的第一辆车停放在车场的最北端），若车场内已停满n辆车，那么后来的车只能在门外的便道上等候，一旦有车开走，则排在便道上的第一辆车即可开入；当停车场内某辆车要离开时，在它之后进入的车辆必须先退出车场为它让路，待该辆车开出大门外，其它车辆再按原次序进入车场，每辆停放在车场的车在它离开停车场时必须按它停留的时间长短交纳费用。试为停车场编制按上述要求进行管理的模拟程序。要求程序输出每辆车到达后的停车位置（停车场或便道上），以及某辆车离开停车场时应缴纳的费用和它在停车场内停留的时间。
## 设计思路
停车场的管理流程如下：
①当车辆要进入停车场时，检查停车场是否已满，如果未满则车辆进入停车场；如果停车场已满，则车辆进入便道等候。
②当车辆要求出行时，先让在它之后进入停车场的车辆退出停车场为它让路，再让该车退出停车场，让路的所有车辆再按其原来进入停车场的次序进入停车场。之后，再检查在便道上是否有车等候，有车则让最先等待的那辆车进入停车场。
## 数据结构
由于停车场只有一个大门，当停车场内某辆车要离开时，在它之后进入的车辆必须先退出车场为它让路，先进停车场的后退出，后进车场的先退出，符合栈的“后进先出，先进后出”的操作特点，因此，可以用一个栈来模拟停车场。而当停车场满后，继续来到的其它车辆只能停在便道上，根据便道停车的特点，先排队的车辆先离开便道进入停车场，符合队列的“先进先出，后进后出”的操作特点，因此，可以用一个队列来模拟便道。排在停车场中间的车辆可以提出离开停车场，并且停车场内在要离开的车辆之后到达的车辆都必须先离开停车场为它让路，然后这些车辆依原来到达停车场的次序进入停车场，因此在前面已设的一个栈和一个队列的基础上，还需要有一个地方保存为了让路离开停车场的车辆，由于先退出停车场的后进入停车场，所以很显然保存让路车辆的场地也应该用一个栈来模拟。因此，本题求解过程中需用到两个栈和一个队列。栈以顺序结构实现，队列以链表结构实现。
## 安装依赖
```
pip install -r requirements.txt

# 设置阿里云镜像源（推荐）
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# 或者设置清华大学源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

#conda设置清华大学源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/

#显示源地址
conda config --set show_channel_urls yes

pip config get global.index-url

#python打包
pyinstaller --onefile --noconsole main.py
```
项目文档结构
```
parking_space/
│
├── main.py                  # 程序主入口
├── core/
│   ├── parking.py           # 核心类：ParkingLot, Car, WaitingLane
│   ├── billing.py           # 计费逻辑封装
│   └── config.py            # 全局配置（默认容量、费率等）
│
├── extensions/
└── dual_exit/
│   ├── parking.py          # 双向停车场核心类
│   ├── lane.py             # 双便道管理类
│   ├── optimizer.py        # 出口优化算法
│   ├── adapter.py          # 适配器（连接新旧系统）
│   └── ui_extension.py     # UI扩展组件
├── ui/
│   ├── login.py             # 登录界面
│   ├── main_menu.py         # 主菜单界面
│   ├── parking_ui.py        # 停车管理界面（车辆进出、查看状态）
│   └── settings.py          # 设置界面（可配置费率、容量）
│
├── models/
│   └── user.py              # 用户模型（简单权限）
│
└── utils/
    └── time_utils.py        # 时间/日期相关工具函数
```