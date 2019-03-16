import logging
import sys
from loading import *
from pattern import *
from func import *

logging.basicConfig(level=logging.DEBUG,
                    # filename='../logs/CodeCraft-2019.log',

                    # 需要修改

                    filename='./logs/CodeCraft-2019.log',



                    #需要修改
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    [carInfo, carData] = carLoading(car_path)
    [roadInfo, roadData] = carLoading(road_path)
    [crossInfo, crossData] = carLoading(cross_path)

# to read input file
#     print(111)
# process

# to write output file


if __name__ == "__main__":
    main()