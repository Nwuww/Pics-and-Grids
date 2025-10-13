from log import logout
import sys
import ctypes
import os

def compatibility_win7():
    """兼容性修复"""
    if sys.platform == 'win32':
        # 禁用高精度计时器（解决GetSystemTimePreciseAsFileTime问题）
        os.environ["PYTHONLEGACYWINDOWSTIMER"] = "1"

        # 确保DLL搜索路径包含程序目录
        if hasattr(os, 'add_dll_directory'):
            os.add_dll_directory(os.path.dirname(__file__))

    # Windows 7 内核API兼容性补丁
    if sys.platform == 'win32':
        os.environ["PYTHONLEGACYWINDOWSSTDIO"] = "1"
        os.environ["PYTHONLEGACYWINDOWSTIMER"] = "1"

        # 禁用进程快照API
        try:
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.SetDllDirectoryW(None)
        except:
            pass

    output_path = ""


def parse_color(color_input, default=(0, 0, 0)):
    """将颜色输入解析为 RGB 元组，支持十六进制和逗号分隔的 RGB"""
    if not color_input.strip():
        logout("Reg", "Default color", "COLOR", 2)
        return default  # 用户直接回车时使用默认值

    # 处理十六进制颜色（如 #FF0000）
    if color_input.startswith("#"):
        hex_color = color_input.lstrip("#")
        if len(hex_color) == 3:  # 缩写格式 #RGB → #RRGGBB
            hex_color = "".join([c * 2 for c in hex_color])
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    # 处理 RGB 格式（如 255,0,0）
    elif "," in color_input:
        try:
            r, g, b = map(int, color_input.split(","))
            return r, g, b
        except:
            print(f"无效的 RGB 颜色，使用默认值 {default}")
            logout("Warn","Invalid color!", "COLOR", 2)
            return default

    # 其他情况使用默认值
    else:
        print(f"无法识别的颜色格式，使用默认值 {default}")
        logout("Warn", "Invalid color!", "COLOR", 2)
        return default

def parse_anchor(anchor_str):
    """验证并解析锚点方向"""
    while True:
        # 检查长度和字母
        anchor_str = anchor_str.upper().strip()
        if len(anchor_str) != 2 or not all(c in 'UDLRM' for c in anchor_str):
            logout("Warn", f"Invalid Anchor format! 1:{anchor_str}", "ANCHOR", 2)
            print("锚点格式错误，必须包含两个方向字符(如UM/RD/MM)")
            anchor_str = input(
                "请输入锚点方向\n(U上 D下 L左 R右 M中，如UM/MU正上，RD/DR右下，MM正中): \n").strip()
            continue
        # 使用字母加权：水平方向w1，竖直方向w2，中间w5，最后结果必然为3或>6，否则输入格式错误
        weight_tmp = 0
        for i in range(0,2):
            if anchor_str[i] == "R" or anchor_str[i] == "L":
                weight_tmp += 1
            elif anchor_str[i] == "U" or anchor_str[i] == "D":
                weight_tmp += 2
            elif anchor_str[i] == "M":
                weight_tmp += 5
        if weight_tmp != 3 and weight_tmp < 5:
            logout("Warn", f"Invalid Anchor format! 2 :{anchor_str}", "ANCHOR", 2)
            print("锚点格式错误，两个字符必须分别为不同方向(L/R/M)+(U/D/M)")
            anchor_str = input(
                "请输入锚点方向\n(U上 D下 L左 R右 M中，如UM/MU正上，RD/DR右下，MM正中): \n").strip()
            continue
        break
    return anchor_str[0], anchor_str[1]  # 返回 (垂直方向, 水平方向)
