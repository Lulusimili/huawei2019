import numpy as np
import pandas as pd
import os

def carLoading(car_path):
    """
    读取车辆数据，返回数值化数据
    :param car_path: 文件名
    :return: [Info, data]
    """
    with open(car_path) as f:
        temp = f.read()
    temp = temp.split('\n')
    Info = temp[0]                # 得到说明
    temp = temp[1:]                     # 截取数据段

    for i in range(len(temp)):          #字符串操作，得到数据内容
        temp[i] = temp[i][1:-1].split(', ')

    # 转化数据类型，int型，array数组存储
    data = np.array(pd.DataFrame(temp)).astype(int)

    return [Info, data]



def outputs(carID_data, carRouteDict, carTimeDict, filePath):
    """
    输出路线txt文档
    :param carList:
    :return:
    """
    #(carID, time, rtList)

    pass

