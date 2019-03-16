#实现各种功能函数
import pandas as pd
import numpy as np
from loading import *
from pattern import *


# 演示文档中最好自己设置下car_path这些文件路径

# car_path = ?
# cross_path = ?
# road_path = ?
#
# [carInfo, carData] = carLoading(car_path)
# [roadInfo, roadData] = carLoading(road_path)
# [crossInfo, crossData] = carLoading(cross_path)

DIRECTION_DICT= {(1, 2): 1, (1, 3): 0, (1, 4): 2,
                 (2, 1): 2, (2, 3): 1, (2, 4): 0,
                 (3, 1): 0, (3, 2): 2, (3, 4): 1,
                 (4, 1): 1, (4, 2): 0, (4, 3): 2}

def topoEstablish(roadData, crossData):
    """
    建立道路拓扑， 返回一个拓扑lidt
    :param crossData:
    :return: 节点和边拓扑list: edges--字典类型, vset--列表类型
    """
    # 创建路径link
    edges = {}                          # 有向路线，link
    def add_edge(front, back, value):
        edges[(front, back)] = value;

    for road in roadData:
        #'#(id,length,speed,channel,from,to,isDuplex)'
        #   0   1       2       3     4   5     6
        add_edge(front= road[4], back= road[5], value= road[1])         # 去向
        if road[6]:
            add_edge(front=road[5], back=road[4], value=road[1])        # 回向
        else:
            pass


    # 创建顶点对象
    # (id,roadId,roadId,roadId,roadId)， -1为无
    #   0    1     2      3       4
    vset = [None]                                                       #为了索引方便
    noUse = np.array([[-1, -1, -1, -1, -1]])
    newCrossData = np.concatenate((noUse, crossData), axis=0)           #生成一个新数组，方便索引和crossId对应
    for i in range(1,len(newCrossData)):
        currentNode = newCrossData[i]
        currentNodeID = newCrossData[i][0]
        temp_outList = []                                               # 存储邻接节点ID，因为数据newCrossData中id和索引下相同
                                                                        # 所以直接存储索引
        for curr_roadID in currentNode[1:]:
            if curr_roadID == -1:
                continue                                                # -1表示此方向没有道路连接，直接pass
            else:
                indexs = np.where(newCrossData[:, 1:] == curr_roadID)[0]    #np.where返回两个索引，[0]是列方向上索引
                trueIndex = indexs[indexs != currentNodeID].astype(int)
                temp_outList.append(trueIndex)
        tempV = Vertex(currentNodeID, temp_outList)
        vset.append(tempV)

    return edges, vset




def judgeDirection(roadFrom, roadTo, crossData, directionDic = DIRECTION_DICT):
    """
    通过道路判断执行，左转，还是右转
    :param roadFrom:    通过路口前的道路ID，源道路
    :param roadTo:      通过路口后的道路ID，目的道路
    :param crossData:
    :return: 0--Go Straight, 1--Turn Left, 2--Turn Right
    """
    idx1 = np.where(crossData == roadFrom)[0]       # 找到源道路连接的路口, 取行索引
    idx2 = np.where(crossData == roadTo)[0]         # 找到目的道路连接的路口, 取行索引

    # 求交集
    idxNeed = idx1[idx1 == idx2]
    cross = crossData[idxNeed]
    tag_src = np.where(cross == roadFrom)[1].astype(int)        # cross为单行数据，所以取列索引
    tag_des = np.where(cross == roadTo)[1].astype(int)

    # 方向判断
    drct = DIRECTION_DICT[(tag_src, tag_des)]

    return drct

def calcuDistance(routineList, edges):
    """
    计算路径的总距离
    :param routineList: 路径list，包含始发点和终点
    :param edges: 链路字典
    :return: 路径cover的总距离
    """
    length = len(routineList)
    dis = 0
    for i in range(length-1):
        src = routineList[i]
        des = routineList[i+1]
        dis += edges[(src, des)]
    return dis

