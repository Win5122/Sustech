import numpy as np


def convolve(matrix, kernel):
    """
    对输入的矩阵进行卷积操作。

    参数:
    matrix (np.ndarray): 输入矩阵，形状为 (H, W)
    kernel (np.ndarray): 卷积核，形状为 (kH, kW)

    返回:
    np.ndarray: 卷积后的结果矩阵
    """
    # 获取矩阵和卷积核的尺寸
    H, W = matrix.shape
    kH, kW = kernel.shape

    # 计算输出矩阵的尺寸
    output_H = H - kH + 1
    output_W = W - kW + 1

    # 初始化输出矩阵
    output = np.zeros((output_H, output_W))

    # 遍历输入矩阵，进行卷积操作
    for i in range(output_H):
        for j in range(output_W):
            # 提取当前区域的子矩阵
            region = matrix[i:i + kH, j:j + kW]
            # 计算卷积结果
            output[i, j] = np.sum(region * kernel)
            if output[i, j] < 0:
                output[i, j] = 0

    return output


def softmax(z):
    """
    计算输入向量 z 的 softmax 值。

    参数:
    z (np.ndarray): 输入向量或矩阵，形状为 (N,) 或 (N, M)

    返回:
    np.ndarray: softmax 结果，与输入具有相同的形状
    """
    # 为了数值稳定性，减去最大值
    z_exp = np.exp(z - np.max(z, axis=-1, keepdims=True))
    # 计算分母（即指数值的总和）
    sum_z_exp = np.sum(z_exp, axis=-1, keepdims=True)
    # 计算 softmax
    return z_exp / sum_z_exp


def main():
    # 示例矩阵和卷积核
    matrix_list = [
        np.array([
            [2, -5, 3, 1, 5, 0],
            [8, 1, 0, 3, 3, 3],
            [-1, -1, -2, -1, -6, 0],
            [-3, 0, 6, -6, -1, 8],
            [0, -5, 1, 2, 1, -4],
            [-1, -3, 2, -3, -2, -4],
        ]),
        np.array([
            [14, 6],
            [24, 25],
        ]),
        np.array([
            [14, 6],
            [24, 25],
        ]),
        np.array([
            [14, 6],
            [24, 25],
        ]),
        np.array([
            [14, 6],
            [24, 25],
        ]),
        np.array([
            [14, 6],
            [24, 25],
        ]),
        np.array([
            [14, 6],
            [24, 25],
        ]),

    ]

    kernel_list = [
        np.array([
            [1, -3, 0],
            [-3, 2, -1],
            [0, -1, 1],
        ]),
        np.array([
            [2, 0],
            [1, -2],
        ]),
        np.array([
            [0, -1],
            [0, -2],
        ]),
        np.array([
            [-1, 2],
            [-1, 0],
        ]),
        np.array([
            [-2, 1],
            [0, 2],
        ]),
        np.array([
            [-2, 0],
            [-1, 0],
        ]),
        np.array([
            [0, -1],
            [2, -1],
        ]),
    ]

    A = [
        np.array([
            [-1, 1, -5],
            [2, -1, -1],
        ]),
        np.array([
            [-1, 1, -5],
            [2, -1, -1],
        ]),
    ]

    B = [
        np.array([
            [2],
            [0],
            [0],
        ]),
        np.array([
            [28],
            [0],
            [17],
        ]),
    ]

    for i in range(len(matrix_list)):
        matrix = matrix_list[i]
        kernel = kernel_list[i]

        # 执行卷积运算
        result = convolve(matrix, kernel)

        print(f"运行次数{i + 1}:")
        print("卷积结果:")
        print(f"{result}\n")

    for i in range(len(A)):
        a = A[i]
        b = B[i]

        # 执行卷积运算
        result = np.dot(a, b)

        print(f"运行次数{i + 1}:")
        print("乘法结果:")
        print(f"{result}\n")

    print("softmax结果:")
    print(f"{softmax(np.array([-2, 4]))}\n")

    print("softmax结果:")
    print(f"{softmax(np.array([-113, 39]))}\n")

    print()


if __name__ == '__main__':
    main()
