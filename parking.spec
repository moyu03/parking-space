# parking.spec

block_cipher = None

# 主入口文件
a = Analysis(
    ['main.py'],
    pathex=['.'],  # 项目根目录
    binaries=[],
    datas=[
        # 添加所有需要包含的目录和文件
        ('ui/', 'ui'),
        ('core/', 'core'),
        ('models/', 'models'),
        ('utils/', 'utils'),
        ('icon.ico', '.'), # 添加图标
        ('D:\\anaconda\\python312.dll', '.')
    ],
    hiddenimports=[
        # 手动添加所有隐藏依赖
        'tkinter',
        'time',
        'datetime',
        'collections',
        'sys',
        
        'os',
        'utils.time_utils'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 生成 PY 文件
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 可执行文件配置
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ParkingSystem',  # 输出文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 使用 UPX 压缩
    console=False,  # 不显示控制台
    icon='icon.ico',  # 图标文件
)

# 收集所有文件
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ParkingSystem'  # 最终文件夹名
)