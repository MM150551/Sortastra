import cv2 as cv
import numpy as np

'''
Notes to self:

frame shape is (480, 640, 3)

'''
cropSize = 40
ULcorner = [int(240-(cropSize/2)),int(320-(cropSize/2))]
videoCapture = cv.VideoCapture(0)

idealColor = [5, 25, 132]
x = True

Rlist = []
Glist = []
Blist = []
colorTol = 50 

def list_avg(x):
     return int(sum(x)/len(x))

def within_range(intendedValue,givenvalue,tolerance):
    if(givenvalue <= intendedValue +tolerance/2 and givenvalue >= intendedValue - tolerance/2):
        return True
    else:
        return False
        



while(1):
    ret, frame = videoCapture.read()
    if not ret :
        break

    frameArray = np.uint16(frame)
    #print(frameArray)

    #print(frame)
    dimensions = np.shape(frame)
    #print(dimensions)

    Cropped_frame = frame[ULcorner[0]:(ULcorner[0]+cropSize),ULcorner[1]:(ULcorner[1]+cropSize)]

    

    for color in Cropped_frame:
        
        for Color in color:
                
            #print(Color)
            Rlist.append(Color[2])
            Glist.append(Color[1])
            Blist.append(Color[0])
    RGBavgList = [list_avg(Rlist),list_avg(Glist),list_avg(Blist)]
    print(RGBavgList)
    
    if(within_range(idealColor[0],RGBavgList[0],colorTol) and within_range(idealColor[1],RGBavgList[1],colorTol) and within_range(idealColor[2],RGBavgList[2],colorTol)):
        print("the given onbject is within the color range")

    cv.imshow("cropped", Cropped_frame)
    cv.imshow("original", frame)

    #zeroing lists
    Rlist.clear()
    Glist.clear()
    Blist.clear()
    RGBavgList.clear()

    if cv.waitKey(1) & 0xFF == ord('q') :       
        break