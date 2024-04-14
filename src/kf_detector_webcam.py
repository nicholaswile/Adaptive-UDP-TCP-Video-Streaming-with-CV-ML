'''
Adapted from OpenCV
https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
'''
import numpy as np
import cv2 as cv
 
cap = cv.VideoCapture(0)

vid_dir= "../test-vids/"

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter(f"{vid_dir}webcam.avi", fourcc, 20.0, (640, 480))

if not cap.isOpened():
    print("Cannot open camera")
    exit()

frame_count = 0
keyframe_indices = []
pixel_values = []
threshold = 3000000

while True:
    # Capture frame-by-frame
    ret, this_frame = cap.read()
    
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    if (frame_count == 0):
        keyframe_indices.append(frame_count)
        pixel_values.append(0)
        prev_frame = this_frame.copy()
        cv.putText(this_frame, f"Frame {frame_count}: Keyframe (TCP)", (20, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    elif (frame_count > 0):
        diff = cv.absdiff(prev_frame, this_frame)
        diff_sum = np.sum(diff)
        pixel_values.append(diff_sum)
        prev_frame = this_frame.copy()

        # Removes faulty frames
        if (diff_sum == 0):
            continue

        if diff_sum > threshold:
            keyframe_indices.append(frame_count)
            cv.putText(this_frame, f"Frame {frame_count}: Keyframe (TCP)", (20, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(this_frame, f"Pixel Diff: {diff_sum}", (20, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        else:
            cv.putText(this_frame, f"Frame {frame_count}: Not Key (UDP)", (20, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv.putText(this_frame, f"Pixel Diff: {diff_sum}", (20, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
    # write the frame
    out.write(this_frame)
 
    # Display the resulting frame
    cv.imshow('frame', this_frame)

    frame_count += 1
    
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
out.release()
cv.destroyAllWindows()