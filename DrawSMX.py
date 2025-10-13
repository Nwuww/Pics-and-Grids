from log import logout
from PIL import Image, ImageDraw
from MyUtils import parse_color

def draw_square_matrix(output_folder, output_filename):
    # 1. 背景颜色
    bg_color = parse_color(input("背景颜色"
              "[RGBA格式，如 220,220,220 或 #RRGGBB](Default=#E6E6FA]:\n"
              "推荐查询 https://www.codeeeee.com/color/picker.html\n") or "#E6E6FA"
    )
    alpha = int(input("背景不透明度 [alpha 0~255](Default=255): ") or 255)
    alpha = max(0, min(255, alpha))
    bg_color = bg_color + (alpha,)

    # 2. 矩阵参数
    mat_s = int(input("矩阵总边长 [Pixels](Default=1000): ") or 1000)
    num = int(input("矩阵方块行数 [Pixels](Default=5): ") or 5)
    space_rt = float(input("空隙占比 [Proportion:0~1](Default=0.05): ") or 0.05)
    edge_s = int(input("矩阵边缘间距 [Pixels](Default=100): ") or 100)
    sqr_color = parse_color(input("方块颜色"
                                  "[十六进制色值 #RRGGBB 或 RGB r,g,b](Default=\"#FFFACD\")\n"
                                  "推荐查询 https://www.codeeeee.com/color/picker.html\n") or "#FFFACD"
                            )
    sqr_alpha = max(0, min(255, int(input("输入方块不透明度[0~255](Default=200): ") or 200)))
    sqr_color = sqr_color + (sqr_alpha,)

    # 3. 计算方块和间隙尺寸
    total_space = int(mat_s * space_rt)
    sp_s = int(total_space / (num - 1)) if num > 1 else 0
    sqr_s = int((mat_s - total_space) / num)

    print(f"计算参数: 方块尺寸 = {sqr_s:.2f}px, 间隙 = {sp_s:.2f}px")

    # 4. 计算图片总尺寸
    img_size = mat_s + 2 * edge_s
    img = Image.new('RGBA', (img_size, img_size), bg_color)
    draw = ImageDraw.Draw(img)

    logout("Data", f"BG: {bg_color}, {alpha}\n"
           f"MAT: {mat_s} {num} {space_rt} {edge_s} {sqr_color}\n"
           f"sqr_s:{sqr_s}, sp_s:{sp_s}, img_size:{img_size}", "DRAW_MATRIX", 1)

    # 5. 绘制方块矩阵
    logout("DEBUG", "Start drawing sqr", "DRAW_MATRIX", 1)
    print("> 绘制方块矩阵")
    for i in range(num):
        for j in range(num):
            # 计算方块左上角坐标
            x = edge_s + i * (sqr_s + sp_s)
            y = edge_s + j * (sqr_s + sp_s)
            logout("DEBUG", f"x:{x},y:{y}", "DRAW_MATRIX", 2)
            # 绘制方块
            draw.rectangle(
                [x, y, x + sqr_s, y + sqr_s],
                fill=sqr_color
            )

    # 6. 保存第一张图

    img.save(f"{output_folder}\\onlySqr_{output_filename}")
    print(f"已保存: {output_folder}\\onlySqr_{output_filename}")
    logout("Imp", f"Img(only sqr) saving: {output_folder}\\onlySqr_{output_filename}",
           "DRAW_MATRIX", 1)

    # 7. 绘制直线选项

    line_choice = input("绘制直线 (row/col/both/none): ").lower() or "both"
    if line_choice in ['row', 'col', 'both']:
        print("> 绘制直线")
        line_color = parse_color(input("直线颜色"
                                       "[十六进制色值 #RRGGBB 或 RGB r,g,b](Default=\"#B4EEB4\")\n"
                                       "推荐查询 https://www.codeeeee.com/color/picker.html\n") or "#B4EEB4"
                                 )
        sp_s = int(input(f"直线宽度[Pixel](计算推荐值={int(sp_s)}): ") or sp_s)
        logout("Data", f"line: {line_choice}, {line_color}, {sp_s}",
               "DRAW_MATRIX", 1)

        logout("DEBUG", "Start drawing line", "DRAW_MATRIX", 1)
        if line_choice == 'row' or line_choice == 'both':
            # 绘制水平线
            logout("DEBUG", "drawing row", "DRAW_MATRIX", 2)
            for i in range(1, num):
                y = edge_s + i * (sqr_s + sp_s) - sp_s / 2
                logout("DEBUG", f"y: {y}", "DRAW_MATRIX", 3)
                draw.line(
                    [0, y, edge_s * 2 + mat_s, y],
                    fill=line_color,
                    width=int(sp_s)
                )
        if line_choice == 'col' or line_choice == 'both':
            # 绘制垂直线
            logout("DEBUG", "drawing col", "DRAW_MATRIX", 2)
            for i in range(1, num):
                x = edge_s + i * (sqr_s + sp_s) - sp_s / 2
                logout("DEBUG", f"x: {x}", "DRAW_MATRIX", 3)
                draw.line(
                    [x, 0, x, edge_s * 2 + mat_s],
                    fill=line_color,
                    width=int(sp_s)
                )

        # 保存带直线的图
        img.save(f"{output_folder}\\with_lines_{output_filename}")
        print(f"已保存到: {output_folder}\\with_lines_{output_filename}ヾ(≧▽≦*)/ !\n快点移动或者重命名，不然就要被覆盖了喵! ><")
        logout("Imp", f"Img(with line) saving: {output_folder}\\with_lines_{output_filename}",
               "DRAW_MATRIX", 1)
