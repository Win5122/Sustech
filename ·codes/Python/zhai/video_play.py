import cv2
import numpy as np
import serial
# import time  # 导入time模块用于等待
# import struct
import pickle

# # 视频文件的路径
# video_path = r"Y:\文件\嵌入式\assignment3\video_material.mp4"
# # 创建视频读取对象
# cap = cv2.VideoCapture(video_path)
#
# # 检查视频是否成功打开
# if not cap.isOpened():
#     print("Error: Could not open video.")
#     exit()
#
# # 获取视频的帧率
# fps = cap.get(cv2.CAP_PROP_FPS)
#
# # 计算每秒需要处理的帧数
# frames_per_second = 1
#
# # 计算每帧的时间间隔（以帧为单位）
# frame_interval = int(fps / frames_per_second)
#
# 创建串口对象
ser = serial.Serial("COM6", 1000000, 8, "N", 1, timeout=None)
ser.dtr = False
ser.rts = False
# # 存储处理后的帧数据
# all_frame_data = []
#
# # 读取视频帧
# frame_count = 0
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     # 检查是否是我们需要处理的帧
#     if frame_count % frame_interval == 0:
#         # 转换为RGB颜色空间
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#         # 缩放图片到45x60
#         resized_frame = cv2.resize(frame_rgb, (60, 45), interpolation=cv2.INTER_AREA)
#
#         # 获取图像的尺寸
#         height, width = resized_frame.shape[:2]
#
#         # 创建一个空的数组来存储16位的像素值
#         frame_16bit = np.zeros((height, width), dtype=np.uint16)
#
#         # 将RGB图像转换为16位真色彩（RGB565格式）
#         for y in range(height):
#             for x in range(width):
#                 r = np.uint16((resized_frame[y, x, 0] >> 3)) << 11  # 红色5位
#                 g = np.uint16((resized_frame[y, x, 1] >> 2)) << 5  # 绿色6位
#                 b = (resized_frame[y, x, 2] >> 3) & 0x1F  # 蓝色5位
#                 frame_16bit[y, x] = r | g | b
#
#         # 将图像转换为一维数组
#         flat_array = frame_16bit.flatten()
#
#         # 存储处理后的帧数据
#         all_frame_data.append(flat_array)
#
#     frame_count += 1
#
#
# # 将所有帧数据保存为一个文件
# with open('all_frame_data.pkl', 'wb') as f:
#     pickle.dump(all_frame_data, f)

# 读取保存的数据
with open('all_frame_data.pkl', 'rb') as f:
    all_frame_data = pickle.load(f)

# 发送处理后的帧数据
for frame_index, frame_data in enumerate(all_frame_data):
    # 发送固定标志位
    frame_marker = 0x1234
    ser.write(frame_marker.to_bytes(2, byteorder='little'))  # 发送16位固定标志位
    # raw_data = ser.read(2)
    # index = struct.unpack('<2B', raw_data)
    # print(index)

    # 发送帧数据
    for value in frame_data:
        ser.write(value.astype(np.uint16).tobytes())  # 发送16位数据
        # 等待一秒钟
        # raw_data = ser.read(2)
        # index = struct.unpack('<2B', raw_data)
        # print(index)
        # if raw_data[0] == 0x55:
        #     try:
        #         if raw_data[1] == 0x53:
        #             index = struct.unpack('<2B', raw_data)
        #             aaa = index[1]
        #             print(aaa)
        #     except struct.error:
        #         print("error1551")
# 释放视频读取对象
# cap.release()
# 关闭串口
ser.close()

print("所有帧已发送完毕。")