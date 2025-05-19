import os
import shutil
from pathlib import Path

import comtypes.client


def find_and_copy_pdfs(source_folder, target_folder):
    """
    遍历源文件夹，找到所有 PDF 文件并复制到目标文件夹
    @param source_folder: 源文件夹路径（str或Path对象）
    @param target_folder: 目标文件夹路径（str或Path对象）
    """
    target_path = Path(target_folder)
    target_path.mkdir(parents=True, exist_ok=True)  # 自动创建目标文件夹
    source_path = Path(source_folder)

    # 使用递归glob匹配
    for pdf_file in source_path.rglob(f"*.pdf"):
        target_file = target_path / pdf_file.name
        # 处理文件名冲突（自动添加序号）
        if target_file.exists():
            continue
        # 显式转换为字符串
        shutil.copy2(str(pdf_file), str(target_file))
        print(f"已复制: {pdf_file} -> {target_file}")

    # 使用递归glob匹配
    for docx_file in source_path.rglob(f"*.docx"):
        input_file = str(docx_file)
        output_file = str(target_path / f"{docx_file.stem}.pdf")
        # 处理文件名冲突（自动添加序号）
        counter = 1
        if Path(output_file).exists():
            continue
        # 初始化COM对象
        word = comtypes.client.CreateObject('Word.Application')
        # 设置为不可见模式（不打开Word应用程序）
        word.Visible = False
        # 打开Word文档
        doc = word.Documents.Open(input_file)
        # 保存为PDF文件
        doc.SaveAs(output_file, FileFormat=17)  # 17 是PDF格式的代码
        # 关闭文档
        doc.Close()
        # 退出Word应用程序
        word.Quit()
        print(f"已复制: {input_file} -> {output_file}")


def rename_file(path):
    for file in os.listdir(path):
        if file.endswith(".pdf"):
            new_name = file
            while new_name.__contains__("+"):
                new_name = new_name.replace("+", "_")
            while new_name.__contains__("-"):
                new_name = new_name.replace("-", "_")
            file_path = os.path.join(path, file)
            new_file_path = os.path.join(path, new_name)
            os.rename(file_path, new_file_path)


if __name__ == "__main__":
    origin_list = ["2023本科论文", "组内毕设2023", "2024本科论文"]
    target_list = ["2023本科论文", "2023组内毕设", "2024本科论文"]

    for origin, target in zip(origin_list, target_list):
        print(f"正在处理：{origin}")

        # 指定要遍历的文件夹路径
        folder_path = rf"D:\Sustech\course\CS490_Graduation_Thesis\work\data-original\{origin}"
        output_path = rf"D:\Sustech\course\CS490_Graduation_Thesis\work\data-preprocessed\{target}\pdf"

        # 指定要搜索的文件扩展名
        find_and_copy_pdfs(folder_path, output_path)
        rename_file(output_path)

        print(f"处理完成：{origin}")
