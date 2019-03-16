import numpy as np
import os
import pandas as pd

fileName = '..\\config\\car.txt'
temp = []
with open(fileName, 'r') as f:
    xx = f.read()
    print(xx)
    temp.append(xx)

# df = pd.read_table(fileName)
CARS = temp[0].split('\n')
print(CARS)