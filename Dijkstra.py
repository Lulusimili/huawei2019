import pandas as pd
import numpy as np
from loading import *
from pattern import *
from func import *
def get_unknown_min(vset,vlist):
    """
    #此函数则代替优先队列的出队操作
    :param vset: 有假数据的列表
    :param vlist: 没有假数据的集合，方便进行删除
    :return: 找到的最小距离的节点
    """
    the_min = 0
    the_index = 0
    j = 0
    for v1 in vset:
        if(v1.know is True):
            continue
        else:
            if(j == 0):
                the_min = v1.dist
                the_index = v1.vid
            else:
                if(v1.dist < the_min):
                    the_min = v1.dist
                    the_index = v1.vid
            j += 1
    #此时已经找到了未知的最小距离的元素是谁
    vlist.remove(vset[the_index]) #相当于执行出队操作
    return vset[the_index]

def update(vset,i,edges,vlist):
    """
    更新节点信息
    :param vset:
    :param i: 第i个节点作为顶点
    :param edges:
    :param vlist:
    :return:
    """
    vset[i].dist = 0

    while(len(vlist) != 0):
        vt = get_unknown_min(vset,vlist)
        #print(vt.vid, vt.dist, vt.outList)  # 打印出来顶点到某一节点的最短距离，以及这个节点的邻接节点（可以到达的节点）
        vt.know = True
        for w in vt.outList:  # w为索引
            v = vset[int(w)]
            if (v.know is True):
                continue
            if (v.dist == float('inf')):
                v.dist = vt.dist + edges[(vt.vid, v.vid)]
                v.prev = vt.vid
                print('v.vid:',v.vid,'v.prev:',v.prev)
            else:
                if ((vt.dist + edges[(vt.vid, int(w))]) < v.dist):
                    v.dist = vt.dist + edges[(vt.vid, v.vid)]
                    v.prev = vt.vid
                    print('v.vid:', v.vid, 'v.prev:', v.prev)
                else:  # 原来的路径更小一点，所以没有必要更新
                    pass


#用递归的方法得到任意起点到终点的最短路径
def real_get_traj(start,index,vset):
    traj_list = []

    def get_traj(index): #参数是顶点在cvlist中的索引
        if(index == start): #终点
            traj_list.append(index)

            print(traj_list[::-1]) #反抓list，得到从起点到终点的路径
            return
        if(vset[index].dist == float('inf')):
            print('从起点到该顶点根本没有路径')
            return
        traj_list.append(index)
        print('prev',vset[index].prev)
        get_traj(vset[index].prev)  #因为环的存在，这里递归出现了问题
    get_traj(index)
    print('该最短路径的长度为',vset[index].dist)