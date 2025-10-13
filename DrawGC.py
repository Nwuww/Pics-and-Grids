from log import logout
from PIL import Image, ImageDraw
from MyUtils import parse_color

def draw_grid_with_crosses(output_path):
    # 输入参数
    size_y = int(input("横向网格线数 (Default=50): ") or 50)
    size_x = int(input("纵向网格线数 (Default=50): ") or 50)
    s = int(input("网格线间距 s [Pixels](Default=50): ") or 50)
    l = int(input("网格线宽度 l [Pixels](Default=2): ") or 2)
    alpha = int(input("网格线不透明度 alpha [0~255](Default=100): ") or 100)

    # 网格线颜色输入（默认黑色）
    line_color_input = input("网格线颜色\n"
                             "[十六进制色值 #RRGGBB 或 RGB r,g,b](Default=\"#1F1E33\")\n"
                             "推荐查询 https://www.codeeeee.com/color/picker.html\n") or "#1F1E33"
    line_color = parse_color(line_color_input, (0, 0, 0))

    # 十字参数
    s_cross = int(input("十字半径 s_cross [Pixels](Default=10): ") or 10)
    l_cross = int(input("十字宽度 l_cross [Pixels](Default=4): ") or 4)
    alpha_cross = int(input("十字不透明度 alpha_cross [0~255](Default=220): ") or 220)

    # 十字颜色输入（默认红色）
    cross_color_input = input("十字颜色(Default=\"#1F2030\")\n") or "#1F2030"
    cross_color = parse_color(cross_color_input, (0, 0, 0))

    logout("Data", (f"DrawGrid\n"
                    f"#-[size={size_x}:{size_y}]\n"
                    f"#-[G={s}:{l}:{alpha}:{line_color}]\n"
                    f"#-[C={s_cross}:{l_cross}:{alpha_cross}:{cross_color}]"),
           ("DRAW_GC", 167), 1)

    # 验证输入
    if s_cross >= s:
        logout("Warn", "s_cross >= s", "DRAW_GC", 1)
        raise ValueError("十字半径 s_cross 必须小于网格间距 s")

    # 计算画布大小
    num_lines_x = size_x
    num_lines_y = size_y
    canvas_size_x = (num_lines_x - 1) * (s + l) + l
    canvas_size_y = (num_lines_y - 1) * (s + l) + l
    logout("DEBUG", f"Calculations:\n"
                f"numl_xy: {size_x}, {size_y}\n"
                f"canvas_xy: {canvas_size_x}, {canvas_size_y}", "DRAW_GC", 1)


    print("开始绘制！")
    print("> 创建背景")
    # 创建透明背景图像
    img = Image.new('RGBA', (canvas_size_x, canvas_size_y), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    logout("Reg", "img Created!", "DRAW_GC", 1)

    logout("Reg", "Start drawing", "DRAW_GC", 1)
    # 绘制水平网格线（带透明度）
    print("> 绘制水平网格")
    logout("Reg", "Horizontal lines drawing start",
           "DRAW_GC", 2)
    logout("DEBUG", "draw loop start: ", "DRAW_GC", 2)
    for i in range(num_lines_y):
        y = i * (s + l) + l // 2
        logout("DEBUG", f"{i}:y={y}", "DRAW_GC", 3)
        if y >= canvas_size_y:
            logout("DEBUG", "draw loop END;", "DRAW_GC", 3)
            break  # 超出画布时停止
        draw.line([(0, y), (canvas_size_x, y)], fill=(*line_color, alpha), width=l)
        logout("DEBUG", f"d({0},{y}),({canvas_size_x},{y})", "DRAW_GC", 3)

    # 绘制垂直网格线（带透明度）
    print("> 绘制垂直网格")
    logout("Reg", "Vertical lines drawing start",
           "DRAW_GC", 2)
    logout("DEBUG", "draw loop start: ", "DRAW_GC", 3)
    for i in range(num_lines_x):
        x = i * (s + l) + l // 2
        logout("DEBUG", f"{i}:x={x}", "DRAW_GC", 3)
        if x >= canvas_size_x:
            logout("DEBUG", "draw loop END;", "DRAW_GC", 3)
            break
        draw.line([(x, 0), (x, canvas_size_y)], fill=(*line_color, alpha), width=l)
        logout("DEBUG", f"d({x},{0}),({x},{canvas_size_y})", "DRAW_GC", 3)

    # 在网格线交点绘制十字（带透明度）
    print("> 绘制十字")
    logout("Reg", "Crosses drawing start",
           "DRAW_GC", 2)
    for row in range(num_lines_y):
        y = row * (s + l) + l // 2
        if y >= canvas_size_y:
            break
        for col in range(num_lines_x):
            x = col * (s + l) + l // 2
            if x >= canvas_size_x:
                break

            # 只在特定交点绘制十字
            if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
                draw.line([(x - s_cross, y), (x + s_cross, y)],
                          fill=(*cross_color, alpha_cross), width=l_cross)
                draw.line([(x, y - s_cross), (x, y + s_cross)],
                          fill=(*cross_color, alpha_cross), width=l_cross)

    # 保存图像
    img.save(output_path)
    print(f"图像已保存到 \"{output_path}\" ヾ(≧▽≦*)/ !\n快点移动或者重命名，不然就要被覆盖了喵! ><")
    logout("Imp", f"GC Saved!:{output_path}", "DRAW_GC", 1)

