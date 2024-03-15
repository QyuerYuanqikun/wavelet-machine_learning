from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, concatenate, Activation, Dropout
from tensorflow.keras.models import Model

def conv2d_block(input_tensor, n_filters, kernel_size=3):
    # 卷积块
    x = input_tensor
    for i in range(2):
        x = Conv2D(filters=n_filters, kernel_size=(kernel_size, kernel_size), kernel_initializer='he_normal', padding='same')(x)
        x = Activation('relu')(x)
    return x

def get_unet(input_img, n_filters=64):
    # 编码器
    c1 = conv2d_block(input_img, n_filters=n_filters*1, kernel_size=3)
    p1 = MaxPooling2D((2, 2))(c1)
    p1 = Dropout(0.1)(p1)

    c2 = conv2d_block(p1, n_filters=n_filters*2, kernel_size=3)
    p2 = MaxPooling2D((2, 2))(c2)
    p2 = Dropout(0.1)(p2)

    c3 = conv2d_block(p2, n_filters=n_filters*4, kernel_size=3)
    p3 = MaxPooling2D((2, 2))(c3)
    p3 = Dropout(0.2)(p3)

    c4 = conv2d_block(p3, n_filters=n_filters*8, kernel_size=3)
    p4 = MaxPooling2D((2, 2))(c4)
    p4 = Dropout(0.2)(p4)

    c5 = conv2d_block(p4, n_filters=n_filters*16, kernel_size=3)

    # 解码器
    u6 = UpSampling2D((2, 2))(c5)
    u6 = concatenate([u6, c4])
    u6 = Dropout(0.2)(u6)
    c6 = conv2d_block(u6, n_filters=n_filters*8, kernel_size=3)

    u7 = UpSampling2D((2, 2))(c6)
    u7 = concatenate([u7, c3])
    u7 = Dropout(0.2)(u7)
    c7 = conv2d_block(u7, n_filters=n_filters*4, kernel_size=3)

    u8 = UpSampling2D((2, 2))(c7)
    u8 = concatenate([u8, c2])
    u8 = Dropout(0.1)(u8)
    c8 = conv2d_block(u8, n_filters=n_filters*2, kernel_size=3)

    u9 = UpSampling2D((2, 2))(c8)
    u9 = concatenate([u9, c1])
    u9 = Dropout(0.1)(u9)
    c9 = conv2d_block(u9, n_filters=n_filters*1, kernel_size=3)

    outputs = Conv2D(12, (1, 1), activation='sigmoid')(c9)
    model = Model(inputs=[input_img], outputs=[outputs])
    return model

# 定义模型输入
input_img = Input((None, None, 12), name='img')
model = get_unet(input_img, n_filters=64)

model.compile(optimizer='adam', loss='mean_squared_error')
model.summary()

import numpy as np
import os

def load_wavelet_coefficients(npy_file_path):
    """从.npz文件加载小波系数"""
    data = np.load(npy_file_path)
    # 将系数堆叠，形成模型期望的格式
    coeffs = np.stack((data['cA'], data['cH'], data['cV'], data['cD']), axis=-1)
    return coeffs

def prepare_dataset(noisy_dir, clean_dir):
    """准备数据集，加载噪声和干净的小波系数"""
    x = []  # 噪声图片系数
    y = []  # 干净图片系数
    filenames = os.listdir(noisy_dir)
    for filename in filenames:
        noisy_path = os.path.join(noisy_dir, filename)
        clean_path = os.path.join(clean_dir, filename)
        if os.path.isfile(noisy_path) and os.path.isfile(clean_path):
            x.append(load_wavelet_coefficients(noisy_path))
            y.append(load_wavelet_coefficients(clean_path))
    return np.array(x), np.array(y)

# 指定噪声图片和干净图片的小波系数存放路径
noisy_dir = 'E:\\wavelet\\wavelet coefficient\\Gauss\\test'
clean_dir = 'E:\\wavelet\\wavelet coefficient\\source\\test'

# 加载数据集
x_train, y_train = prepare_dataset(noisy_dir, clean_dir)

# 注意：根据您的实际数据情况，可能需要进一步调整数据形状或类型

