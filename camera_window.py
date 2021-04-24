# Simple camera viewer with open cv
# Press the 'q' button to close the windows and the program
# import the opencv library 
import cv2

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
vid.set(3, 1024)  # Set horizontal resolution max 3280 hd 1920
vid.set(4, 768)  # Set vertical resolution max 2464 hd 1080

try:
    # Main loop for image processing
    while(True): 
        # Capture the video frame 
        ret, frame = vid.read()
        if (ret):
            cv2.imshow('frame', frame) 
        # Close the window with the the 'q' button
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
finally:
    print("Cleaning up")
    # After the loop release the cap object 
    vid.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows()
