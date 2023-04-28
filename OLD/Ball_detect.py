import cv2 as cv
import numpy as np
#import Color_detection as CD

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
                              param1=100, param2=30, minRadius=0, maxRadius=500)
    
        
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
        for i in circles[0 , :] :
            if chosen is None :     chosen = i          #first case of comparison
            if prevCircles is not None :
                if dist(chosen[0], chosen[1], prevCircles[0], prevCircles[1]) <= dist(i[0], i[1], prevCircles[0], prevCircles[1]) :
                    chosen = i
        
            #Center Dot
            cv.circle(frame, (i[0], i[1]), 1, (0,100,100), 3)

            #Outer circle
            cv.circle(frame, (i[0], i[1]), i[2], (255,0,255), 3)
            prevCircles = chosen

    cv.imshow("circles", frame)      # name of window

    if cv.waitKey(1) & 0xFF == ord('q') :       # stop video if I click on q
        break

videoCapture.release()
cv.destroyAllWindows()