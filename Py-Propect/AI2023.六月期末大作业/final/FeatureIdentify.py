# ##此文件用于计算未知设备的各个状态与已知设备最小欧氏距离
#
import numpy as np
#
known_devices = {
    'YD1落地风扇': {
        '1档': np.array([144.5862, 145, 1, 284.3103, 147.500, 882.8103]),
        '2档': np.array([161.3333, 162, 18, 332.333, 132.0000, 926.0000]),
        '3档': np.array([174.8814, 176, 2, 381.0339, 80.9153, 975.7797])
    },
    'YD2微波炉': {
        '低火': np.array([5935.5000, 5976, 81, 11412.9615, 2599.4615, 872.077]),
        '中低火': np.array([5854.9375, 5904, 93, 11309.5625, 2436.0938, 876.6250]),
        '中火': np.array([5758.2500, 5823, 136, 11183.9531, 2271.5625, 881.3125]),
        '中高火': np.array([5591.625, 5698, 198, 10952.1429, 2056.1964, 888.2321]),
        '高火': np.array([5422.4136, 5541, 225, 10754.6852, 1886.8086, 895.8272])
    },
    'YD3热水壶': {
        '打开': np.array([7815.0811, 7924, 131, 17045.5541, 20.1892, 999.000])
    },
    'YD4电脑': {
        '睡眠': np.array([32.8095, 33, 1, 9.2619, 64.6905, 133.0714]),
        '重启': np.array([239.9138, 339, 158, 241.448, 69.1379, 455.3793])
    },
    'YD5白炽灯': {
        '打开': np.array([183.0953, 184, 1, 407.3810, 6.2063, 998.000])
    },
    'YD6节能灯': {
        '打开': np.array([41.0476, 42, 1, 53.1429, 11.111, 580.1429])
    },
    'YD7打印机': {
        '打开': np.array([28.9750, 29, 1, 7.0500, 57.4500, 115.450]),
        '打印': np.array([3812.8571, 3922, 221, 8375.85, 87.5714, 996.000]),
        '结束': np.array([48.3333, 49, 1, 37.9877, 54.8765, 353.395]),
        '复印': np.array([3236.823, 5304, 4849, 5875.29, 127.000, 786.647]),
        '扫描': np.array([110.7879, 143, 41, 111.954, 53.4621, 453.568])
    },
    'YD8饮水机': {
        '加热': np.array([1821.7692, 1829, 18, 3993.33, 5.6154, 998.984]),
        '制冷': np.array([348.6739, 491, 390, 455.427, 81.5507, 565.695]),
        '加热制冷': np.array([2017.9363, 2121, 254, 4385.16, 73.7182, 990.300]),
        '保温': np.array([9.0625, 10, 1, 6.5938, 0.2031, 324.437])
    },
    'YD9挂式空调': {
        '制冷': np.array([143.7014, 160, 27, 214.328, 217.656, 647.552]),
        '辅热': np.array([122.7543, 126, 7, 149.824, 202.929, 530.982])
    },
    'YD10吹风机': {
        '1档热风': np.array([2027.3106, 2090, 68, 2534.29, 2419.17, 571.825]),
        '1档冷风': np.array([790.4603, 793, 4, 1558.74, 252.015, 893.984]),
        '2档热风': np.array([5962.9904, 5986, 32, 12981.4, 88.1154, 999.000]),
        '2档冷风': np.array([1423.4912, 1428, 6, 3129.43, 75.3158, 999.000])
    },
    'YD11电视机': {
        '打开': np.array([537.2373, 543, 7, 1089.32, 353.440, 901.627])
    }
}



unknown_devices ={
    '设备1': {
        'state1': np.array([24.9748, 27, 4, 23.4194, 1.871, 418.5323]),
        'state2': np.array([1843.5606, 1855, 29, 4081.5225, 6.516, 999])
    },
    '设备2': {
        'state1': np.array([141.7902, 155, 25, 210.75, 212.9, 627.9167]),
        'state2': np.array([123.9776, 127, 6, 153.4286, 203.1228, 539.9825]),
    }
}

# 初始化最小距离和最匹配的状态与设备
min_distance = float('inf')
matched_state = None
matched_device = None

# 遍历每个未知设备特征向量
for unknown_device, state_vectors in unknown_devices.items():
    for state, feature_vector in state_vectors.items():
        # 遍历每个已知设备
        print()
        print("当前未知设备向量：")
        print(f"{state}", feature_vector)
        for device, known_state_vectors in known_devices.items():
            # 遍历已知设备的每个状态特征向量
            for known_state, known_feature_vector in known_state_vectors.items():
                # 计算欧氏距离
                #distance = np.linalg.norm(feature_vector - known_feature_vector)
                distance = np.sqrt(np.sum(np.square( feature_vector - known_feature_vector)))
                print(f"当前检测设备：{device}", f"当前检测状态：{known_state}", f"当前欧氏距离：{distance}")

                # 更新最小距离和最匹配的状态与设备
                if distance < min_distance:
                    min_distance = distance
                    matched_state = state
                    matched_device = device
                #print(f"当前检测设备：{device}", f"当前检测状态：{known_state}", f"当前欧氏距离：{min_distance}")

        # 输出当前未知设备的最匹配的状态和设备
        #print(feature_vector)
        print(f"未知设备状态: {state}", unknown_device)
        print("最匹配的状态:", matched_state, f"   所属设备:", matched_device)
        #print("所属设备:", matched_device)
        print("欧氏距离:", min_distance)
        print()

    # 重置最小距离和最匹配的状态与设备
    min_distance = float('inf')
    matched_state = None
    matched_device = None

