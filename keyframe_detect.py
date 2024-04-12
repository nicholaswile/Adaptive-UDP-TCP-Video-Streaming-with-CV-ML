'''
Nicholas Wile, Gar Lock, Carter Mondy
CS 6027: Computer Networks
Adaptive UDP/TCP Video Streaming with CV
Spring 2024
'''

import cv2
import numpy as np

# Read the input video
vid_dir= "test-vids/"
vid_names = ["lecture0", ]
in_vid_path = f"{vid_dir}{vid_names[0]}.mp4"
cap = cv2.VideoCapture(in_vid_path)

# Initialize variables
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
threshold = 2000000
keyframe_indices = []

# Outputs a video that labels keyframes
out_vid_path = vid_dir + f"{vid_names[0]}_labeled.mp4"
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video = cv2.VideoWriter(out_vid_path, fourcc, 30.0, (width, height))

max = 0

# Iterate thru each vid frame and detect key frame
for i in range(frame_count):
    ret, this_frame = cap.read()
    if not ret:
        break
    
    if i == 0:
        keyframe_indices.append(i)
        cv2.putText(this_frame, f"Frame {i}: Keyframe (TCP)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Pixel difference 
    if i > 0:
        diff = cv2.absdiff(prev_frame, this_frame)
        diff_sum = np.sum(diff)
        if (diff_sum > max):
            print(diff_sum)
            max = diff_sum
        '''
        Compare pixel diff to threshold
        If diff exceeds threshold, more changes
        So this gets labeled as a keyframe
        '''
        if diff_sum > threshold:
            keyframe_indices.append(i)
            cv2.putText(this_frame, f"Frame {i}: Keyframe (TCP)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(this_frame, f"Frame {i}: Not Key (UDP)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    prev_frame = this_frame.copy()
    video.write(this_frame)

cap.release()
video.release()

print(f"Detected {len(keyframe_indices)} keyframes out of {frame_count} total video frames.")
print(f"Output video saved as {out_vid_path}")