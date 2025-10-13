import time
import os
from pathlib import Path

deb_mode :bool = False

def deb(stat: bool):
    global deb_mode
    deb_mode = True

def get_log_file():
    """确保日志目录存在并返回文件对象"""
    log_dir = Path("log")
    log_dir.mkdir(exist_ok=True)

    now_time = f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}^" \
               f"{time.localtime().tm_hour}_{time.localtime().tm_min}_{time.localtime().tm_sec}"

    log_path = log_dir / f"logout[{now_time}].txt"
    return open(log_path, 'a', encoding='utf-8')  # 追加模式

# 全局文件对象（单例模式）
_log_file = get_log_file()

'''
Reg 普通记录
Data 数据记录
Imp 重要记录
Warn 警告错误
FATAL 致命错误
DEBUG 调试信息
'''
def logout(importance, message, pos, sublevel=0):
    try:
        log_line = "#" * sublevel + f"[{importance}|{pos}] {message}\n"
        if deb_mode or importance != "DEBUG":
            _log_file.write(log_line)
        _log_file.flush()  # 强制立即写入磁盘

        if message == "#EXIT#":
            _log_file.write("LOG FILE CLOSED\n")
            _log_file.close()
    except Exception as e:
        print(f"[FATAL|log.logout] 日志写入失败: {e}")

# 程序退出时自动关闭的保险措施
import atexit

atexit.register(lambda: _log_file.close() if not _log_file.closed else None)
