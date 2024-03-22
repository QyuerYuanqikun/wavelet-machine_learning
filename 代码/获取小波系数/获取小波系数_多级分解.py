import pywt
import cv2
import numpy as np
import os

def save_wavelet_coeffs(coeffs_rgb, output_dir, filename):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    coeffs_dict = {}
    for i, color in enumerate(['r', 'g', 'b']):
        for j, coeffs in enumerate(coeffs_rgb[i]):
            # 适当修改以确保使用正确的键
            flatten_coeffs(coeffs, f'{color}_{j}', coeffs_dict)
    np.savez_compressed(os.path.join(output_dir, filename), **coeffs_dict)

def flatten_coeffs(coeffs, prefix, coeffs_dict):
    if isinstance(coeffs, tuple):
        # 处理非最低级的系数
        coeffs_dict[f'{prefix}_cA'] = coeffs[0]
        if isinstance(coeffs[1], tuple):
            # 如果还有下一级，则继续递归处理
            flatten_coeffs(coeffs[1], prefix, coeffs_dict)
        else:
            # 处理最低级别的细节系数
            for i, coeff in enumerate(coeffs[1]):
                coeffs_dict[f'{prefix}_c{i}'] = coeff
    else:
        # 最低级别的处理，如果直接传入的是系数数组
        coeffs_dict[prefix] = coeffs

def apply_wavelet_transform(image_path, wavelet='haar', level=2):
    image = cv2.imread(image_path)
    coeffs_rgb = []
    for i in range(3):
        coeffs = pywt.wavedec2(image[:, :, i], wavelet, level=level)
        coeffs_rgb.append(coeffs)
    return coeffs_rgb

def process_images(input_dir, output_dir, wavelet='haar', level=2):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
            img_path = os.path.join(input_dir, filename)
            coeffs_rgb = apply_wavelet_transform(img_path, wavelet, level)
            save_wavelet_coeffs(coeffs_rgb, output_dir, os.path.splitext(filename)[0])

# 定义图片数据集目录和小波系数保存目录
input_dir = 'E:\\wavelet\\Image\\Flickr1024 Dataset\\Test_same_size_512'
output_dir = 'E:\\wavelet\\wavelet coefficient\\source_djfj_512\\test'

# 处理图像并保存小波系数
process_images(input_dir, output_dir, 'coif1', 3)  # 使用Coiflet1小波进行3级分解
