'''
Nicholas Wile, Gar Lock, Carter Mondy
CS 6027: Computer Networks
Adaptive UDP/TCP Video Streaming with CV
Spring 2024
'''

import cv2
import socket
import pickle
import struct

# Set up the sockets
server_ip = '0.0.0.0'  # Listen on all available interfaces
tcp_server_port = 8080
udp_server_port = 12000

# Create TCP socket
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind((server_ip, tcp_server_port))
tcp_server_socket.listen(10)
print(f"[TCP] Listening on {server_ip}:{tcp_server_port}")
conn, addr = tcp_server_socket.accept()
print(f"[TCP] Connection from {addr}")

# Create UDP socket
udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server_socket.bind((server_ip, udp_server_port))
print(f"[UDP] Listening on {server_ip}:{udp_server_port}")

# Create an OpenCV window to display the received frames
cv2.namedWindow("Server: received frames", cv2.WINDOW_NORMAL)

'''
Where the livestream will save 
As a video-on-demand
'''
vid_dir= "../test-vids/"

# Define the codec and create a VideoWriter object
fps = 20.0 # Through testing, this worked best for webcam
dim = (640, 480)
fourCC = cv2.VideoWriter_fourcc(*"XVID")
name = "livestream_receiver"
vid = cv2.VideoWriter(f"{vid_dir}{name}.avi", fourCC, fps, dim, isColor=True)

while True:
    # Receive frame size
    size_data = conn.recv(4)

    # TCP
    if size_data:
        frame_size = struct.unpack('!I', size_data)[0]

        # Receive frame data
        frame_data = b""
        while len(frame_data) < frame_size:
            chunk = conn.recv(frame_size - len(frame_data))
            if not chunk:
                break
            frame_data += chunk

    # UDP
    else:
        pass
        # Right now, UDP does not work
        # frame_data, _ = udp_server_socket.recvfrom(65536)
    
    # Decode and display the frame
    this_frame = pickle.loads(frame_data)

    # Save frame to video
    vid.write(this_frame)

    # Display livestream 
    cv2.imshow("Server: received frames", this_frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture
cv2.destroyAllWindows()
conn.close()
tcp_server_socket.close()
udp_server_socket.close()