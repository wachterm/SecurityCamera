# import the opencv library 
import cv2
import time
import numpy

# In the debug mode:
# - green bounding boxes are drawn around the areas where motion was detected
# - no files are stored when motion was detected
# - no timelapse will be applied, so that images are taken as fast as possible
debug_mode = False
# Prints also date and time into the image
print_date = True

def writelog(logtext):
    now = time.time() # get snapshot of current time
    lt = time.localtime(now) # conraspberry vert to local time struct
    seconds = now - now // 1 # get remainder of the seconds
    logfile = open("/home/pi/SecurityCam/logfile.txt", "a+")
    logfile.write(time.strftime("%Y-%m-%d-%H-%M-%S", lt) + str(seconds)[1:5] + ": " + logtext + "\n")
    logfile.close()

writelog("Program started")

# Timelapse value in seconds. Images are taken only in this interval.
timelapse = 0.5 # seconds minimally from one image to the next one
# Threshold value for motion detection. Detection only when this size of pixels area change
threshold_motion = 0.001 # factor of whole image area (300 pixels std, 2000 HD)
  
# initialize the baseline image for motion detection  
baseline_image = None
# define a video capture object 
vid = cv2.VideoCapture(0) 
# The following resolutions are tested with the original pi cam:
# 640x480 (standard)
# 1920x1088 (like hd)
# Teh following resolutions are officially supported by the ELP camera of the smart systems lab:
#2592 (H) x 1944 (V) Pixel MJPEG 15 fps YUY2 3 fps
#2048 (H) x 1536 (V) Pixel MJPEG 15PS YUY2 3 fps
#1600 (H) x 1200 (V) Pixel MJPEG 15 fps YUY2 3 fps
#1920 (H) x 1080 (V) Pixel MJPEG 15 fps YUY2 3 fps
#1280 (H) x 1024 (V) Pixel MJPEG 15 fps YUY2 7.5 FPS
#1280 (H) x 720 (V) Pixeln MJPEG 30 fps YUY2 7.5 FPS
#1024 (H) x 768 (V) Pixeln MJPEG 30 fps YUY2 15 fps
#800 (H) x 600 (V) Pixeln MJPEG 30 fps YUY2 30 fps
#640 (H) x 480 (V) Pixel MJPEG 30 fps YUY2 30 fps
vid.set(3, 1920)  # Set horizontal resolution max 3280 hd 1920
vid.set(4, 1088)  # Set vertical resolution max 2464 hd 1080

starttime = time.time()
writelog("Init done")

# Sleeps so that the timelapse period is fulfilled
def wait():
    global starttime, timelapse, vid
    currenttime = time.time()
    looptime = currenttime - starttime
    difftime = timelapse - looptime
    while (time.time() - currenttime < difftime):
        ret, frame = vid.read()
    starttime = time.time()

imagenumber = 1
# Main loop for image processing
while(True): 
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read()
    image_width = numpy.shape(frame)[0]
    image_height = numpy.shape(frame)[1]
    if (debug_mode):
        print("image " + str(imagenumber))
    imagenumber = imagenumber + 1

    # Make gray and blurred frame
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)
  
    # Store it first time as baseline image
    if baseline_image is None:
        baseline_image = gray_frame
        wait()
        continue

    # Find difference between new and base image
    delta = cv2.absdiff(baseline_image,gray_frame)
    # Apply a threshold in order not to take each minimum change
    threshold = cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    # Detect objects inside the threshold area
    (contours,_) = cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Decide which contours based on the size will be taken into account
    motion_detected = False
    for contour in contours:
        threshold_area = threshold_motion*image_width*image_height
        if cv2.contourArea(contour) < threshold_area: # This value decides how huge a changed area must be to be detected
            continue
        # Motion detected
        motion_detected = True
        if (debug_mode):
            # Draw a rectangle around the identified contour
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)

    # Writes date and time into the image
    if(print_date):
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (int(image_width/72.5), int(image_width/27.2))
        fontScale              = 0.328+image_width*image_height/1781760#std 0.5, HD 1.5
        fontColor              = (255,255,255)
        lineType               = int(1.483+image_width*image_height/593920)#std 2, HD 5
        now = time.time() # get snapshot of current time
        lt = time.localtime(now) # convert to local time struct
        seconds = now - now // 1 # get remainder of the seconds
        cv2.putText(frame, time.strftime("%Y-%m-%d %H:%M:%S", lt) + str(seconds)[1:5], 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)        

    # Debug image windows
    #cv2.imshow("gray_frame Frame",gray_frame)
    #cv2.imshow("Delta Frame",delta)
    #cv2.imshow("Threshold Frame",threshold)
    # Display the resulting frame 
    if (debug_mode):
        cv2.imshow('frame', frame) 
      
    # Save image if motion detected
    if (motion_detected):
        writelog("Motion detected")
        # work out the timestamp part of the filename
        now = time.time() # get snapshot of current time
        lt = time.localtime(now) # convert to local time struct
        seconds = now - now // 1 # get remainder of the seconds
        #filename = "image-" + str(lt[0]) + "-" + str(lt[1]) + "-" + str(lt[2]) + "-" \
        #                   + str(lt[3]) + "-" + str(lt[4]) + "-" + str(lt[5]) + ".jpg"
        filename = "/home/pi/SecurityCam/images/image-" + time.strftime("%Y-%m-%d-%H-%M-%S", lt) + str(seconds)[1:5] + ".jpg"
        cv2.imwrite(filename, frame)

    baseline_image = gray_frame

    # Wait until timelapse time is completed
    wait()

    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows()
