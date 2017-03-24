在终端中用ASCII字符播放视频，不是什么新鲜玩意了，只是今天突然想写来玩一玩。

# 用法
```
$ ./ascii_video.py -h
ascii_video.py -i <inputfile> [-s <speed>]
-i: 指定输入视频文件
-s: 播放速度, 与硬件性能有关, 默认为10, 数值越大越快
运行中按q退出, 按p暂停/恢复
```

- 不仅对视频，对图片也可以用。
- 调小终端字体可以提高效果，但是性能就呵呵了……
- 自适应终端大小，但是比例默认拉伸为16:9

# 依赖库

本来想直接用C++和ffmpeg来解码视频，但是太复杂了搞得头大，所以就用Python+OpenCV这个组合了。
- OpenCV
- numpy
- curses
- FFmpeg

# 系统
我在Ubuntu 16.04上写的，Python版本3.5，默认终端。其他系统和终端模拟器没有测试过，我自己也只拿几个视频跑了一下。

# 效果

| 原始                                       | ASCII                                    |
| ---------------------------------------- | ---------------------------------------- |
| ![bad_apple.png](https://raw.githubusercontent.com/xiadong1994/ascii-video-player/master/samples/bad_apple.png) | ![bad_apple_ascii](https://raw.githubusercontent.com/xiadong1994/ascii-video-player/master/samples/bad_apple_ascii.png) |
| ![](https://raw.githubusercontent.com/xiadong1994/ascii-video-player/master/samples/hyouka.png) | ![](https://raw.githubusercontent.com/xiadong1994/ascii-video-player/master/samples/hyouka_ascii.png) |
| ![](https://raw.githubusercontent.com/xiadong1994/ascii-video-player/master/samples/kobayashi.png) | ![](https://raw.githubusercontent.com/xiadong1994/ascii-video-player/master/samples/kobayashi_ascii.png) |
| ![](https://raw.githubusercontent.com/xiadong1994/ascii-video-player/master/samples/konosuba.png) | ![](https://raw.githubusercontent.com/xiadong1994/ascii-video-player/master/samples/konosuba_ascii.png) |