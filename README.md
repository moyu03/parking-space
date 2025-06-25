# parking-space停车场管理

## 安装依赖
```
pip install -r requirements.txt
```
文件结构
```
parking-management/
├── src/                    # 源代码
│   ├── core/               # 核心算法
│   │   ├── parking_lot.py      # 停车场类（栈实现）
│   │   ├── side_road.py        # 便道类（队列实现）
│   │   ├── calculator.py       # 计费模块
│   │   └── constants.py        # 常量配置
│   │
│   ├── ui/                 # 界面系统
│   │   ├── main_window.py      # 主窗口
│   │   ├── status_panel.py     # 状态显示区
│   │   └── control_panel.py    # 操作控制区
│   │
│   └── extension/          # 扩展功能
│       ├── logger.py           # 操作日志
│       ├── persistence.py      # 数据存储
│       └── report_generator.py # 统计报表
│
├── tests/                  # 测试套件
│   ├── test_core/          # 核心算法测试
│   └── test_extension/     # 扩展功能测试
│
├── docs/                   # 项目文档
│   ├── API.md              # 接口文档
│   └── DESIGN.md           # 设计思路
│
├── requirements.txt        # Python依赖
└── main.py                 # 程序入口
```