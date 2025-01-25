import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
import json
import av
from detect import detect_frame
from streamlit_webrtc import webrtc_streamer

if 'model' not in st.session_state:
    print("loading model...")
    st.session_state.model = tf.saved_model.load('detectionmodel')
    print("model loaded")

st.title("Watcher of Weapons")

option = st.sidebar.selectbox(
    "Footage options",
    ("Webcam", "Upload file", "RTSP")
)

# if 'notify_q' not in st.session_state:
#     st.session_state['notify_q'] = multiprocessing.Queue()
# if 'record_q' not in st.session_state:
#     st.session_state['record_q'] = multiprocessing.Queue()
# if 'notify_p' not in st.session_state:
#     st.session_state['notify_p'] = multiprocessing.Process(target=notify, args=(st.write(st.session_state.notify_q),))
# if 'record_p' not in st.session_state:
#     st.session_state['record_p'] = multiprocessing.Process(target=record, args=(st.write(st.session_state.notify_q),))    
# if 'started' not in st.session_state:
#     st.session_state['started'] = False
    
# if not st.session_state['started']:  
#     st.write(st.session_state.notify_p).start()
#     st.write(st.session_state.record_p).start()
#     st.session_state['started'] = True

if option == "Upload file":
    uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "mpeg"])
    if uploaded_file:
        pass
            
def video_frame_callback(frame):
    print("callback")
    img = frame.to_ndarray()
    img = detect_frame(st.session_state.model, img)
     
    return av.VideoFrame.from_ndarray(img) 
                
if option == "Webcam":
    webrtc_streamer(key="sample", video_frame_callback=video_frame_callback)
        
if __name__ == "__main__":    
    dic = {'detected': False,
           'confirmed': False}
    json_obj = json.dumps(dic, indent=4)
    with open('status.json', 'w') as f:
        f.write(json_obj)
        
    # notify_q.close()
    # record_q.close()
    
    # notify_q.join_thread()
    # record_q.join_thread()
    
    # notify_p.join()
    # record_p.join()