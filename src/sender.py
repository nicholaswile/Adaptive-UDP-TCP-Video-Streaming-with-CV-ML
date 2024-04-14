import cv2
import socket
import pickle
import struct
import numpy as np
from matplotlib import pyplot as plt

# Set up sockets
server_ip = "127.0.0.1"
tcp_server_port = 8080
udp_server_port = 12000

# Open the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Create TCP socket and try to connect to the server
tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    tcp_client_socket.connect((server_ip, tcp_server_port))
    print(f"[TCP] Connected to {server_ip}:{tcp_server_port}")
except ConnectionRefusedError:
    print(f"[TCP] Connection to {server_ip}:{tcp_server_port} failed. Make sure the server is running.")
    exit(1)

# Create UDP socket
udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize variables
frame_count = 0
keyframe_indices = []
pixel_values = []
threshold = 5000000

'''
Where the livestream will save as a video-on-demand 
The sender saves debug frames which display pixel diff and keyframe classification
'''
vid_dir= "../test-vids/"
fig_dir = "../figures/"

# Define the codec and create a VideoWriter object
fps = 20.0 # Through testing, this worked best for webcam
dim = (640, 480)
fourCC = cv2.VideoWriter_fourcc(*"XVID")
name = "webcam_sender"
vid = cv2.VideoWriter(f"{vid_dir}{name}.avi", fourCC, fps, dim, isColor=True)

while True:
    # Capture webcame livestream frame by frame
    ret, this_frame = cap.read()

    # Used for displaying keyframe status and pixel diff on sender side
    debug_frame = this_frame.copy()

    # Ret is true when frame is read correctly
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    '''
    Domain knowkedge: the first frame in a stream has no pixel diff
    But still want to make a keyframe, first frame can be an important feature
    So we skip thresholding for the first frame
    '''
    isKey = False
    if (frame_count == 0):
        keyframe_indices.append(frame_count)
        pixel_values.append(0)
        prev_frame = this_frame.copy()
        cv2.putText(debug_frame, f"Frame {frame_count}: Keyframe (TCP)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    elif (frame_count > 0):
        diff = cv2.absdiff(prev_frame, this_frame)
        diff_sum = np.sum(diff)
        pixel_values.append(diff_sum)
        prev_frame = this_frame.copy()

        # Removes faulty frames read from webcam
        if (diff_sum == 0):
            frame_count += 1
            continue

        if diff_sum > threshold:
            keyframe_indices.append(frame_count)
            cv2.putText(debug_frame, f"Frame {frame_count}: Keyframe (TCP)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(debug_frame, f"Pixel Diff: {diff_sum}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            isKey = True
        else:
            cv2.putText(debug_frame, f"Frame {frame_count}: Not Key (UDP)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(debug_frame, f"Pixel Diff: {diff_sum}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Save frame to video
    vid.write(debug_frame)

    # Below is for saving frames as images, used for debugging.
    # cv2.imwrite(f"{fig_dir}{frame_count}.png", debug_frame)
    
    # Display the resulting sender's frame
    cv2.imshow("Client: sent frame", debug_frame)

    frame_count += 1
    
    if cv2.waitKey(1) == ord('q'):
        break

    # Encode the frame
    data = pickle.dumps(this_frame)
    size = struct.pack('!I', len(data))

    try:
        # Send important keyframes through TCP to prevent data loss
        # For the rest, send through UDP 
        if isKey:
            tcp_client_socket.sendall(size + data)

        # Right now, UDP does not work
        else:
            # udp_client_socket.sendto(data, (server_ip, udp_server_port))
            tcp_client_socket.sendall(size + data)
            
    except socket.error:
        continue

# Release the capture and sockets when program is done
cap.release()
tcp_client_socket.close()
udp_client_socket.close()
cv2.destroyAllWindows()

# Plot distribution of pixel diff across video frames
fig, ax = plt.subplots()
ax.plot(np.linspace(0, frame_count, frame_count), pixel_values, linewidth=1.0)
plt.ylim(0,threshold*3)
plt.axhline(threshold, color = 'r', linestyle = '-') 
plt.title(f"Pixel Difference Distribution\n({len(keyframe_indices)} keyframes)")
plt.xlabel("Video Frame")
plt.ylabel("Pixel Difference")

name = "webcam_histogram.png"
plt.savefig(f"{fig_dir}{name}")
plt.show()

print(f"Detected {len(keyframe_indices)} keyframes out of {frame_count} total frames from the livestream.")