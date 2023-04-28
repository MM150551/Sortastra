import cv2 as cv
import cvlib 
import time
from cvlib.object_detection import draw_bbox


cropSize = 10
#AOI = [240,320]
videoCapture = cv.VideoCapture(0)

idealColor = [150, 33, 25]
colorTol = 80
x = True

Rlist = []
Glist = []
Blist = [] 
index_list = []

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


video = cv.VideoCapture(0)
label = []
while True:

    ret, frame = video.read()
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

        #indicating if the average color in the cropped box is withing the idea/intended color range
        if(within_range(idealColor[0],RGBavgList[0],colorTol) and within_range(idealColor[1],RGBavgList[1],colorTol) and within_range(idealColor[2],RGBavgList[2],colorTol)):
            #print("the given object is within the color range")
            cv.rectangle(frame,(bbox[ind][0],bbox[ind][1]),(bbox[ind][2],bbox[ind][3]),[0,255,0],2)

        Rlist.clear()
        Glist.clear()
        Blist.clear()
        RGBavgList.clear()

        cv.imshow("Cropped_frame",Cropped_frame)
        #time.sleep(5)

        

    cv.imshow("Color detection",frame)

    
        

    #cv.imshow("Object Detection",output_image)
    if cv.waitKey(1) & 0xFF == ord('q') :
        break

video.release()
cv.destroyAllWindows()