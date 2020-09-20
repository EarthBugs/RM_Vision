
import cv2
import numpy as np 
import time 

import preprocess as pp
import lightfilter as lf


#9.17
#对高光通道与高饱和红色通道做与运算。其中红色通道由 红色减蓝色结果二值化的结果 与 红色减绿色结果二值化的结果 进行与运算得到
#可在水平60°左右开始抓取，45°左右稳定抓取
debug_mode = True #单帧调试模式
file_dir = 'test_videos\\' + 'blue_c.mp4' #视频路径
highlight_thr = 230  #高光通道阈值
color_type = 1 #灯条颜色参数，0为红，1为蓝，默认红
color_thr = 110  #颜色通道饱和度阈值
draw_color = (255, 0, 0)  #绘制颜色
capture = cv2.VideoCapture(file_dir)

while(True):
    ret,frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    preprocessed = pp.preprocess(highlight_thr,gray,color_thr,frame,color_type)
    #获得融合处理后的选择图

    contours, hierarchy = cv2.findContours(preprocessed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #寻找最终图中的目标轮廓

    final_box,final_rect = lf.get_final_box(contours)
    #获得板子的框选区域坐标二维数组

    try:
        cv2.drawContours(frame, [final_rect], -1, (0,255,0), 3)
        for i in range(len(final_box)):
            cv2.drawContours(frame, [final_box[i]], -1, draw_color, 2)
    except:
        pass
    #绘制在原图上

    #Roi_next = Roi_get(final_rect,frame)
    #得到用于下一帧的ROI

    cv2.imshow('final_pic',preprocessed)
    cv2.imshow('final_pic_ora',frame)

    if debug_mode:
       cv2.waitKey(0)

    if cv2.waitKey(30) == ord('q'):
        break