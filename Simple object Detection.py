import cv2 
import cvlib as cv
from cvlib.object_detection import draw_bbox


video = cv2.VideoCapture(0)
label = []
while True:
    ret, frame = video.read()
    bbox , label , conf = cv.detect_common_objects(frame)
    output_image =draw_bbox(frame,bbox , label , conf)
    
    print(bbox)

    cv2.imshow("Object Detection",output_image)
    if cv2.waitKey(1) & 0xFF == ord('q') :
        break

video.release()
cv2.destroyAllWindows()