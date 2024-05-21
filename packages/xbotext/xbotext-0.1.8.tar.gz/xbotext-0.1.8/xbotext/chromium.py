# 获取 %localappdata% 文件夹的数据

import os
import json

local_appdata_path = os.getenv('LOCALAPPDATA')


def get_chromium_user_data_path(browser_name="edge") -> str:
    """获取浏览器的用户数据目录"""
    if browser_name == "edge":
        return os.path.join(local_appdata_path, "Microsoft", "Edge", "User Data")
    elif browser_name == "chrome":
        return os.path.join(local_appdata_path, "Google", "Chrome", "User Data")
    else:
        raise ValueError("不支持的浏览器名称")



