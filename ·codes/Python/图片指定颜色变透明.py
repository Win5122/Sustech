from PIL import Image


def fit(r, g, b, a):
    result = False
    if r > 240 and g > 240 and b > 240:
        result = True
    return result


# 打开图片
with Image.open("result.png") as img:
    # 将图片转换为RGBA模式
    img = img.convert("RGBA")
    # 获取图片的宽度和高度
    width, height = img.size
    r1, g1, b1, a1 = (-1, -1, -1, -1)
    # 遍历每个像素点
    for y in range(height):
        for x in range(width):
            if x > 1050:
                continue
            r, g, b, a = img.getpixel((x, y))
            # 如果当前像素点是白色，则将其透明度设置为0
            if fit(r, g, b, a):
                img.putpixel((x, y), (255, 255, 255, 0))
            else:
                # 全部
                continue
                # 周围
                # break
    # 保存图片
    img.save("result_1.png")
