import numpy as np
import os
import pandas as pd


# %%
def load_coeffs(npz_file_path):
    """
    从npz文件加载小波系数。
    """
    data = np.load(npz_file_path)
    return data['cA'], data['cH'], data['cV'], data['cD']


# %%
def adaptive_threshold(coeffs, ratio):
    """
    基于系数的能量自适应确定阈值，并根据阈值过滤系数。
    """
    coeff_flat = coeffs.flatten()
    squared_energy = np.square(coeff_flat)
    threshold = np.percentile(squared_energy, (1 - ratio) * 100)  # 基于能量百分位数确定阈值
    filtered_coeffs = coeff_flat * (squared_energy >= threshold)  # 保留高于阈值的系数
    return filtered_coeffs


# %%
def adjust_and_reduce_coeffs(coeffs, target_dims, ratio):
    """
    调整不同类型系数的能量比重，并应用自适应阈值进行降维。
    """
    reduced_coeffs = []
    for i, coeff in enumerate(coeffs):
        # 应用自适应阈值过滤
        filtered_coeffs = adaptive_threshold(coeff, ratio[i])
        # 确保降维到指定的维度
        reduced_coeffs.append(filtered_coeffs[:target_dims[i]])
    return np.concatenate(reduced_coeffs)


# %%
def process_folder(input_dir, output_dir, target_dims, ratio):
    """
    处理文件夹中的所有npz文件，并保存降维后的系数。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.npz'):
            file_path = os.path.join(input_dir, filename)
            cA, cH, cV, cD = load_coeffs(file_path)
            coeffs = [cA, cH, cV, cD]
            reduced_coeffs = adjust_and_reduce_coeffs(coeffs, target_dims, ratio)

            # 保存为Pandas DataFrame，适用于随机森林训练
            df = pd.DataFrame(reduced_coeffs.reshape(1, -1))
            output_file_path = os.path.join(output_dir, filename.replace('.npz', '.csv'))
            df.to_csv(output_file_path, index=False)


# %%
# 示例用法
input_dir = 'E:\\wavelet\\wavelet coefficient\\source\\test'
output_dir = 'E:\\wavelet\\wavelet coefficient\\source\\test_source_小波系数能量自适应阈值降维'
target_dims = [500, 166, 166, 167]  # 设置每种类型系数的目标维度
ratio = [0.9, 0.8, 0.8, 0.8]  # 设置自适应阈值的保留比例

process_folder(input_dir, output_dir, target_dims, ratio)