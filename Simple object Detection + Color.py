import cv2 as cv
import cvlib 
import time
from cvlib.object_detection import draw_bbox
import numpy as np

cropSize = 10
#AOI = [240,320]
videoCapture = cv.VideoCapture(0)

numRowColumn = [4,3]

idealColor = [160, 147, 35]
colorTol = 80
x = True

Rlist = []
Glist = []
Blist = [] 
index_list = []

socketNumbers = set()

def list_avg(x):
    try:
        return int(sum(x)/(len(x))) ##### +1 IS TEMPORARY 
    except:
        return 0

def within_range(targetValue,givenvalue,tolerance):
    if(givenvalue <= targetValue +tolerance/2 and givenvalue >= targetValue - tolerance/2):
        return True
    else:
        return False

def within_two_values(startValue,endValue,givenvalue):
    if(startValue <= givenvalue and givenvalue < endValue):
        return True
    else:
        return False

def divide_into_equal_values(total,numOfValues):
    segment = total//numOfValues
    segmentedValues = []
    segmentedValues.clear()
    for i in range(numOfValues+1):
        segmentedValues.append(i*segment)
    return segmentedValues

video = cv.VideoCapture(0)
label = []
while True:

    ret, frame = video.read()

    dimensions = list(np.shape(frame))
    
    #divide the screen into segments indicating socket location
    yValues = divide_into_equal_values(dimensions[0],numRowColumn[0])
    xValues = divide_into_equal_values(dimensions[1],numRowColumn[1])

    
    for i in yValues:
        cv.line(frame,(0,i),(dimensions[1],i),(0,0,255),1)
    for i in xValues:
        cv.line(frame,(i,0),(i,dimensions[0]),(0,0,255),1)

    #print(xValues , yValues)

    bbox , label , conf = cvlib.detect_common_objects(frame)
    #output_image =draw_bbox(frame,bbox , label , conf)
    
    #print(bbox)
    #print(label)

    index = 0
    index_list.clear()


    for L in label:
        if L == "orange" or L == "sports ball" or L == "apple":
            index_list.append(index)
        index = index + 1
    
    for ind in index_list:

        Cropped_frame = frame[max(2,bbox[ind][1]+cropSize):max(2,bbox[ind][3]-cropSize),max(2,bbox[ind][0]+cropSize):max(2,bbox[ind][2]-cropSize)]


        #extracting color from each pixel in the cropped frame
        for color in Cropped_frame:
        
                for Color in color:
                
                    #print(Color)
                    Rlist.append(Color[2])
                    Glist.append(Color[1])
                    Blist.append(Color[0])

        #getting average color of the cropped box
        RGBavgList = [list_avg(Rlist),list_avg(Glist),list_avg(Blist)]

        #print(RGBavgList)

        #printing text indicating the average color of the cropped box on its upper left corner
        cv.putText(frame,str(RGBavgList),(bbox[ind][0], bbox[ind][1]),fontFace=cv.FONT_HERSHEY_SIMPLEX,fontScale=0.4,color=(0,255,0),thickness=2)


        ####################
        middlePoint = (int((bbox[ind][0]+bbox[ind][2])/2),int((bbox[ind][1]+bbox[ind][3])/2))

        #indicating if the average color in the cropped box is withing the ideal/intended color range
        if(within_range(idealColor[0],RGBavgList[0],colorTol) and within_range(idealColor[1],RGBavgList[1],colorTol) and within_range(idealColor[2],RGBavgList[2],colorTol)):
            #print("the given object is within the color range")
            cv.rectangle(frame,(bbox[ind][0],bbox[ind][1]),(bbox[ind][2],bbox[ind][3]),[0,255,0],2)

            socketNum = 0
            counter = 0
            #print(middlePoint[1])
            
            segmentx = dimensions[1]/numRowColumn[1]
            segmenty = dimensions[0]/numRowColumn[0]
            br = False

            #adds the socket number to the set NOTE: pressing r will reset the set
            for x in xValues:
                for y in yValues:
                    counter = counter + 1
                    if (within_two_values(y,y+segmenty,middlePoint[1]) and within_two_values(x,x+segmentx,middlePoint[0])):
                        #print(counter)
                        socketNumbers.add(counter)
                        br =True
                        break
                if(br):
                    break
                counter = counter - 1

        Rlist.clear()
        Glist.clear()
        Blist.clear()
        RGBavgList.clear()

        #cv.imshow("Cropped_frame",Cropped_frame)
        #time.sleep(5)

        

        #print(middlePoint)
        cv.circle(frame, middlePoint, 1, (0,0,255), 4)
        
        

    if cv.waitKey(1) & 0xFF == ord('r') :
        socketNumbers.clear()


    cv.imshow("Color detection",frame)
    #cv.imshow("Object Detection",output_image)
    if cv.waitKey(1) & 0xFF == ord('q') :
        break


print(socketNumbers)

video.release()
cv.destroyAllWindows()