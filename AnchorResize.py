from PIL import Image, ImageDraw
import sys
from MyUtils import parse_anchor
from log import logout

def calculate_transparent_region(img_size, anchor, ratio):
    logout("Reg", "Start calculating transparent_region", "ANCHOR_RESIZE_CALC",2)
    """计算透明区域坐标"""
    width, height = img_size
    anchor = anchor.upper()

    # 标准化方向：确保两个字符分别代表不同轴向
    h_dir = next((c for c in anchor if c in 'LR'), None)
    v_dir = next((c for c in anchor if c in 'UD'), None)

    # 计算新尺寸（ratio>1时扩大画布）
    new_width = int(width * ratio) if ratio > 1 else width
    new_height = int(height * ratio) if ratio > 1 else height


    # 计算透明区域边界
    if ratio <= 1:  # 覆盖模式
        logout("DEBUG", f"CUT MODE: anchor:{anchor}",
               "ANCHOR_RESIZE_CALC", 3)
        if not v_dir:  # 纯水平方向（LM/RM）
            if 'L' in anchor:
                box = (0, 0, int(width * ratio), height)  # 左边界对齐
            else:
                box = (width - int(width * ratio), 0, width, height)  # 右边界对齐

        elif not h_dir:  # 纯垂直方向（UM/DM）
            if 'U' in anchor:
                box = (0, 0, width, int(height * ratio))  # 上边界对齐
            else:
                box = (0, height - int(height * ratio), width, height)  # 下边界对齐

        else:  # 角落组合（LU/RU/LD/RD）
            if 'L' in anchor:
                left = 0
                right = int(width * ratio)
            else:
                left = width - int(width * ratio)
                right = width

            if 'U' in anchor:
                top = 0
                bottom = int(height * ratio)
            else:
                top = height - int(height * ratio)
                bottom = height

            box = (left, top, right, bottom)  # 角点对齐

    else:  # 扩展模式（ratio>1）
        logout("DEBUG", f"EXT MODE: anchor:{anchor}",
               "ANCHOR_RESIZE_CALC", 3)
        if not v_dir:  # 水平扩展（LM/RM）
            if 'L' in anchor:
                box = (new_width - width, 0, new_width, new_height)  # 右边界对齐原图左
            else:
                box = (0, 0, new_width - width, new_height)  # 左边界对齐原图右

        elif not h_dir:  # 垂直扩展（UM/DM）
            if 'U' in anchor:
                box = (0, new_height - height, new_width, new_height)  # 下边界对齐原图上
            else:
                box = (0, 0, new_width, new_height - height)  # 上边界对齐原图下

        else:  # 角落扩展（LU/RU/LD/RD）
            if 'L' in anchor:
                left = new_width - width
                right = new_width
            else:
                left = 0
                right = new_width - width

            if 'U' in anchor:
                top = new_height - height
                bottom = new_height
            else:
                top = 0
                bottom = new_height - height

            box = (left, top, right, bottom)  # V型凹点对齐原图角

    return (new_width, new_height), box


def cutting_mode(src_img, anchor, ratio):
    width, height = src_img.size

    if anchor in ('LM', 'ML'):
        box = [(0, 0, int(width * ratio), height)]
    elif anchor in ('RM', 'MR'):
        box = [(width - int(width * ratio), 0, width, height)]
    elif anchor in ('UM', 'MU'):
        box = [(0, 0, width, int(height * ratio))]
    elif anchor in ('DM', 'MD'):
        box = [(0, height - int(height * ratio), width, height)]
    elif anchor in ('LU', 'UL'):
        box = [(0, 0, int(width * ratio), int(height * ratio))]
    elif anchor in ('RU', 'UR'):
        box = [(width - int(width * ratio), 0, width, int(height * ratio))]
    elif anchor in ('LD', 'DL'):
        box = [(0, height - int(height * ratio), int(width * ratio), height)]
    elif anchor in ('RD', 'DR'):
        box = [(width - int(width * ratio), height - int(height * ratio), width, height)]
    elif anchor == 'MM':
        keep_w, keep_h = int(width * ratio), int(height * ratio)
        left, top = (width - keep_w) // 2, (height - keep_h) // 2
        box = [
            (0, 0, width, top),  # 上
            (0, top + keep_h, width, height),  # 下
            (0, top, left, top + keep_h),  # 左
            (left + keep_w, top, width, top + keep_h)  # 右
        ]

        # 应用透明
    mask = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(mask)
    for area in box:
        draw.rectangle(area, fill=0)
    result = src_img.copy()
    result.putalpha(mask)
    return result

