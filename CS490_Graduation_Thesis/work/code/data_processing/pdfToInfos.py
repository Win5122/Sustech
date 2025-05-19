import io
import os
import shutil

import fitz
import pdfplumber
import pytesseract
from PIL import Image

# 添加这行代码（路径根据实际安装位置调整）
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def get_txt(in_path):
    """
    提取PDF文字内容
    """
    reports = {}
    full_text = []
    with pdfplumber.open(in_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            # 页数编码标签
            page_tip = "\n# page " + str(page_number) + ":" if page_number != 1 else "# page 1:"
            # 优先提取文本
            text = page.extract_text()
            if text and text.strip():
                full_text.append(text)
            else:
                # 处理扫描件图片OCR
                # print("need use OCR to scan")
                # return "failed"
                img = page.to_image(resolution=300).original
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                img = Image.open(img_bytes)
                ocr_text = pytesseract.image_to_string(img, lang='chi_sim')  # 支持中文OCR
                full_text.append(ocr_text)

    # # get all contents
    # contents_start_num = 0
    # for num, text in enumerate(full_text):
    #     if text.count("目录") > 0 or text.count("Contents") > 0 or text.count("Table of Content"):
    #         contents_start_num = num
    #         break
    # if contents_start_num == 0:
    #     return "failed"
    # contents_start = full_text[contents_start_num].replace(full_text[contents_start_num].split("\n")[-1], "")
    # first_content = contents_start.split("\n")[1].split(". . .")[0].strip()
    # if full_text[contents_start_num + 1].startswith(first_content):
    #     contents = contents_start
    # else:
    #     contents = contents_start + full_text[contents_start_num + 1].replace(
    #         "\n" + full_text[contents_start_num + 1].split("\n")[-1], "")
    # contents = contents.split('\n')
    # for num, content in enumerate(contents):
    #     contents[num] = content.removesuffix(content.split(" ")[-1])
    #     contents[num] = contents[num].split(". . .")[0].strip()
    #     contents[num] = contents[num].split("...")[0].strip()
    #
    # # get all first level contents
    # first_level_content_list = []
    # first_level_content_pattern = r'^\d+\.(?:\s*)[\u4e00-\u9fa5a-zA-Z]+.*?(?=\s*$)'
    # for content in contents:
    #     if re.match(first_level_content_pattern, content):
    #         first_level_content_list.append(content)
    #     # elif content.count("参考文献") > 0:
    #     #     first_level_content_list.append(content)
    #     # elif content.count("附录") > 0:
    #     #     first_level_content_list.append(content)
    #     # elif content.count("致谢") > 0:
    #     #     first_level_content_list.append(content)
    #
    # # divide full text into parts according to the first level contents
    # full_text = re.sub(r'^(\d+)\.\s+', r'\1.', "\n".join(full_text))
    # for num, content in enumerate(first_level_content_list):
    #     apart = full_text.split(content)
    #     full_text = content + apart[-1]
    #     reports[num] = content.join(apart).replace(full_text, "")
    # reports[len(reports)] = full_text
    return "\n".join(full_text)


def get_img(in_path, img_path):
    """
    提取PDF所有图片
    """
    # 创建图片文件夹
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    # 读取PDF文件
    pdf_document = fitz.open(in_path)

    # 遍历每一页
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)

        # 提取图片
        for img_index, img in enumerate(image_list):
            xref = img[0]  # 图片的交叉引用编号
            base_image = pdf_document.extract_image(xref)
            image_data = base_image["image"]
            image_form = base_image["ext"]
            image_name = ""
            for i, info in enumerate(base_image):
                if info == 'image':
                    continue
                image_name += ("" if i == 0 else "_") + f"{info}-{base_image[info]}"
            image_filename = os.path.join(img_path,
                                          f"page_{page_number + 1}_image_{img_index + 1}_{image_name}.{image_form}")

            # 保存图片
            with open(image_filename, "wb") as img_file:
                img_file.write(image_data)
            print(f"成功保存图片: {image_filename}")

    # 如果目录为空，删除目录
    if not os.listdir(img_path):
        shutil.rmtree(img_path)


if __name__ == "__main__":
    # all_folders = ["2023本科论文", "2023组内毕设", "2024本科论文"]
    folder_list = ["2023本科论文", "2023组内毕设", "2024本科论文"]

    for folder in folder_list:
        print(f"正在处理：{folder}")

        # 指定要遍历的文件夹路径
        folder_path = rf"D:\Sustech\course\CS490_Graduation_Thesis\work\data-preprocessed\{folder}\pdf"
        output_path = rf"D:\Sustech\course\CS490_Graduation_Thesis\work\data-preprocessed\{folder}\txt"
        images_path = rf"D:\Sustech\course\CS490_Graduation_Thesis\work\data-preprocessed\{folder}\image"

        for file in os.listdir(folder_path):
            if file.endswith(".pdf"):
                print(f"正在处理：{file}")

                pdf_path = os.path.join(folder_path, file)

                txt_path = os.path.join(output_path, file.replace(".pdf", ".txt"))
                txt = get_txt(pdf_path)
                if txt == "failed":
                    continue
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(txt)
                # for i in range(len(txt)):
                #     txt_file = txt_path.replace(".txt", rf"\part{i + 1}.txt")
                #     os.makedirs(os.path.dirname(txt_file), exist_ok=True)
                #     with open(txt_file, "w", encoding="utf-8") as f:
                #         f.write(txt[i])

                get_img(pdf_path, images_path + "\\" + file.replace(".pdf", ""))

                print(f"处理完成：{file}\n")

        print(f"处理完成：{folder}\n")
