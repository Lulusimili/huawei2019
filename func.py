#实现各种功能函数
import pandas as pd
import numpy as np
from loading import *
from pattern import *
from copy import deepcopy


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

def findSrcVid(carDataArray, sortedVset):
    """
    找到车的出发节点
    :param carDataArray: 车辆数据， 格式[id,from,to,speed,planTime]
    :return:
    """
    src = carDataArray[1]
    return sortedVset[src]

def findDesVid(carDataArray, sortedVset):
    """
    找到车的目标节点
    :param carDataArray: 车辆数据， 格式[id,from,to,speed,planTime]
    :return:
    """
    src = carDataArray[2]
    return sortedVset[src]


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
        if (1 == road[6]):
            add_edge(front=road[5], back=road[4], value=road[1])        # 回向
        else:
            continue


    # 创建顶点对象
    # (id,roadId,roadId,roadId,roadId)， -1为无
    #   0    1     2      3       4
    falseVid = Vertex(None, [None, None, None, None])
    vset = [falseVid]                                                   #为了索引方便
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
                # assert curr_roadID != -1
                currRoad = roadData[np.where(roadData[:, 0] == curr_roadID)[0]]
                # assert len(currRoad) != 0
                # print(currRoad)
                indexs = np.where(newCrossData[:, 1:] == curr_roadID)[0]    #np.where返回两个索引，[0]是列方向上索引
                trueIndex = indexs[indexs != currentNodeID].astype(int)     #一条道路有两端，排除自己的那一段
                trueIndex = int(trueIndex)
                # print('currentCross:', i)
                # print('trueIndex: ', trueIndex)
                # print('carFrom:', currRoad[0, 1])
                # print(type(trueIndex))
                if (trueIndex == int(currRoad[0, 4])) & (int(currRoad[0, 6]) == 0):     #如果某条单向道路，des为本节点，则不添加其src节点
                    #                          from                    isDuplex
                    temp_outList = temp_outList
                else:
                    temp_outList.append(trueIndex)

        tempV = Vertex(currentNodeID, temp_outList)
        vset.append(tempV)

    # 确保vset是按照vid的大小排序，并且与索引对应，eg: A.vid == 1, sortedVset[1] == A
    # 虽然我觉得没啥必要
    sortedVset = [1] * len(vset)
    sortedVset[0] = falseVid
    for v in vset[1:]:
        idx = v.vid
        sortedVset[idx] = v

    assert len(vset) == len(sortedVset)
    # return edges, vset
    return edges, sortedVset

# def getUnknownMin(srcNode, vList， vset):
#     """
#     找到从srcNode出发的最短路径
#     :param srcNode:  出发节点
#     :param vList:   节点列表, 包含一个假节点，在索引0处
#     :return:   返回位置元素中，距离最小的
#     """
#     # vset = set(vList[1:])
#
#     theMin = 0
#     theIdx = 0
#     j = 0
#
#     for i in range(1, len(vList)):
#         if (vList[i].know is True):
#             continue
#         else:
#             if(0 == j):                 # 初始化
#                 theMin = vList[i].dist
#                 theIdx = i
#             else:
#                 if(theMin > vList[i].dist):
#                     theMin = vList[i].dist
#                     theIdx = [i]
#             j += 1
#
#         # 不断更新theIdx后，已经探明最近的节点
#         # 将他从vset（未探明节点集合？）中删除
#
#     vset.remove(vList[theIdx])
#     return vList[theIdx]



def OSPF(src, des, vList_origin, edges):
    """
    返回OSPF最短路径
    后期可能会添加p-坚持算法
    :param srcNode:     源节点， vertex对象
    :param desNode:     目的节点， vertex对象
    :param vList:       整个节点列表
    :param edges:       用以索引的边缘列表
    :return:
    """
    vList = deepcopy(vList_origin[:])
    # vList = vList_origin[:]

    # vset = set(deepcopy(vList[1:]))
    vset = set(vList[1:])

    # print(len(vset), 'inside')

    def getUnknownMin():
        """
        找到从srcN ode出发的最短路径
        :param srcNode:  出发节点
        :param vList:   节点列表, 包含一个假节点，在索引0处
        :return:   返回位置元素中，距离最小的
        """
        # vset = set(vList[1:])

        theMin = 0
        theIdx = 0
        j = 0
        # print('aaa   aaa')
        for i in range(1, len(vList)):
            if (vList[i].know is True):
                continue
            else:
                if (0 == j):  # 初始化
                    # print('come here')
                    theMin = vList[i].dist
                    theIdx = i
                else:
                    if (theMin > vList[i].dist):
                        theMin = vList[i].dist
                        theIdx = i
                j += 1

        # 不断更新theIdx后，已经探明最近的节点
        # 将他从vset（未探明节点集合？）中删除
        # print(len(vset), 'length inside 1')
        vset.remove(vList[theIdx])
        # print(len(vset), 'length inside 2')

        return vList[theIdx]

    srcNode = vList[src]
    desNode = vList[des]

    # print('Src Node', srcNode.vid);  print('Src Node Dist', srcNode.dist)
    # print('Des Node', desNode.vid);

    srcNode.dist = 0

    # 更新距离
    while(len(vset) != 0):                                  # 当未知节点集合非空
        # print(srcNode.vid, '*****************\n')

        vNode = getUnknownMin()

        # print('Debug Session 1')
        # print(vset)

        # print(vNode.vid, vNode.dist, vNode.outList)          # 打印出来顶点到某一节点的最短距离，以及这个节点的邻接节点（可以到达的节点）
        vNode.know = True
        for w in vNode.outList:                             # w对应的是索引
            # print('w in outList:', w)
            a = int(w)
            # print(a)
            if(vList[a].know is True):                      # 在当前节点的出表内遍历
                continue
            if(vList[a].dist == float('inf')):
                vList[a].dist = vNode.dist + edges[(vNode.vid, a)]
                # print('added dist:', edges[(vNode.vid, a)])
                # print('current dist:', vList[a].dist)
                vList[a].prev = vNode.vid
            else:
                if(vNode.dist + edges[(vNode.vid, a)] < vList[a].dist):
                    vList[a].dist = vNode.dist + edges[(vNode.vid, a)]
                    vList[a].prev = vNode.vid
                else:
                    pass

    def getFinalRoutine(start, end):
        """
        得到任意一对节点间的最短路径
        首先确保所有节点的前驱已经更新
        :param start:   起始节点（可与终端节点互换）
        :param end:     终端节点
        :return:        路径列表rtList
        """
        # for v in vList[1:]:
        #     if 0 == v.prev:
        #         raise Exception("This node hasn't been discovered", v.vid)
            # 此处默认不会出现没有路径的情况，假定为全联通
        rtList = []
        def getTrace(end):
            if (start == end):                  # 反向回溯, 已经回溯到源节点
                rtList.append(end)
                # print(rtList[::-1], 'function inside')
                return
            if vList[end].dist == float('inf'):
                print('No route')
                return
            rtList.append(end)
            getTrace(vList[end].prev)
        getTrace(end)
        return rtList[::-1]

    rt = getFinalRoutine(srcNode.vid, desNode.vid)

    return rt




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


def writeListToStr(dataList):
    """
    将dataList中的元素，作为一行写入，返回一个字符串对象
    元素间用','间隔
    :param dataList:    dataList中的元素，保证都是int类型, 或者是np.array类型
    :return:
    """
    result = ''
    for i in range(len(dataList)-1):
        result += str(dataList[i]) + ','
    result += str(dataList[-1])
    return result

