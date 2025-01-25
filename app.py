import streamlit as st
import cv2
import numpy as np
import av
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import tensorflow as tf
from detect import detect_frame, detect, notify, record
import multiprocessing
import json
import time 

st.title("Watcher of Weapons")

option = st.sidebar.selectbox(
    "Footage options",
    ("Upload file", "Webcam", "RTSP")
)


if option == "Upload file":
    uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "mpeg"])
    if uploaded_file:
        dic = {'detected': False,
           'confirmed': False}
        json_obj = json.dumps(dic, indent=4)
        with open('status.json', 'w') as f:
            f.write(json_obj)
        
        notify_q = multiprocessing.Queue()
        record_q = multiprocessing.Queue()
        
        notify_p = multiprocessing.Process(target=notify, args=(notify_q,))
        notify_p.start()
        
        record_p = multiprocessing.Process(target=record, args=(record_q,))
        record_p.start()
        
        detect(notify_q, record_q)
        
        notify_q.close()
        record_q.close()
        
        notify_q.join_thread()
        record_q.join_thread()
        
        notify_p.join()
        record_p.join()

if option == "Webcam":
    # webrtc_streamer(key="stream")
    img_file_buffer = st.camera_input("Camera feed")
    if img_file_buffer is not None:
        # To read image file buffer with OpenCV:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        dic = {'detected': False,
           'confirmed': False}
        json_obj = json.dumps(dic, indent=4)
        with open('status.json', 'w') as f:
            f.write(json_obj)
        
        notify_q = multiprocessing.Queue()
        record_q = multiprocessing.Queue()
        
        notify_p = multiprocessing.Process(target=notify, args=(notify_q,))
        notify_p.start()
        
        record_p = multiprocessing.Process(target=record, args=(record_q,))
        record_p.start()
        
        annotated_frame = detect_frame(cv2_img, notify_q, record_q)
        st.image(annotated_frame)
        
        notify_q.close()
        record_q.close()
        
        notify_q.join_thread()
        record_q.join_thread()
        
        notify_p.join()
        record_p.join()
        # Display the resized image
        
