import pandas as pd


def check_data(data_path1, data_path2):
    # 读取两个CSV文件
    df1 = pd.read_csv(data_path1)
    df2 = pd.read_csv(data_path2)

    # 对列排序，使列顺序一致
    df1 = df1.reindex(sorted(df1.columns), axis=1)
    df2 = df2.reindex(sorted(df2.columns), axis=1)

    # 对行排序
    df1_sorted = df1.sort_values(by=df1.columns.tolist()).reset_index(drop=True)
    df2_sorted = df2.sort_values(by=df2.columns.tolist()).reset_index(drop=True)

    # 比较是否相同
    if df1_sorted.equals(df2_sorted):
        print("两个CSV文件内容相同")
        return True
    else:
        print("两个CSV文件内容不同")
        return False


if __name__ == '__main__':
    for i in range(5, 6):
        print(f'checking task{i}')
        path1 = f'./results/r{i}.csv'
        path2 = f'./all/r{i}.csv'
        if check_data(path1, path2):
            print('pass\n')
        else:
            print('fail\n')
