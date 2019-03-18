import numpy as np
import os




class Car(object):
    # (id,from,to,speed,planTime)
    def __init__(self, car_dataArray):
        self.id         = car_dataArray[0]
        self.src        = car_dataArray[1]
        self.des        = car_dataArray[2]
        self.speed      = car_dataArray[3]
        self.planTime   = car_dataArray[4]

    def getRoute(self, rtList):
        self.route = rtList

    def calcuMaxTime(self, distance):
        self.minTime = distance / self.speed

class Cross(object):
    # (id,roadId,roadId,roadId,roadId)
    def __init__(self, cross_dataArray):
        self.id         =  cross_dataArray[0]
        self.road1      =  cross_dataArray[1]
        self.road2      =  cross_dataArray[2]
        self.road3      =  cross_dataArray[3]
        self.road4      =  cross_dataArray[4]

        self.outList    =  []                   #出表，由此节点向外，邻接表默认为空，有带后续建立
        self.inList     =  []                   #入表，由其他节点向自己
class Road(object):
    # (id,length,speed,channel,from,to,isDuplex)
    def __init__(self, road_dataArray):
        self.id         = road_dataArray[0]
        self.length     = road_dataArray[1]
        self.maxSpeed = road_dataArray[2]
        self.channel = road_dataArray[3]
        self.src = road_dataArray[4]
        self.des = road_dataArray[5]
        self.isDuplex = road_dataArray[6]                       #是否可以双向同行
        self.maxCapcity = self.channel * self.length            #单向，最大车容量


class Vertex(object): #顶点类
    def __init__(self,vid,outList):
        self.vid = vid #出边
        self.outList = outList #出边指向的顶点ID的列表，也可以理解为邻接表
        self.know = False #默认为假
        self.dist = float('inf') #顶点s到该点的距离默认为无穷大
        self.prev = 0 #上一个顶点的ID，默认为0


