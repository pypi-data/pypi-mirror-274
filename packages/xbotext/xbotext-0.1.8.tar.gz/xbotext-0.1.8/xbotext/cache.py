import xbot # type: ignore
import os
import json
import inspect


# 影刀应用运行时缓存数据
# 缓存目录 考虑跨平台
# %locapappdata% -> xbot -> app -> uuid
# %locapappdata% -> xbot -> activity -> activity_name


def get_xbot_type():
    """获取机器人类型
    :retrun: app, activity
    """
    stack = inspect.stack()
    for calling_module_frame in stack:
        if "xbot_robot" in calling_module_frame.filename:
            calling_module_file_path =  calling_module_frame.filename
            break
    calling_module_dir, _ = os.path.split(calling_module_file_path)
    package_json_file_path = os.path.join(calling_module_dir, "package.json")

    with open(package_json_file_path) as f:
        package_json = json.load(f)
        robot_type = package_json.get("robot_type")

        # 应用返回对应的 uuid , 指令返回指令编码
        if robot_type == "app":
            robot_key = package_json.get("uuid")

        if robot_type == "activity":
            robot_key = package_json.get("activity_code")

        return robot_type, robot_key


def get_xbot_cache_path():
    """获取缓存文件路径"""
    cache_path = os.environ.get('LOCALAPPDATA')
    xbot_type = get_xbot_type()
    xbot_cache_path = os.path.join(cache_path, "xbot", *xbot_type)

    if not os.path.exists(xbot_cache_path):
        os.makedirs(xbot_cache_path)

    default_cache_path = os.path.join(xbot_cache_path, "default")
    if not os.path.exists(default_cache_path):
        with open(default_cache_path, "w") as f:
            json.dump(dict(), f)

    return xbot_cache_path


def get_xbot_cache_default(key=None):
    """返回应用或者指令缓存数据
    :param: key 获取键, 如果是 None 返回全部
    """
    default_cache_path = os.path.join(get_xbot_cache_path(), "default")

    with open(default_cache_path) as f:
        default_json = json.load(f)
        if key:
            return default_json.get(key)
        return default_json


def set_xbot_cache_default(key, value) -> bool:
    """设置应用或指令缓存数据"""

    try:
        default_cache_path = os.path.join(get_xbot_cache_path(), "default")
        with open(default_cache_path, "r") as fr:
            default_json = json.load(fr)
        with open(default_cache_path, "w") as fw:
            default_json[key] = value
            json.dump(default_json, fw, indent=4)
        return True
    except Exception as e:
        print(e)
        return False


def set_xbot_cache_default_breakponit(num: int):
    """设置应用执行过程的断点"""
    set_xbot_cache_default("breakpoint", num)


def get_xbot_cache_default_breakponit() -> int:
    """获取应用执行过程中断点"""
    return get_xbot_cache_default("breakpoint")


def show_xbot_cache_default_breakpoint(title="继续运行", label="开始位置") -> None:
    """通过对话框的形式展示断点, 并允许客户输入"""
    breakponit_value = get_xbot_cache_default_breakponit()
    if get_xbot_cache_default_breakponit() == None:
        return

    dialog_info = xbot.app.dialog.show_input_dialog(title, label, typestr='input', value=str(breakponit_value))
    breakponit_value = dialog_info.get('value')
    assert str(breakponit_value).isdigit(), "请输入数字"
    set_xbot_cache_default_breakponit(int(breakponit_value))

