import os


def rename_ogg_to_mp3(directory):
    # 遍历指定目录中的所有文件
    for filename in os.listdir(directory):
        # 检查文件是否以.ogg结尾
        if filename.endswith('.ogg'):
            # 构建新的文件名
            new_filename = filename[:-4] + '.mp3'
            # 构建完整的文件路径
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)
            # 重命名文件
            os.rename(old_file_path, new_file_path)
            print(f'Renamed: {old_file_path} -> {new_file_path}')


if __name__ == '__main__':
    # 指定要处理的目录
    directory = r'E:\\音乐'
    rename_ogg_to_mp3(directory)
