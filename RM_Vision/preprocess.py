import cv2
import numpy as np 
import time

#  自定义函数：用于颜色通道处理
#  输入 1：color_thr：颜色通道饱和度阈值
#  输入 2：frame：原图
#  返回值：color_img：合成后的颜色筛选图
def color_deal(color_thr,frame,color_type=0):
    #分离出B,G,R三色通道
        (b,g,r) = cv2.split(frame)
        
        if color_type == 0:
            sub_rg = cv2.subtract(r, g)
            sub_rb = cv2.subtract(r, b)
            #得到红色减蓝，绿通道的单通道图

            ret,res_rg = cv2.threshold(sub_rg,color_thr,255, cv2.THRESH_BINARY)
            ret,res_rb = cv2.threshold(sub_rb,color_thr,255, cv2.THRESH_BINARY)
            #分别筛选出红-蓝，红-绿通道的高饱和度
            final = cv2.bitwise_and(res_rg,res_rb)
            #位运算融合
        if color_type == 1:
            sub_bg = cv2.subtract(b, g)
            sub_br = cv2.subtract(b, r)
            #得到蓝减红，绿通道的单通道图

            ret,res_bg = cv2.threshold(sub_bg,color_thr,255, cv2.THRESH_BINARY)
            ret,res_br = cv2.threshold(sub_br,color_thr,255, cv2.THRESH_BINARY)
            #分别筛选出蓝-绿，蓝-红通道的高饱和度
            final = cv2.bitwise_and(res_bg,res_br)
            #位运算融合
        kernelx = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
        color_img = cv2.dilate(final, kernelx)
        #膨胀结果
        return color_img

#  自定义函数：用于高通道处理
#  输入 1：highlight_thr：高光通道阈值
#  输入 2：gray：原图灰度图
#  返回值：highlight_img：高光通道图
def highlight_deal(highlight_thr,gray):
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        #将原图像进行高斯滤波，过滤掉高噪音
        ret,imged = cv2.threshold(blur,highlight_thr,255, cv2.THRESH_BINARY)
        #二值化出高光通道

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 7))
        highlight_img = cv2.dilate(imged, kernel)
        #对原高光通道进行膨胀操作
        return highlight_img

#  自定义函数：用于对高光图和色图做与运算
#  输入 1：highlight_thr：高光通道阈值
#  输入 2：gray：原图灰度图
#  输入 3：color_thr：色图阈值
#  输入 4：frame：原图
#  输入 4：color_type：蓝红模式，默认为0红色
#  返回值：preprocessed：处理后的融合图
def preprocess(highlight_thr,gray,color_thr,frame,color_type=0):

    highlight_img = highlight_deal(highlight_thr,gray)
    color_img = color_deal(color_thr,frame,color_type)

    kernele = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    preprocessed = cv2.bitwise_and(img_color,img_high)
    #高通道和色融合图进行与运算
    preprocessed = cv2.dilate(preprocessed, kernele)
    #膨胀最终图

    cv2.imshow('highlight_dilated',highlight_img)
    cv2.imshow('color_dilated',color_img)

    return preprocessed