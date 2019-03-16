from func import *
from pattern import *
from loading import *

filePath = 'C:\\Users\\13937\\Desktop\\华为软挑\\SDK\\SDK_python\\CodeCraft-2019\\config'
carPath = filePath + '\\' + 'car.txt'
roadPath = filePath + '\\' + 'road.txt'
crossPath = filePath + '\\' + 'cross.txt'

[carInfo, carData]      = carLoading(carPath)
[roadInfo, roadData]    = carLoading(roadPath)
[crossInfo, crossData]  = carLoading(crossPath)

edges, vset = topoEstablish(roadData, crossData)

for k in edges.keys():
    temp = edges[k]
    print(k, temp)
for v in vset:
    print(v.vid, v.outList)