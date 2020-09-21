import cv2
import numpy as np

#  自定义函数：根据输入矩形的长宽来矫正其角度θ
#  输入 1：最小矩形
#  返回值：校正后的角度θ
def angle_correction(min_box):
	#cv2最小矩形算法中，哪条边是width/height与这条边的长度无关。其width为：将x轴逆时针旋转，第一条与x轴平行的边为width
	#min_box[1][0]是width，min_box[1][1]是height，如果width>height，则其角度正确，如果width<heigit，则其width,heigit和角度错误，需要交换width,height高并取角度补角
	if min_box[1][0] < min_box[1][1]:
		#swap(min_box[1][0],min_box[1][1])#交换了width和height
		print(min_box[2])
		min_box[2] = 90 + min_box[2]#取角度补角
	return min_box[2]

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
		final_box = np.empty([0,2])
		final_box1 = np.empty
		for i in range(len(contours)):
			#x, y, w, h = cv2.boundingRect(contours[i])
			#box = ([x,y],[x+w,y],[x+w,y+h],[x,y+h])
			min_box = cv2.minAreaRect(contours[i])
			min_box_angle = angle_correction(min_box)#纠正该矩形的width,height，并矫正角度
			if (80 > min_box_angle) and (min_box_angle > 100):
				break#若该矩形的角度不在范围内，则跳出循环，不进行存储

			#以下代码将有效矩形进行存储
			print('所选最小矩形',min_box)
			min_box_point = cv2.boxPoints(min_box)#取最小矩形四点
			min_box_point = np.int0(min_box_point)# 矩形的四个角点取整
			final_box = np.append(final_box,min_box_point,axis = 0)
			final_box1 = np.split(final_box,len(final_box)/4)
			for i in range(len(final_box)):
				final_box[i] = np.int0(final_box[i])
			final_box1 = np.int0(final_box1)
			print('可能四边形合集',final_box)
		try:
			final_rect = cv2.minAreaRect(final_box)
			final_rect = np.int0(cv2.boxPoints(final_rect))
			print('分割后',final_box1)
		except:
			final_rect = final_box
			pass
		return final_box1,final_rect
