import cv2
import numpy as np
import argparse 

def pruning(image, length=1):

    border_image = cv2.copyMakeBorder(image, 1, 1, 1, 1, borderType=cv2.BORDER_CONSTANT)    # 上下左右擴充 1px
    output_image = image.copy()
    discard = []

    # 找出所有尖端開始一路追溯到分岔點然後判斷長度
    for y in range(1, border_image.shape[0] - 1):
        for x in range(1, border_image.shape[1] - 1):
            if border_image[y][x] != 255:
                continue
            near = -1   # 因為會掃到自己所以從 -1 開始
            # 掃描以自己為中心的九宮格
            for i in range(3):
                for j in range(3):
                    near = near + 1 if border_image[y - i + 1][x - j + 1] == 255 else near
            if near == 1:   # 鄰近的線點有 1 個即是尖端
                x2, y2 = x, y
                route = []
                # 追溯到分岔點
                while True:
                    border_image[y2][x2] = 0    # 先把自己塗黑以讓標記下一點容易
                    next = 0
                    near2 = 0
                    for i in range(3):
                        for j in range(3):
                            if border_image[y2 - i + 1][x2 - j + 1] == 255:
                                near2 += 1
                                next = (y2 - i + 1, x2 - j + 1) # 標記接下來的點
                    if near2 != 1:
                        border_image[y2][x2] = 255  # 走到岔點時記得將該點塗回白色
                        break
                    route.append((y2, x2))
                    y2, x2 = next
                if len(route) <= length:
                    for point in route:
                        discard.append(point)
    for point in discard:
        output_image[point[0] - 1][point[1] - 1] = 0
    return output_image

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', type=str, help='image name', default='input.bmp')
    parser.add_argument('-l', '--length', type=int, help='max length to prune', default=1)
    args = parser.parse_args()

    image = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    output_image = pruning(image, args.length)
    cv2.imwrite('pruned_image.bmp', output_image)
