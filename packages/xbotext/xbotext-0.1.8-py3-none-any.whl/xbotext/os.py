# 开启长路径
# 开启文件扩展名
# 获取安装文件的路径
# 是否安装某个软件

import winreg


def is_show_file_ext():
    """检查是否显示文件扩展名"""
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced",
    )
    value, _ = winreg.QueryValueEx(key, "HideFileExt")
    winreg.CloseKey(key)
    return value == 0


def set_show_file_ext():
    """设置显示文件扩展名"""
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced",
        0,
        winreg.KEY_WRITE,
    )
    winreg.SetValueEx(key, "HideFileExt", 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(key)


def enable_long_paths():
    """启用长路径支持"""
    try:
        # 打开注册表键
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\FileSystem",
            0,
            winreg.KEY_SET_VALUE,
        )

        # 设置注册表项
        winreg.SetValueEx(key, "LongPathsEnabled", 0, winreg.REG_DWORD, 1)

        # 关闭注册表键
        winreg.CloseKey(key)

        print("Long paths support enabled successfully.")
    except Exception as e:
        print(f"Failed to enable long paths support: {e}")