def extending_mode(src_img, anchor, ratio):
    width, height = src_img.size
    if anchor in ('LM', 'ML', 'RM', 'MR'):
        new_width, new_height = int(width * ratio), height
    elif anchor in ('UM', 'MU', 'DM', 'MD'):
        new_width, new_height = width, int(height * ratio)
    else:
        new_width, new_height = int(width * ratio), int(height * ratio)

    result = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))

    if anchor in ('LM', 'ML'):
        result.paste(src_img, (int(new_width - width * (ratio - 2)), 0))
    elif anchor in ('RM', 'MR'):
        result.paste(src_img, (0, 0))
    elif anchor in ('UM', 'MU'):
        result.paste(src_img, ((new_width - width) // 2, 0))
    elif anchor in ('DM', 'MD'):
        result.paste(src_img, ((new_width - width) // 2, new_height - height))
    elif anchor in ('LU', 'UL'):
        result.paste(src_img, (new_width - width, new_height - height))
    elif anchor in ('RU', 'UR'):
        result.paste(src_img, (0, new_height - height))
    elif anchor in ('LD', 'DL'):
        result.paste(src_img, (new_width - width, 0))
    elif anchor in ('RD', 'DR'):
        result.paste(src_img, (0, 0))
    elif anchor == 'MM':
        result.paste(src_img, ((new_width - width) // 2, (new_height - height) // 2))
    return result

def anchoring_cut(output_folder, output_filename):
    # 用户输入
    src_path = (input("请输入源图片路径: ") or "test.jpg").strip()
    anchor = input("请输入锚点方向\n(U上 D下 L左 R右 M中，如UM/MU正上，RD/DR右下，MM正中，必须两个字母组合): \n").strip()
    ratio = float(input("请输入绘制比例\n(<1则覆盖原图，>1则扩大源图尺寸填充透明)[Default=0.5]: ") or 0.5)
    # 处理
    anchor_dirs = parse_anchor(anchor)
    anchor = ""
    for anc in anchor_dirs:
        anchor += anc
    logout("Data", f"src_path:{src_path}, anchor:{anchor}, ratio:{ratio}",
           "ANCHOR_RESIZE", 1)


    # 打开源图像并转为RGBA模式
    src_img = Image.open(src_path).convert('RGBA')
    original_size = src_img.size
    logout("Reg", "src Img open successful!", "ANCHOR_RESIZE", 1)
    print("源文件读取成功！")

    # 计算透明区域
    print("开始计算锚定区域..")
    new_size, transparent_box = calculate_transparent_region(original_size, anchor, ratio)

    print("开始绘制图像..")
    if ratio < 1:
        result = cutting_mode(src_img, anchor, ratio)
    else:
        result = extending_mode(src_img, anchor, ratio)

    # 保存结果
    result.save(f"{output_folder}\\{anchor}{ratio}_{output_filename}")
    print(f"图像已保存到 \"{output_folder}\\{anchor}{ratio}_{output_filename}\" ヾ(≧▽≦*)/ !\n快点移动或者重命名，不然就要被覆盖了喵! ><")
    logout("Imp", f"Anchored result Saved!:{output_folder}\\{anchor}{ratio}_{output_filename}",
           "ANCHOR_RESIZE", 1)

