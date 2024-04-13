'''
Nicholas Wile, Gar Lock, Carter Mondy
CS 6027: Computer Networks
Adaptive UDP/TCP Video Streaming with CV
Spring 2024
'''

import cv2
import matplotlib.pyplot as plt
import numpy as np

fps = 30.0
threshold = 2000000

# Read the input video
vid_dir= "test-vids/"
fig_dir = "figures/"
vid_names = ["lecture0", "lecture1"]

for vid_name in vid_names:
    in_vid_path = f"{vid_dir}{vid_name}.mp4"
    cap = cv2.VideoCapture(in_vid_path)

    # Initialize variables
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    keyframe_indices = []
    pixel_values = []

    # Outputs a video that labels keyframes
    out_vid_path = vid_dir + f"{vid_name}_labeled.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(out_vid_path, fourcc, fps, (width, height))

    # Iterate thru each vid frame and detect key frame
    for i in range(frame_count):
        if i == 4000:
            frame_count = 4000
            # Don't go beyond 4K frames, b/c I don't feel like waiting
            break

        ret, this_frame = cap.read()
        if not ret:
            break
        
        # Label first frame as key frame
        if i == 0:
            keyframe_indices.append(i)
            pixel_values.append(0)
            prev_frame = this_frame.copy()
            cv2.putText(this_frame, f"Frame {i}: Keyframe (TCP)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Pixel difference 
        if i > 0:
            diff = cv2.absdiff(prev_frame, this_frame)
            diff_sum = np.sum(diff)
            pixel_values.append(diff_sum)
            prev_frame = this_frame.copy()

            '''
            Compare pixel diff to threshold
            If diff exceeds threshold, more changes
            So this gets labeled as a keyframe
            '''
            if diff_sum > threshold:
                keyframe_indices.append(i)
                cv2.putText(this_frame, f"Frame {i}: Keyframe (TCP)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(this_frame, f"Pixel Diff: {diff_sum}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            else:
                cv2.putText(this_frame, f"Frame {i}: Not Key (UDP)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(this_frame, f"Pixel Diff: {diff_sum}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        video.write(this_frame)

    cap.release()
    video.release()

    # Plot distribution of pixel diff across video frames
    fig, ax = plt.subplots()
    ax.plot(np.linspace(0, frame_count, frame_count), pixel_values, linewidth=1.0)
    plt.ylim(0,threshold*5)
    plt.axhline(threshold, color = 'r', linestyle = '-') 
    plt.title(f"Pixel Difference Distribution: {vid_name}\n({len(keyframe_indices)} keyframes)")
    plt.xlabel("Video Frame")
    plt.ylabel("Pixel Difference")
    plt.savefig(f"{fig_dir}{vid_name}.png")
    plt.show()

    print(f"Detected {len(keyframe_indices)} keyframes out of {frame_count} total video frames.")
    print(f"Output video saved as {out_vid_path}")