import cv2
from PIL import ImageTk, Image, ImageDraw
from tkinter import *
import PIL
import numpy
import matplotlib as mp
import math
import os
import numpy as np
import glob
import mahotas
from sklearn.svm import SVC
from sklearn import svm
features=[]
labels=[]
with open("features_3.txt",encoding="utf-8") as fp:
    lines = fp.readlines()
    for line in lines:
        mylist = line.split(',')
        #if(mylist[0]==''):
         #   continue
        new_list=np.zeros(100)

        labels.append(str(mylist[0]))
        #print('Len of each feature',len(mylist[1:]))
        features.append(list(mylist[1:]))
        # print(labels)
#print('Length of the labels',len(labels),'=>',labels)
#print('Length of the feature',len(features),'=>',features)
labels=np.array(labels)
features=np.array(features)
clf=svm.SVC()
clf.fit(features,labels)
#clf.fit(labels)
#t=clf.predict([[5,5,4,15,13,13,12,11,10,10,1,1,8,7,6,6,6,5,2,1,1,18,16,16,16,15,16,16,16,17,17,18,18,1,1,2,3,4,5,5,7,8,8,9,9,1,1,11,11,12,12,12,13,13,12,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
width = 200
height =200
center = height//2
white = (255, 255, 255)
green = (0,128,0)
x=[]
y=[]
x_filter= []
y_filter= []
x_new = []
y_new = []
complex_new = []
if os.path.isfile("dataset_predict.txt"):
    os.remove("dataset_predict.txt")
if os.path.isfile("features_predict.txt"):
    os.remove("features_predict.txt")
def paint(event):
        thefile = open('dataset_predict.txt', 'a')
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        thefile.write((str(x1)+","+str(y1)+"\n"))
        thefile.close()
        x.append(x1)
        y.append(y1)
        
        print(x1,y1)
        #thefile.write((str(x1)+","+str(y1)+"\n"))
        filename = "3character_predict.jpeg"
        image1.save(filename)
        #thefile.write((str(x1)+","+str(y1)+"\n"))
        
        cv.create_oval(x1, y1, x2, y2, fill="black",width=2)
        draw.line([x1, y1, x2, y2],fill="black",width=2)
        #thefile.write((str(x1)+","+str(y1)+"\n"))

root = Tk()

cv = Canvas(root, width=width, height=height, bg='white')
cv.pack()
image1 = PIL.Image.new("RGB", (width, height), white)
draw = ImageDraw.Draw(image1)
cv.pack(expand=YES, fill=BOTH)
cv.bind("<B1-Motion>", paint)
root.mainloop()          # upto here program accepts input from user and prints coordinates as mouse is dragged

with open("dataset_predict.txt") as fp:
        line = fp.readline()
        mylist = line.split(',')
        x.append(int(mylist[0]))
        y.append(int(mylist[1]))
        #cnt = 1
        while line:
            line = fp.readline()
            mylist = line.split(',')
            #print("Line {}: {}".format(cnt, line.strip()))
            #print("Line {}: {}".format(cnt, mylist))
            if(mylist[0]==''):
                continue
            x.append(int(mylist[0]))
            y.append(int(mylist[1]))
            #cnt += 1
length=len(x)
window_size=5
num_of_features=round(length/window_size)
#print(length)
#print(num_of_features)
#file=open("features_predict.txt", "a+")
#file.write("[")
code_array=[]
for t in range (0,num_of_features):
            file=open("features_predict.txt", "a+")
            k=5*t
            m=k+5
            if(m>=length):
                break
            del_x=x[m]-x[k]
            del_y=y[m]-y[k]
            if ((del_x)==0):
                avg_slope="inf"
                avg_slope_copy="inf"
                code=300
            else:
                avg_slope=(del_y)/(del_x)
                avg_slope=math.atan(avg_slope)
                avg_slope=(avg_slope)*180/3.141594
                avg_slope_copy=avg_slope
                if(avg_slope<0):
                    avg_slope=abs(avg_slope)
                    if(del_y<0):
                        avg_slope=360-avg_slope
                    else:
                        avg_slope=180-avg_slope
                    
                else:
                    if(del_x<0 and del_y<0):
                        avg_slope=180+avg_slope
                code= math.floor(avg_slope/20)+1
                code_array.append(code)
                file.write(str(code)+",")
file.close()
code_array_size=len(code_array)
print(code_array_size)
req_zeros=100-code_array_size
file=open("features_predict.txt", "a")
for y in range(0,req_zeros):
            file.write("0,")
            code_array_size=code_array_size+1
file.close()
file=open("features_predict.txt", "rb+")
file.seek(-1, os.SEEK_END)
file.truncate()
file.close()
y_predict=[]
with open("features_predict.txt") as fp:
    lines = fp.read()
    mylist = lines.split(',')
    for i in range (0,len(mylist)):
        y_predict.append(int(mylist[i]))
features_predict=[]
features_predict=[y_predict]
print(features_predict)
t=clf.predict(features_predict)
print(t)
