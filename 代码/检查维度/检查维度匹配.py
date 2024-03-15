import os
import numpy as np

# 定义目录路径
noise_dir = 'E:\\wavelet\\wavelet coefficient\\Gauss\\test'
source_dir = 'E:\\wavelet\\wavelet coefficient\\source\\test'

# 获取两个目录中的所有npz文件名
noise_files = {file for file in os.listdir(noise_dir) if file.endswith('.npz')}
source_files = {file for file in os.listdir(source_dir) if file.endswith('.npz')}

# 找到两个目录都存在的文件
common_files = noise_files.intersection(source_files)

# 用于记录维度不一致的文件名
mismatched_files = []

# 检查每个相同的文件
for file in common_files:
    # 加载npz文件
    noise_data = np.load(os.path.join(noise_dir, file))
    source_data = np.load(os.path.join(source_dir, file))

    # 比较文件的维度
    for key in noise_data.files:
        if key in source_data.files:
            if noise_data[key].shape != source_data[key].shape:
                mismatched_files.append(file)
                break  # 如果发现维度不匹配，不再比较其他key

# 输出维度不匹配的文件名
print("维度不匹配的文件:", mismatched_files)
