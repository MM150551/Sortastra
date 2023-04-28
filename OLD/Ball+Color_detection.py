import cv2 as cv
import numpy as np
import time

cropSize = 40
#AOI = [240,320]
videoCapture = cv.VideoCapture(0)

idealColor = [150, 170, 160]
x = True

Rlist = []
Glist = []
Blist = []
colorTol = 50 

def list_avg(x):
     return int(sum(x)/(len(x)+1)) ##### +1 IS TEMPORARY 

def within_range(targetValue,givenvalue,tolerance):
    if(givenvalue <= targetValue +tolerance/2 and givenvalue >= targetValue - tolerance/2):
        return True
    else:
        return False
    

videoCapture = cv.VideoCapture(0)
prevCircles = None          # represent the circle from previous frame
dist = lambda x1,y1,x2,y2 : (x1-x2)**2 + (y1-y2)**2    
    # calculate the square of distance between 2 of the points in the frame
    # rather than returning square root which is the distance formula
    # I'm going to return the entire thing it self
while True :
    ret, frame = videoCapture.read()
    if not ret :
        break
    
    grayFrame = cv.cvtColor(frame , cv.COLOR_BGR2GRAY)  #convert color to gray
    blurFrame = cv.GaussianBlur(grayFrame , (17,17) , 0)    #to get rid of noise using GaussianBlur function
            
        # @ number 17 tells the size of mini window that is inspecting to figure out the blur
            #this number must be odd & if it is larger it will make it more blurred
        # @ 0 ==> sigmaX Gaussian kernel standard deviation in X direction.
    
    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1 , 20, 
                              param1=50, param2=30, minRadius=20, maxRadius=500)
    
        
        # @ HOUGH_GRADIENT ==> method Detection method,Finds circles in a grayscale image using the Hough transform 
            # it will return a list of the circles and stored in  circles
        # @ 0.5 == > dp Inverse ratio of the accumulator resolution to the image resolution
            # if it's larger then the circles we finds are closer to each other are going to be merged
            # a good value is between 1 & 1.5 
        # @ 1000 ==> minDist Minimum distance between the centers of the detected circle
            # 1000 ==> is very larg for only test
        # @ parame1 ==> sensitivity of circle detection 
            # if it's too high, it's not going to find enough circles
        # @ parame2 ==> accuracy of circle detection 
            # the way it works is it sets the number of edge points that are needed to declare that there is a circle
            # 25 ==> there a minimum of 25 edge points to declare that a circle is present
            # if it's too high, it's not going to find enough circles
        # @ minRadius ==> Minimum circle radius that can be detected
            # 75 ==> circles are far from camera
        # @ maxRadius ==> Maximum circle radius that can be detected
            # 500 ==> circles are very close camera

    if circles is not None :        # do we have circles
        circles = np.uint16(np.around(circles))     #convert it to numpy array
        chosen = None

        #print(circles)

        for i in circles[0 , :] :

            #Center Dot
            cv.circle(frame, (i[0], i[1]), 1, (0,100,100), 3)
            cropSize = i[2]
            #Outer circle
            #cv.circle(frame, (i[0], i[1]), i[2], (255,0,255), 3)

            AOI = [i[0],i[1]]
            ULcorner = [max(1,int(AOI[0]-(cropSize/2))),max(1,int(AOI[1]-(cropSize/2)))]
            Cropped_frame = frame[ULcorner[0]:max(1,(ULcorner[0]+cropSize)),ULcorner[1]:max(1,(ULcorner[1]+cropSize))]

            
            for color in Cropped_frame:
        
                for Color in color:
                
                    #print(Color)
                    Rlist.append(Color[2])
                    Glist.append(Color[1])
                    Blist.append(Color[0])

            RGBavgList = [list_avg(Rlist),list_avg(Glist),list_avg(Blist)]
            #print(RGBavgList)

            cv.putText(frame,str(RGBavgList),(i[0], i[1]),fontFace=cv.FONT_HERSHEY_SIMPLEX,fontScale=0.4,color=(0,255,0),thickness=2)

            if(within_range(idealColor[0],RGBavgList[0],colorTol) and within_range(idealColor[1],RGBavgList[1],colorTol) and within_range(idealColor[2],RGBavgList[2],colorTol)):
                #print("the given object is within the color range")
                cv.circle(frame, (i[0], i[1]), i[2], (255,0,255), 2)

            #cv.imshow("cropped", Cropped_frame)
            #cv.imshow("original", frame)
        

            #zeroing lists
            Rlist.clear()
            Glist.clear()
            Blist.clear()
            RGBavgList.clear()
            #cv.destroyWindow("cropped")
        time.sleep(0.2)




    cv.imshow("circles", frame)      # name of window

    if cv.waitKey(1) & 0xFF == ord('q') :       # stop video if I click on q
        break

videoCapture.release()
cv.destroyAllWindows()