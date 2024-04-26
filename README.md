# Computer Vision-Enabled Adaptive Video Streaming with Dual TCP-UDP
A prototype hybrid UDP/TCP video streaming application. We use the OpenCV computer vision library to calculate pixel difference between lecture video frames. We leverage this to identify key frames in a video stream and adapt the transport layer protocol accordingly for real-time video streaming. Keyframes will be sent with TCP and less important frames will be sent with UDP.

## Running the project
Create a virtual environment, activate it, and run the following command:
```
pip install -r requirements.txt
```

To start livestreaming, open two terminals. If your webcam is turned on, turn it off. In the first terminal, run the following command to start the server that receives video frames:
```
python receiver.py
```

Next, run the following command in the second terminal to start recording live from your webcam:
```
python sender.py
```

Each frame from the livestream will have its absolute pixel difference calculated and compared to the previous frame in the livestream. 

If the pixel difference is higher than a specified threshold, then we observe that significant changes have taken place from frame-to-frame and thus mark this as a keyframe and serve it using TCP.

## Other files
To test thresholding on a source video, change to the src directory and run the following:
```
python kf_detector_video.py
```

To test webcam functionality, run the following:
```
python kf_detector_webcam.py
```
