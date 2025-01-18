from PIL import Image
import numpy as np


def change_background_to_transparent(image_path, output_path):
    # 打开图片并转换为 RGBA 模式
    img = Image.open(image_path).convert("RGBA")

    # 将图片转换为 numpy 数组
    image_data = np.array(img)

    # 分离 RGBA 通道
    r, g, b, a = image_data[:, :, 0], image_data[:, :, 1], image_data[:, :, 2], image_data[:, :, 3]

    # 定义白色背景的阈值，允许颜色有些微差异
    white_threshold = (r > 200) & (g > 200) & (b > 200)

    # 将背景像素设置为全透明 (Alpha = 0)
    image_data[white_threshold] = (255, 255, 255, 0)

    # 将 numpy 数组转换回图片
    transparent_image = Image.fromarray(image_data)

    # 保存为 PNG 以保留透明背景
    transparent_image.save(output_path)

    print(f"保存透明背景图片到: {output_path}")


if __name__ == "__main__":
    image = "3eda1fe37f17891820c7f464981925c4.png"  # 图片路径
    output = "output_image.png"  # 输出文件路径
    change_background_to_transparent(image, output)
