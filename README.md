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

# Pruning

## 目標
給定 1px 寬帶分支的線條，將小於一給定長度的分岔消除。

## 步驟

1. 使用相鄰像素中輪廓點的數量來判斷該點為尖端(1)、線條(2)或分岔點(>2)
2. 找到所有的端點，並開始沿著線條方向向分支點搜索並記錄長度
3. 如果長度低於給定值則記錄並在最後一起移除並輸出

## 用法

```
usage: pruning.py [-h] [-i IMAGE] [-l LENGTH]

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        image name
  -l LENGTH, --length LENGTH
                        max length to prune
```

example:
```
python pruning.py -i image.jpg -l 5
```

## 效果

原圖

![原圖](<pruning_images/iscoolrev.bmp> "原圖")

```
python pruning.py -i iscool.bmp -l 3
```
剪 3 格以下，可以看見 I 的左下和 S 的兩個尾巴被剪了

![剪 3 格以下](<pruning_images/pruned_image_3.bmp> "剪 3 格以下")

```
python pruning.py -i iscool.bmp -l 15
```
剪 15 格以下，可以看見 I 的左上和 L 的尾巴也被剪了

![剪 15 格以下](<pruning_images/pruned_image_15.bmp> "剪 15 格以下")

```
python pruning.py -i iscool.bmp -l 30
```
剪 30 格以下，可以看見最長的 C 頭上也被剪了

![剪 30 格以下](<pruning_images/pruned_image_30.bmp> "剪 30 格以下")
