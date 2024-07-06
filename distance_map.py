from cmath import inf
import cv2
import numpy as np
import math
import argparse 

class Point():
    def __init__(self):
        self.is_edit = True
        self.nearest = []
        self.distance_square = inf
        self.angle = []

def find_nearest_map(image):

    border_image = cv2.copyMakeBorder(image, 1, 1, 1, 1, borderType=cv2.BORDER_CONSTANT)    # 上下左右擴充 1px

    # 初始化記錄訊息的圖
    distance_map = np.empty((border_image.shape[0], border_image.shape[1]), dtype=Point)
    for y in range(border_image.shape[0]):
        for x in range(border_image.shape[1]):
            distance_map[y, x] = Point()
    # 邊緣不會修改
    for y in range(border_image.shape[0]):
        distance_map[y, 0].is_edit = distance_map[y, border_image.shape[1] - 1].is_edit = False
    for x in range(border_image.shape[1]):
        distance_map[0, x].is_edit = distance_map[border_image.shape[0] - 1, x].is_edit = False
    
    # 迭代直到每像素穩定
    is_stable = False
    while not is_stable:
        is_stable = True
        # 遍歷每個像素
        for y in range(1, border_image.shape[0] - 1):
            for x in range(1, border_image.shape[1] - 1):
                if distance_map[y, x].is_edit:
                    is_stable = False
                distance_map[y, x].is_edit = False

                # 輪廓點最近點即是自身
                if image[y - 1, x - 1] == 255:
                    distance_map[y, x].distance_square = 0
                    distance_map[y, x].nearest.append((y, x))
                    continue

                # 檢查 8 相鄰點的每個最近點與自身的距離
                for j in range(-1, 2):
                    for i in range(-1, 2):
                        for point in distance_map[y + j, x + i].nearest:
                            if point in distance_map[y, x].nearest: # 跳過已經就是最近的點
                                continue
                            distance_square = (y + j - point[0]) ** 2 + (x + i - point[1]) ** 2 # 計算距離
                            if distance_square <= distance_map[y, x].distance_square:
                                if not distance_map[y, x].is_edit:  # 第一次清空列表
                                    distance_map[y, x].nearest = []
                                    distance_map[y, x].is_edit = True
                                if distance_square < distance_map[y, x].distance_square:    # 找到更小值也清空列表
                                    distance_map[y, x].nearest = []
                                distance_map[y, x].nearest.append(point)
                                distance_map[y, x].distance_square = distance_square
                                # print('find new nearest point at: ')

    # 計算角度
    for y in range(1, border_image.shape[0] - 1):
        for x in range(1, border_image.shape[1] - 1):
            for point in distance_map[y, x].nearest:
                distance_map[y, x].angle.append(math.atan2(point[0] - y, point[1] - x))
    
    return distance_map
                                
def visualize_distance_map(image, distance_map):

    output_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

    # 找出最遠距離作為比例尺
    max_distance = 1
    for y in range(1, distance_map.shape[0] - 1):
        for x in range(1, distance_map.shape[1] - 1):
            if distance_map[y, x].distance_square > max_distance:
                max_distance = distance_map[y, x].distance_square
    max_distance = max_distance ** 0.5

    # 依照角度與越遠越鮮豔的距離著色
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image[y, x] == 255:
                output_image[y, x] = (0, 0, 255)
                continue
            hue = math.floor(179 * (distance_map[y + 1, x + 1].angle[0] + math.pi) / (2 * math.pi))
            saturation = math.floor(200 * (distance_map[y + 1, x + 1].distance_square ** 0.5) / max_distance)
            output_image[y, x] = (hue, 55 + saturation, 255)
    
    output_image = cv2.cvtColor(output_image, cv2.COLOR_HSV2BGR)    # HSV 轉 RGB

    cv2.imwrite('distance_map.png', output_image)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', type=str, help='image name', default='input.bmp')
    args = parser.parse_args()

    image = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    distance_map = find_nearest_map(image)
    visualize_distance_map(image, distance_map)
