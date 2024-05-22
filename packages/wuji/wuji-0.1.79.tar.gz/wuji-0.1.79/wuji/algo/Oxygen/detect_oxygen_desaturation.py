#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   detect_oxygen_desaturation
@Time        :   2023/4/25 14:41
@Author      :   Xuesong Chen
@Description :
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SPO2_MIN_VALUE = 110


def detect_oxygen_desaturation(spo2_arr, duration_max=120, spo2_des_min_thre=3, ret_format='df'):
    spo2_max = spo2_arr[0]  # 初始化最大值
    spo2_max_index = 1  # 初始化最大值下标
    spo2_min = SPO2_MIN_VALUE  # 初始化血氧最低值
    des_onset_pred_set = []  # 算法预测氧降起始点总集
    des_duration_pred_set = []  # 算法预测氧降持续时间总集
    des_level_set = []  # 被记录的氧降事件合集
    des_onset_pred_point = 0  # 预测事件起始点
    des_flag = 0  # 氧降事件发生标记
    ma_flag = 0  # motion artifact事件发生标记
    spo2_des_max_thre = 50  # 血氧motion artifact阈值
    duration_min = 5  # 氧降事件至少持续duration_min s才会被记录在内
    prob_end = []

    for i, current_value in enumerate(spo2_arr):
        des_percent = spo2_max - current_value  # 氧降值

        # 检测Motion artifacts
        if ma_flag and (des_percent < spo2_des_max_thre):
            if des_flag and prob_end:
                des_onset_pred_set.append(des_onset_pred_point)
                des_duration_pred_set.append(prob_end[-1] - des_onset_pred_point)
                des_level_point = spo2_max - spo2_min
                des_level_set.append(des_level_point)
            # 重置
            spo2_max = current_value
            spo2_max_index = i
            ma_flag = 0
            des_flag = 0
            spo2_min = SPO2_MIN_VALUE
            prob_end = []
            continue

        # 如果氧降值大于设置的阈值
        if des_percent >= spo2_des_min_thre:
            if des_percent > spo2_des_max_thre:
                ma_flag = 1
            else:
                des_onset_pred_point = spo2_max_index
                des_flag = 1
                if current_value < spo2_min:
                    spo2_min = current_value

        if current_value >= spo2_max and not des_flag:
            spo2_max = current_value
            spo2_max_index = i

        elif des_flag:
            if current_value > spo2_min:
                if current_value > spo2_arr[i - 1]:
                    prob_end.append(i)

                if current_value <= spo2_arr[i - 1] < spo2_arr[i - 2]:
                    spo2_des_duration = prob_end[-1] - spo2_max_index
                    if spo2_des_duration < duration_min:
                        spo2_max = spo2_arr[i - 2]
                        spo2_max_index = i - 2
                        spo2_min = SPO2_MIN_VALUE
                        des_flag = 0
                        prob_end = []
                        continue
                    else:
                        if duration_min <= spo2_des_duration <= duration_max:
                            des_onset_pred_set.append(des_onset_pred_point)
                            des_duration_pred_set.append(spo2_des_duration)
                            des_level_point = spo2_max - spo2_min
                            des_level_set.append(des_level_point)
                        else:
                            des_onset_pred_set.append(des_onset_pred_point)
                            des_duration_pred_set.append(prob_end[0] - des_onset_pred_point)
                            des_level_point = spo2_max - spo2_min
                            des_level_set.append(des_level_point)
                            remain_spo2_arr = spo2_arr[prob_end[0]:i + 1]
                            _onset, _duration, _des_level = detect_oxygen_desaturation(remain_spo2_arr, ret_format='tuple')
                            des_onset_pred_set.extend([i + prob_end[0] for i in _onset])
                            des_duration_pred_set.extend(_duration)
                            des_level_set.extend(_des_level)
                        spo2_max = spo2_arr[i - 2]
                        spo2_max_index = i - 2
                        spo2_min = SPO2_MIN_VALUE
                        des_flag = 0
                        prob_end = []

    if ret_format == 'tuple':
        return des_onset_pred_set, des_duration_pred_set, des_level_set
    else:
        return pd.DataFrame({
            'Type': 'OD',
            'Start': des_onset_pred_set,
            'Duration': des_duration_pred_set,
            'OD_level': des_level_set
        })


if __name__ == '__main__':
    data = np.load('/Users/cxs/Downloads/gt_spo2.npz')
    from wuji.tools.plot_labeled_signal import plot_signal_with_events
    from wuji.algo.Oxygen.desaturation_wrapper import detect_desaturation
    gt_spo2 = data['spo2']
    import time
    s_t = time.time()
    i = 0
    while i < 1000:
        res = detect_desaturation(gt_spo2)
        i += 1
    print(time.time() - s_t)
    plot_signal_with_events(gt_spo2, 1, res)
    # plt.plot(gt_spo2)
    # plt.show()