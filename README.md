# Shade-Finder
A very simple tool to find the darker regions of an image.

## 目標
給定任意的影像，找出影像裡看起來比周遭暗，即亮度差距超過一定值的區塊，且該區塊像素個數必須介於一區間之間。

## 步驟

1. 先將整個影像分成數個區塊，透過 Canny 演算法計算邊緣
    1. 將影像灰階化
    2. 做高斯模糊去除噪音
    3. 計算每個像素之八方向梯度，梯度高於 threshold1 標記為強邊緣，低於 threshold1 但高於 threshold2 另外標記為弱邊緣
    4. 可以連結強邊緣的弱邊緣也標記為邊緣
2. 將邊緣膨脹並腐蝕一定像素數，試圖偵測形狀的缺口並將其封閉
3. 計算每一個區域之平均亮度，並根據區域面積將區域膨脹一定的像素數，計算區域周圍的平均亮度
4. 標記亮度差距與面積符合限制的區塊

## 用法

```
usage: mark_shade.py [-h] [-i IMAGE] [-b BRIGHTNESS] [-g GAP] [-c CANNY CANNY] [-s SIZE SIZE]

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        image name
  -b BRIGHTNESS, --brightness BRIGHTNESS
                        brightness threshold
  -g GAP, --gap GAP     gaps fix level
  -c CANNY CANNY, --canny CANNY CANNY
                        Canny's algorithm's weak/strong thresholds
  -s SIZE SIZE, --size SIZE SIZE
                        area size min/max thresholds
```

example:
```
python mark_shade.py -i image.jpg -b 30 -g 5 -c 30 100 -s 100 10000
```

## 效果

參數

```
python main.py -i pigeon.jpg -b 30 -c 30 100 -s 100 1000000
```

原圖

![原圖](<example_images/pigeon/pigeon.jpg> "原圖")

灰階

![灰階](<example_images/pigeon/gray.jpg> "灰階")

邊緣

![邊緣](<example_images/pigeon/edges.jpg> "邊緣")

原圖+暗區標記

![原圖+暗區標記](<example_images/pigeon/contours.jpg> "原圖+暗區標記")

灰階+暗區標記

![灰階+暗區標記](<example_images/pigeon/brightness.jpg> "灰階+暗區標記")