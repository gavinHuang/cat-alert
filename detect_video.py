import argparse
import cv2
from YoloObjectDetector import YoloObjectDetector
from datetime import datetime

parser = argparse.ArgumentParser(description="Detect Objects in a Video.")
parser.add_argument("-s", "--size", dest="size", default="320", type=str, help="Spatial Size (tiny, 320, 416, 608), default: 320")
parser.add_argument("-i", "--input", dest="input", type=int, help="Input file (optional). If not set, Webcam will be used.")
parser.add_argument("-d", "--display", dest="display", default="true", type=str, help="Wether to show image/video window")
parser.add_argument("-w", "--wait", dest="wait_time", default="0.2",type=float, help="sleep time to capture pic")
args = parser.parse_args()
modelSize = args.size
print("Using size " + modelSize)
print("wait time "+ str(args.wait_time))
print("args.input " + str(args.input))
print("args.display " + str(args.display))

def get_video():
    if args.input is None:
        #works for pc
        cap = cv2.VideoCapture(0)
        #works for pi
        # cap = cv2.VideoCapture(-1,2)
        # cap.open(-1)
    else:
        cap = cv2.VideoCapture(args.input)
    return cap

def video_process(cap):
    while cap.isOpened():
        ret, frame = cap.read()
        if frame is None:
            break

        t1 = datetime.now()
        class_ids = detector.processImage(frame)
        print("detected objects:"+str(class_ids))
        print("time taken:"+str(datetime.now()-t1))
        
        if args.display.lower() == "true": 
            cv2.imshow("Frame", frame)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
        #cat detected
        if class_ids and 15 in class_ids:
            #todo: send alert
            print("cat detected!")
        
try:
    detector = YoloObjectDetector(modelSize)
    cap = get_video()
    video_process(cap)
    if args.display.lower() == "true": 
        cv2.waitKey(5000)
except KeyboardInterrupt as e:
    print(e)
finally:
    cap.release()
    cv2.destroyAllWindows()

