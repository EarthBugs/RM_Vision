import cv2
import numpy as np  

#  自定义函数：将最小矩形的四个坐标点进行左顶点-右顶点-右底点-左底点的排序
#  输入 1：最小矩形的四个坐标
#  输入 2：最小矩形的中点坐标
#  返回值：排序后的数组
def point_sort(box,mid_pointoint):
    sorted = np.empty([4,2])
    for i in (box):
        if (i[0]<=mid_pointoint[0])&(i[1]>=mid_pointoint[1]):
            left_top = i
            sorted[0] = left_top
        if (i[0]>=mid_pointoint[0])&(i[1]>=mid_pointoint[1]):
            right_top = i
            sorted[1] = right_top
        if (i[0]>=mid_pointoint[0])&(i[1]<=mid_pointoint[1]):
            right_down = i
            sorted[2] = right_down
        if (i[0]<=mid_pointoint[0])&(i[1]<=mid_pointoint[1]):
            left_down = i
            sorted[3] = left_down
    return sorted
    

#  自定义函数：用于筛选不是一组平行灯条的干扰
#  输入 1：所有灯条轮廓
#  输入 2：选定最低角度
#  输入 3：选定最高角度
#  返回值：正确平行灯条
def angle_filter(k,max_angle,min_angle):
    return (k >=min_angle) & (k <=max_angle)

#  自定义函数：用于获取灯条宽的中值坐标
#  输入 1：第一个点
#  输入 2：第二个点
#  返回值：中值坐标
def get_mid_point(fst,sec):
    mid_point = (fst + sec)*0.5
    mid_point = np.int0(mid_point)
    mid_point.resize((1,2))
    return mid_point

#  自定义函数：用于获取斜率
#  输入 1：第一中点
#  输入 2：第二中点
#  返回值：斜率
def cul_slope(point1,point2):
    point1 = point1[0]
    point2 = point2[0]
    if (point1[0]-point2[0])== 0:
        k=0
    else:
        k = (point1[1]-point2[1])/(point1[0]-point2[0])
    return k

#  自定义函数：用于选出最终的板子坐标范围
#  输入 1：正确灯条轮廓
#  返回值：板子区域坐标
def get_final_box(contours):
        mid_point_all = np.empty([0,2])
        final_box = np.empty([0,2])
        final_box1 = np.empty
        for i in range(len(contours)):
            #x, y, w, h = cv2.boundingRect(contours[i])
            #box = ([x,y],[x+w,y],[x+w,y+h],[x,y+h])
            box = cv2.minAreaRect(contours[i])
            print('所选最小矩形',box)
            box_point = cv2.boxPoints(box)
            box_point = np.int0(box_point)# 矩形的四个角点取整
            box_point = point_sort(box_point,box[0])
            #剔除负值
            print('可能四边形',box_point)
            get_mid_point1 = get_mid_point(box_point[0],box_point[1])
            get_mid_point2 = get_mid_point(box_point[2],box_point[3])
            k = cul_slope(get_mid_point1,get_mid_point2)
            print('斜率',k)
            if(angle_filter(k,5.6,-5.6)!=1):
                break
            mid_point_all = np.append(mid_point_all,get_mid_point1,axis=0)
            mid_point_all = np.append(mid_point_all,get_mid_point2,axis=0)
            mid_point_all = np.int0(mid_point_all)
            final_box = np.append(final_box,box_point,axis=0)
            final_box1 = np.split(final_box,len(final_box)/4)
            for i in range(len(final_box)):
                final_box[i] = np.int0(final_box[i])
            final_box1 = np.int0(final_box1)
            print('可能四边形合集',final_box)
        try:
            final_rect = cv2.minAreaRect(mid_point_all)
            final_rect = np.int0(cv2.boxPoints(final_rect))
            print('分割后',final_box1)
        except:
            final_rect = mid_point_all
            pass
        return final_box1,final_rect
