import numpy as np

if __name__ == '__main__':
    t = int(input())
    for arr_count in range(t):
        # get data
        n = int(input())
        arr = input().split(" ")
        x, y, p, q = input().split(" ")
        x = int(x)
        y = int(y)
        p = int(p)
        q = int(q)
        # run
        dis_x = np.mean(p - x)
        dis_y = np.mean(q - y)
        dis_largest = 0
        for num in arr:
            dis_largest += int(num)
        if dis_largest < dis_x + dis_y:
            print("NO")
            break

        print("YES")
