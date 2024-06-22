from cmath import inf
import cv2
import numpy as np
import argparse

def mark_shade(image, brightness_threshold = 1, gaps_fix_level = 0, canny_threshold = (0, 128), size_threshold = (0, inf)):

    # 使用 Canny 演算法標記邊緣
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)        # 轉灰階
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)     # 使用高斯模糊消除雜訊
    edges = cv2.Canny(blurred_image, canny_threshold[0], canny_threshold[1])
    
    # 將輪廓膨脹再腐蝕來修補缺口
    kernel = np.ones((gaps_fix_level, gaps_fix_level), np.uint8)
    closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # 偵測出封閉的區塊並標記
    inverse_closed_edges = cv2.bitwise_not(closed_edges)        # 反轉圖配合格式
    regions, markers, stats, centroids = cv2.connectedComponentsWithStats(inverse_closed_edges, connectivity=4)

    # 將邊緣變成 0
    markers = markers + 1
    markers[inverse_closed_edges == 0] = 0

    # 計算個別區塊與周圍區域亮度平均
    brightness = [0] * (regions + 1)
    surround_brightness = [0] * (regions + 1)

    # 逐區塊檢查
    output_image = np.zeros_like(gray_image)
    for label in range(1, regions + 1):     # 跳過邊緣標記 0

        # 膨脹操作
        area = stats[label - 1, cv2.CC_STAT_AREA]                                   # 原區塊面積
        original_mask = np.uint8(markers == label) * 255                            # 原區塊遮罩
        kernel = np.ones((int(2 * area ** 0.5), int(2 * area ** 0.5)), np.uint8)    # 依照原區域面積決定周圍區域的大小
        dilated_mask = cv2.dilate(original_mask, kernel, iterations=1)              # 膨脹後遮罩
        outer_mask = dilated_mask - original_mask                                   # 膨脹區域遮罩
        
        # 計算原圖與膨脹後區域亮度平均
        brightness[label] = np.sum(gray_image[original_mask > 0]) / area if area > 0 else 0
        outer_area = np.sum(outer_mask > 0)
        surround_brightness[label] = np.sum(gray_image[outer_mask > 0]) / outer_area if outer_area > 0 else 0

        # 將原圖畫成區塊亮度圖並在兩圖上標記白色邊緣
        output_image[markers == label] = brightness[label]
        if surround_brightness[label] - brightness[label] >= brightness_threshold and size_threshold[0] <= area <= size_threshold[1]:
            contours, _ = cv2.findContours(original_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(image, contours, -1, (255, 255, 255), 1)
            cv2.drawContours(output_image, contours, -1, 255, 1)

    cv2.imwrite('gray.jpg', gray_image)
    cv2.imwrite('edges.jpg', inverse_closed_edges)
    cv2.imwrite('contours.jpg', image)
    cv2.imwrite('brightness.jpg', output_image)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', type=str, help='image name', default='input.jpg')
    parser.add_argument('-b', '--brightness', type=int, help='brightness threshold', default=16)
    parser.add_argument('-g', '--gap', type=int, help='gaps fix level', default=3)
    parser.add_argument('-c', '--canny', type=int, help='Canny\'s algorithm\'s weak/strong thresholds', nargs=2, default=[50, 100])
    parser.add_argument('-s', '--size', type=int, help='area size min/max thresholds', nargs=2, default=[0, inf])
    args = parser.parse_args()

    image = cv2.imread(args.image, cv2.IMREAD_COLOR)
    mark_shade(image, args.brightness, args.gap, args.canny, args.size)
