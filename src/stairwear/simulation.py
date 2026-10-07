import numpy as np
from scipy.stats import poisson
from .wear_model import User,Step

class Simulation:
    def __init__(self, step: Step, users_per_day, s, days, up_ratio, lateral_std=0.05, time_interval_minutes=1, peak_flow=50, off_peak_flow=10):
        """
        参数：
        - step: 台阶对象
        - users_per_day: 每日用户总数
        - s: 滑动距离（米）
        - days: 仿真天数
        - up_ratio: 上楼用户比例
        - lateral_std: 横向位置标准差
        - time_interval_minutes: 时间间隔（分钟）
        - peak_flow: 高峰期每时间间隔用户数量
        - off_peak_flow: 非高峰期每时间间隔用户数量
        """
        self.step = step
        self.users_per_day = users_per_day
        self.s = s
        self.days = days
        self.up_ratio = up_ratio
        self.lateral_std = lateral_std
        self.time_interval = time_interval_minutes
        self.peak_flow = peak_flow
        self.off_peak_flow = off_peak_flow

    def run(self):
        """
        执行仿真。
        """
        peak_hours = [(8, 10), (17, 19)]  # 高峰时段
        total_time_intervals = int(24 * 60 / self.time_interval)

        for day in range(1, self.days + 1):
            for interval in range(total_time_intervals):
                current_time = (interval * self.time_interval) / 60
                is_peak = any(start <= current_time < end for (start, end) in peak_hours)
                expected_users = self.peak_flow if is_peak else self.off_peak_flow
                num_users = poisson.rvs(expected_users)

                num_up = int(num_users * self.up_ratio)
                num_down = num_users - num_up

                cumulative_force = np.zeros_like(self.step.wear_depth)
                for _ in range(num_up):
                    user = User('up', 500, self.s, self.lateral_std)
                    cumulative_force += user.get_force_distribution(self.step)
                for _ in range(num_down):
                    user = User('down', 900, self.s, self.lateral_std)
                    cumulative_force += user.get_force_distribution(self.step)

                self.step.apply_wear(cumulative_force, self.s)
