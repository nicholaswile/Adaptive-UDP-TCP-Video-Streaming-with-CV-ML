# Adaptive-UDP-TCP-Video-Streaming-with-CV-ML
A prototype hybrid UDP/TCP video streaming application. We use the OpenCV computer vision library to calculate pixel difference between lecture video frames. We leverage this to identify key frames in a video stream and adapt the transport layer protocol accordingly for real-time video streaming. Keyframes will be sent with TCP and less important frames will be sent with UDP.

Create a virtual environment, activate it, and run the following command:
```
pip install -r requirements.txt
```

Then run the command:
```
python keyframe_detect.py
```