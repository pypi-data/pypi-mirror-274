# 获取客户端的版本, 安装路径
# 获取当前登录的用户名
import os
import json
import inspect
import winreg
import xml.dom.minidom
import win32com.client
import win32api
import win32con
import win32process

__all__ = ["get_current_version", "get_current_user"]

def read_registry_value(key, subkey, value_name):
    try:
        registry_key = winreg.OpenKey(key, subkey, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(registry_key, value_name)
        winreg.CloseKey(registry_key)
        return value
    except FileNotFoundError:
        return None


def write_registry_value(key, subkey, value_name, value):
    try:
        registry_key = winreg.OpenKey(key, subkey, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, value_name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except Exception as e:
        print("Error writing to registry:", e)
        return False


def get_process_path(process_name):
    wmi = win32com.client.GetObject("winmgmts:")
    for process in wmi.InstancesOf("Win32_Process"):
        if process.Name == process_name:
            pid = process.ProcessId
            try:
                process_handle = win32api.OpenProcess(
                    win32con.PROCESS_QUERY_INFORMATION, False, pid
                )
                exe_path = win32process.GetModuleFileNameEx(process_handle, 0)
                return exe_path
            except Exception as e:
                print(f"Failed to get process path: {e}")
                return None
            finally:
                win32api.CloseHandle(process_handle)
    return None


def get_current_version():
    """获取当前影刀版本"""
    process_name = "ShadowBot.Shell.exe"
    process_path = get_process_path(process_name)
    try:
        # 获取文件版本信息
        info = win32api.GetFileVersionInfo(process_path, "\\")
        version = "%d.%d.%d.%d" % (
            info["FileVersionMS"] / 65536,
            info["FileVersionMS"] % 65536,
            info["FileVersionLS"] / 65536,
            info["FileVersionLS"] % 65536,
        )
        return version
    except Exception as e:
        return None


def get_current_user():
    """获取当前影刀登录账号"""
    path_username = rf'{os.getenv("Localappdata")}\ShadowBot\users\Account.xml'
    path_dom = xml.dom.minidom.parse(path_username)
    usernam_data = (
        path_dom.documentElement.getElementsByTagName("UserName")[0].childNodes[0].data
    )
    return usernam_data


def get_current_robot_uuid():
    """
    获取当前应用的 uuid
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
        robot_uuid = package_json.get("uuid")
        return robot_uuid
