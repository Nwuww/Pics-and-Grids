from log import logout
from PIL import Image

def resize_image(output_path):
    """图片调整大小功能"""
    # 读取源图片
    while True:
        src_path = (input("\n请输入源图片(要被修改的图片)路径: ") or "test.jpg").strip()
        try:
            src_img = Image.open(src_path)
            logout("Reg", f"src Pic:{src_img},{src_img.size}", "RESIZE", 1)
            break
        except FileNotFoundError:
            print("图片不存在，请重新输入!")
            logout("Warn", "src Pic not exist", "RESIZE", 1)

    print(f"\n当前图片尺寸：{src_img.size} (宽×高)")

    # 选择调整模式
    print("\n请选择调整模式: ")
    print("1. 裁剪模式(裁剪多余部分)")
    print("2. 拉伸模式(强制改变比例)")
    mode = input("请输入选项(1/2): ").strip()

    # 选择目标尺寸确定方式
    print("\n请选择目标尺寸确定方式:")
    print("1. 自定义尺寸")
    print("2. 参考另一张图片的尺寸")
    size_mode = input("请输入选项(1/2):").strip()

    logout("Reg", f"mode:{mode}; sized mode:{size_mode}", "RESIZE", 1)

    # 获取目标尺寸
    if (size_mode == "1") and (mode == "2"):
        logout("Reg", "cut sized mode {1}", "RESIZE", 2)
        while True:
            try:
                width = int(input("请输入目标宽度 [Pixels]: "))
                height = int(input("请输入目标高度 [Pixels]: "))
                if width > 0 and height > 0:
                    target_size = (width, height)
                    logout("Reg", f"cut size={width}:{height}", "RESIZE", 2)
                    break
                print("尺寸必须大于0!")
                logout("Warn", "Invalid size", "RESIZE", 3)
            except ValueError:
                print("请输入有效的数字!")
                logout("Warn", "Invalid input", "RESIZE", 3)
    elif size_mode == "2":
        logout("Reg", "cut sized mode {2}", "RESIZE", 2)
        while True:
            ref_path = input("请输入参考图片路径: ").strip()
            try:
                ref_img = Image.open(ref_path)
                target_size = ref_img.size
                print(f"参考图片尺寸: {target_size}")
                logout("Reg", f"refer img:{ref_path},{target_size}", "RESIZE", 3)
                break
            except FileNotFoundError:
                print("图片不存在，请重新输入!")
                logout("Warn", "refer Pic not exist!", "RESIZE", 3)
    elif (size_mode != "1") or (mode != "1"):
        print("无效选项，使用默认尺寸 512x512")
        logout("Warn", "Invalid size", "RESIZE", 2)
        target_size = (512, 512)

    # 执行调整
    if mode == "1":
        # 获取裁剪区域
        logout("Reg", "resize mode {1}", "RESIZE", 2)
        print("\n请输入裁剪区域坐标(相对于原图左上角)\n"
              "请确保: 0 ≤ x1 < x2 ≤ 图片宽度，0 ≤ y1 < y2 ≤ 图片高度: \n")
        while True:
            try:
                left = int(input("左边界 x1 [Pixels]: "))
                top = int(input("上边界 y1 [Pixels]: "))
                right = int(input("右边界 x2 [Pixels]: "))
                bottom = int(input("下边界 y2 [Pixels]: "))

                # 验证坐标有效性
                if (0 <= left < right <= src_img.width and
                        0 <= top < bottom <= src_img.height):
                    break
                print("坐标无效！请确保: 0 ≤ x1 < x2 ≤ 图片宽度，0 ≤ y1 < y2 ≤ 图片高度")
                logout("Warn", "Invalid coordinate.", "RESIZE", 3)
            except ValueError:
                logout("Warn", "Invalid input", "RESIZE", 3)
                print("请输入有效的数字！")

        # 执行裁剪
        result = src_img.crop((left, top, right, bottom))
    else:
        # 拉伸模式
        logout("Reg", "resize mode {2}", "RESIZE", 2)
        result = src_img.resize(target_size, Image.Resampling.LANCZOS)
    result.save(output_path)
    print(f"图片已保存到 {output_path}")
    logout("Reg", f"Img saved:{output_path}", "RESIZE", 1)