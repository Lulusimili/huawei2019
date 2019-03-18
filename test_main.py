from func import *
from pattern import *
from loading import *
from Dijkstra import *
import logging


logging.basicConfig(level=logging.DEBUG,
                    # filename='../logs/CodeCraft-2019.log',

                    # 需要修改

                    # filename='./logs/CodeCraft-2019.log',
                    filename='./logs/temp.log',

                    #需要修改
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


filePath = 'C:\\Users\\13937\\Desktop\\华为软挑\\SDK\\SDK_python\\CodeCraft-2019\\config'
carPath = filePath + '\\' + 'car.txt'
roadPath = filePath + '\\' + 'road.txt'
crossPath = filePath + '\\' + 'cross.txt'
answerPath = filePath + '\\' + 'answer.txt'

[carInfo, carData]      = carLoading(carPath)
[roadInfo, roadData]    = carLoading(roadPath)
[crossInfo, crossData]  = carLoading(crossPath)

edges, vList = topoEstablish(roadData, crossData)

# for k in edges.keys():
#     temp = edges[k]
#     print(k, temp)
#


# for c in carData:
#      for v in vset:
#           v.know = False
#
#      vlist = vset.copy()
#      vlist = set(vlist)
#      vlist.remove(vset[0])
#
#      src = findSrcVid(c, vset)
#      des = findDesVid(c, vset)
#      print('src:', src.vid, 'des:', des.vid)
#      update(vset, src.vid, edges, vlist)
#      real_get_traj(src.vid, des.vid, vset)

# print('***************************************\n')



# print(len(vset))
# for v in vList:
#     print(v.vid, v.outList)

# 随机选取一辆车
# r = np.random.randint(len(carData))
# r = 10
# car_r = carData[r]
# car_r_src = car_r[1]
# car_r_des = car_r[2]
#
# print(carData[0])

# for r in range(1, len(carData))

# print('************** process -1 *****************')
# mm = OSPF(src= car_r_src, des= car_r_des, vList_origin= vset, edges= edges)
# print(mm)
count = 1

carRouteDict = {}
carTimeDict = {}

for car in carData:
    # print(count)
    c_id  = car[0]
    c_src = car[1]
    c_des = car[2]
    c_speed = car[3]

    # print('COUNTER: ', count)
    # print('counter:', count)

    c_rt = OSPF(c_src, c_des, vList, edges)
    carRouteDict[c_id] = c_rt
    sumDist = calcuDistance(c_rt, edges)

    minTime = sumDist / c_speed
    reguMinTime = np.ceil(minTime)              #向上取整

    carRouteDict[c_id] = c_rt
    carTimeDict[c_id] = reguMinTime
    # text = [c_id, c_src, c_des, sumDist, minTime, c_rt]
    text = [c_id, c_src, c_des, sumDist, minTime]
    count += 1
    # print('Counter: ', count, '\t\t', text)
    # print(len(vList), 'outside')

    logging.info("answer_path is %s" % (text))


with open(answerPath, 'w') as ans:
    ans.writelines('#(carId,StartTime,RoadID_List)\n')

    startTime = 0

    for carID in carData[:, 0]:
        idStr = str(int(carID))
        # timeStr = str(int(carTimeDict[carID]))
        planTime = startTime + carTimeDict[carID]
        timeStr = str(int(planTime))
        startTime += carTimeDict[carID]
        rtStr = writeListToStr(carRouteDict[carID])
        l = '(' + idStr + ',' + timeStr + ',' + rtStr + ')' + '\n'
        ans.writelines(l)




