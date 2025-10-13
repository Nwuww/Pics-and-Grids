import os
import socket

from DrawGC import draw_grid_with_crosses
from DrawSMX import draw_square_matrix
from ResizeImg import resize_image
from AnchorResize import anchoring_cut

from log import logout, deb
from MyUtils import compatibility_win7

try:
    from PIL import Image, ImageDraw
    print("PIL库已安装!")
except ImportError:
    print("PIL库未安装!")
    try:
        socket.create_connection(("151.101.128.223", 80))
        os.system("ping 151.101.128.223 -n 2 -l 1024")
        print("准备安装依赖库，请确保网络通畅!")
        os.system("pip install pillow")
        print("PIL库已安装")
        from PIL import Image, ImageDraw
        print("\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")
    except OSError:
        print("无互联网连接!")
        os.system("ping 151.101.128.223 -n 2 -l 1024")
        os.system("pause")
    
"""
pyinstaller --onefile --add-data "manifest.xml;." --target-arch=32bit --hidden-import=PIL --hidden-import=PIL._imaging main.py
"""

version = "0.4.0 - beta"

if __name__ == "__main__":
    compatibility_win7()
    about = ("\n##############################\n"
             f"grids&pics {version}\n"
             "==> by 不吃猫的鱼鱼鱼 Raindr0pp_ fi5hn0tsa1ty\n"
             "==> 立项自 17/4/25 with Python 3.13.3\n"
             "==> 神秘链接: \nhttps://www.bilibili.com/video/BV1GJ411x7h7/?vd_source=bc522ac4f78d8827312a4a82b3573ee4\n"
             "##############################\n")
    logout("INFO", f"gnp ver{version}", "MAIN", 0)
    logout("Reg", "Start!!!(≧∇≦)~", "MAIN", 0)

    firstTimeFlag = False
    output_folder = "OUTPUT"
    output_filename = "output-"
    output_cnt = int(0)
    while True:
        
        #save path
        if int(input("选择保存模式:\n"
                     "1. 自定义导出目录\n"
                     "2. 使用默认目录\n") or 2) == 1:
            logout("Reg", "Save mode {1}", "MAIN", 0)
            if not firstTimeFlag:
                output_folder = input("自定义输出路径(文件夹名，无需完整目录) \n"
                                    "(Default: ..\\OUTPUT): \n").strip()
                firstTimeFlag = True
            else:
                output_folder = ((input("自定义输出路径(文件夹名，无需完整目录) \n"
                                    "(Last: " + output_folder + ")(直接回车以沿用(覆盖上次文件!!!)): \n").strip())
                               or output_folder)
            if not output_folder.endswith('\\'):
                output_folder += "\\"

            output_filename = (input("自定义输出文件名~同名则会覆盖!!! (Default: output-num): ")
                                    or f"output-{output_cnt}.png")
            if not output_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                output_filename += ".png"

        else:
            logout("Reg", "Save mode {2}", "MAIN", 0)
            output_folder = "OUTPUT\\"
            output_filename = f"output-{output_cnt}.png"

        # 确保目标文件夹存在
        if not os.path.exists(output_folder):
            logout("Warn", "Path not exist", "MAIN", 1)
            os.makedirs(output_folder)
            logout("Reg", "Path been created!", "MAIN", 1)

        # 构建完整路径并保存
        output_path = os.path.join(output_folder, output_filename)
        print("\n\nSave Path: " + output_folder + output_filename)
        logout("Reg", f"Path save:{output_path}", "MAIN", 0)

        #logout("TEST", "#EXIT#", ("BREAK", 267), 0)
        print("\n\n#################################")
        #choose func
        func = input("选择功能: \n"
                         "1. 绘制网格线\n"
                         "2. 绘制方块图\n"
                         "r. resize图片\n"
                         "a. 基于锚点处理图片\n"
                         "e. About Dev.\n"
                         "d. 清除Log缓存\n"
                         "#DEBUG#. 日志调试模式\n"
                         "_> ")
        os.system("cls")
        if func == "1":
            logout("Reg", "Func {DRAW_GC}", "MAIN", 0)
            draw_grid_with_crosses(output_path)
            output_cnt += 1
        elif func == "2":
            logout("Reg", "Func {DRAW_MATRIX}", "MAIN", 0)
            draw_square_matrix(output_folder, output_filename)
            output_cnt += 1
        elif func.lower() == "r":
            logout("Reg", "Func {RESIZE}", "MAIN", 0)
            resize_image(output_path)
            output_cnt += 1
        elif func.lower() == "a":
            logout("Reg", "Func {ANCHOR_RESIZE}", "MAIN", 0)
            anchoring_cut(output_folder, output_filename)
            output_cnt += 1
        elif func.lower() == "e":
            logout("Reg", "Func {ABOUT}", "MAIN", 0)
            print(about)
        elif func.lower() == "d":
            logout("Reg", "Func {DEL log}", "MAIN", 0)
            os.system("del \"log\\*\"")
            logout("Imp", "!!!Delete logs!!!", "MAIN", 0)
            print("=> Already delete!")
        elif func == "#DEBUG#":
            deb(True)
            print("#_> Debug mode start successfully!")
            logout("DEBUG", "DEBUG mode start`(*>﹏<*)′`", "MAIN", 0)
        else:
            logout("FATAL", "Func {ELSE}", "BREAK", 0)
            os.system("start cmd.exe /K "
                      "echo https://www.bilibili.com/video/BV1GJ411x7h7/?vd_source=bc522ac4f78d8827312a4a82b3573ee4")
            logout("Reg", "#EXIT#", "MAIN", 0)
            exit()

        print()
        #break
        if input("Enter \'/\' to restart | Enter \"Enter\" to exit: ") != '/':
            logout("Reg", "#EXIT#またね~(●'◡'●)", "MAIN", 0)
            break

    os.system("pause")