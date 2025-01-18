from PIL import Image


def compress_image(image_path, output_path, quality=100):
    # 打开原始图片
    with Image.open(image_path) as img:
        # 保存压缩后的图片
        img.save(output_path, format='JPEG', quality=quality)


if __name__ == '__main__':
    image = "poster-2.jpg"  # 图片路径
    output = "output_image.jpg"  # 输出文件路径
    compress_image(image, output, quality=97)
