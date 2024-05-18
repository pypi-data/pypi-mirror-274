import cv2
import torch
from PIL import Image
from matplotlib import pyplot as plt

def display_data(dataloader, class_names=[],hw=[1,5]):
    images, labels = next(iter(dataloader))
    fig, axes = plt.subplots(hw[0],hw[1],figsize=(15, 6))  # 调整图像尺寸以避免图像被压缩得太小
    axes = axes.flatten()  # 将axes数组展平为一维数组
    for i in range(hw[0]*hw[1]):  #
        # 根据images的类型区分要不要改变形状
        if isinstance(images[i], torch.Tensor):
            # 如果是张量
            if images[i].dim() == 3 and images[i].size(0) == 3:
                # 彩色图片，不需要转置
                image_data = images[i].clone()  # 复制张量以防止影响原始数据
            else:
                # 其他情况，如灰度图片或单通道图片，需要转置
                image_data = images[i].permute(1, 2, 0).clone()
            axes[i].imshow(image_data)
        if class_names:
            axes[i].set_title(class_names[labels[i]])
        axes[i].axis('off')
    plt.show()