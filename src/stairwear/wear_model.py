"""Original Q8 equations; dimensions and normalisation are discussed in README."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as colors

def archard_wear(K, F, s, H):
    """
    计算磨损深度。

    参数：
    - K: 磨损系数（无量纲）
    - F: 施加的力（牛顿）
    - s: 滑动距离（米）
    - H: 硬度（帕斯卡）

    返回：
    - 磨损深度（米）
    """
    return (K * F * s) / H

class Material:
    def __init__(self, name, hardness, wear_coefficient):
        """
        参数：
        - name: 材料名称
        - hardness: 硬度（帕斯卡）
        - wear_coefficient: 磨损系数（无量纲）
        """
        self.name = name
        self.hardness = hardness
        self.wear_coefficient = wear_coefficient

class Step:
    def __init__(self, material, width, depth, resolution=100):
        """
        参数：
        - material: 材料对象
        - width: 台阶宽度（米）
        - depth: 台阶深度（米）
        - resolution: 网格分辨率（分成多少个网格）
        """
        self.material = material
        self.width = width
        self.depth = depth
        self.resolution = resolution
        # 初始化磨损深度网格（单位：米）
        self.wear_depth = np.zeros((resolution, resolution))
        # 生成网格坐标
        self.x = np.linspace(0, width, resolution)
        self.y = np.linspace(0, depth, resolution)
        self.X, self.Y = np.meshgrid(self.x, self.y)

    def apply_wear(self, force_distribution, s):
        """
        应用磨损。

        参数：
        - force_distribution: 2D 数组，每个网格单元施加的力（牛顿）
        - s: 滑动距离（米）
        """
        wear = archard_wear(
            K=self.material.wear_coefficient,
            F=force_distribution,
            s=s,
            H=self.material.hardness
        )
        self.wear_depth += wear

    def visualize_wear_contour(self, title='磨损深度等高线图'):
        plt.figure(figsize=(8, 6))
        contour = plt.contourf(self.X, self.Y, self.wear_depth * 1000, cmap='inferno')
        plt.colorbar(contour, label='磨损深度（毫米）')
        plt.xlabel('宽度（米）')
        plt.ylabel('深度（米）')
        plt.title(title)
        plt.show()

    def visualize_wear_3d(self, title='磨损深度3D图'):
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        norm = colors.Normalize(vmin=self.wear_depth.min(), vmax=self.wear_depth.max())
        surf = ax.plot_surface(self.X, self.Y, self.wear_depth * 1000, cmap=cm.inferno,
                               linewidth=0, antialiased=False, norm=norm, alpha=0.9)
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='磨损深度（毫米）')
        ax.set_xlabel('宽度（米）')
        ax.set_ylabel('深度（米）')
        ax.set_zlabel('磨损深度（毫米）')
        ax.set_title(title)
        # 调整视角
        ax.view_init(elev=30, azim=225)
        plt.show()

class User:
    def __init__(self, direction, F_total, s, lateral_std=0.05):
        """
        参数：
        - direction: 'up' 或 'down'（上楼或下楼）
        - F_total: 用户施加的总力（牛顿）
        - s: 用户通过台阶时的滑动距离（米）
        - lateral_std: 用户横向位置的标准差（米）
        """
        self.direction = direction
        self.F_total = F_total
        self.s = s
        self.lateral_std = lateral_std  # 横向位置标准差

    def get_force_distribution(self, step: Step):
        """
        返回力分布。

        参数：
        - step: 台阶对象

        返回：
        - 2D 力分布数组（牛顿）
        """
        # 横向位置服从正态分布，中心为台阶中点
        lateral_position = np.random.normal(loc=step.width / 2, scale=self.lateral_std)
        lateral_position = np.clip(lateral_position, 0, step.width)

        # 根据方向确定力的分布区域
        if self.direction == 'up':
            y_force_center = 0.3 * step.depth
        else:
            y_force_center = 0.7 * step.depth

        # 高斯分布参数
        sigma_x = step.width / 10
        sigma_y = step.depth / 10

        # 计算二维高斯力分布
        force_distribution = self.F_total * np.exp(
            -(((step.X - lateral_position) ** 2) / (2 * sigma_x ** 2) +
              ((step.Y - y_force_center) ** 2) / (2 * sigma_y ** 2))
        )
        return force_distribution
