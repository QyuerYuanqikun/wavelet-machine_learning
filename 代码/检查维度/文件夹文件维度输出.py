import numpy as np
import os

def scan_npz_files(folder_path):
    # 遍历文件夹中的所有文件
    for file in os.listdir(folder_path):
        # 检查文件扩展名是否为.npz
        if file.endswith('.npz'):
            file_path = os.path.join(folder_path, file)
            # 加载npz文件
            data = np.load(file_path)
            # 输出文件名和数组维度
            print(f"File: {file}")
            # npz文件可能包含多个数组，遍历所有键
            for key in data.keys():
                print(f"  Key: {key}, Shape: {data[key].shape}")

# 指定你的npz文件所在的文件夹路径
folder_path = 'E:\\wavelet\\wavelet coefficient\\Gauss\\test'
scan_npz_files(folder_path)
