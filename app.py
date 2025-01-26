import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
import json
import av
import utils as utils
from detect import detect_frame
from streamlit_webrtc import webrtc_streamer

if 'model' not in st.session_state:
    print("loading model...")
    st.session_state['model'] = tf.saved_model.load('detectionmodel')
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
    frame = frame.to_ndarray()
    
    print("detecting frame...")
            
    image_data = cv2.resize(frame, (608, 608))
    image_data = image_data / 255.
    image_data = image_data[np.newaxis, ...].astype(np.float32)

    infer_weapon = st.session_state['model'].signatures['serving_default']

    batch_data = tf.constant(image_data)
    pred_bbox = infer_weapon(batch_data)

    for key, value in pred_bbox.items():
        boxes = value[:, :, 0:4]
        pred_conf = value[:, :, 4:]

    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        scores=tf.reshape(
            pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        max_output_size_per_class=50,
        max_total_size=50,
        iou_threshold=0.5,
        score_threshold=0.3
    )
    valid_detections = valid_detections.numpy()[0]
        
    if valid_detections:
        original_h, original_w, _ = frame.shape
        bboxes = utils.format_boxes(boxes.numpy()[0][:valid_detections], original_h, original_w)

        # notify_q.put(bboxes)
        
        pred_bbox = [bboxes, scores.numpy()[0], classes.numpy()[0], valid_detections]
        
        frame = utils.draw_bbox(frame, pred_bbox, info=True)    
         
    return av.VideoFrame.from_ndarray(frame) 
                
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