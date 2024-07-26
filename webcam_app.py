import av
import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, VideoProcessorBase
from pathlib import Path

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.recording = False
        self.frames = []
        self.out = None
        self.video_path = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        if self.recording:
            self.frames.append(img)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

    def start_recording(self):
        self.recording = True
        self.frames = []

    def stop_recording(self):
        self.recording = False
        if len(self.frames) > 0:
            height, width, _ = self.frames[0].shape
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            self.video_path = Path("output.avi")
            self.out = cv2.VideoWriter(str(self.video_path), fourcc, 20.0, (width, height))

            for frame in self.frames:
                self.out.write(frame)

            self.out.release()

st.title("Webcam Live Feed with Recording")
st.subheader("Using WebRTC and Streamlit")

webrtc_ctx = webrtc_streamer(
    key="example",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

if webrtc_ctx.video_processor:
    if st.button("Start Recording"):
        webrtc_ctx.video_processor.start_recording()

    if st.button("Stop Recording"):
        webrtc_ctx.video_processor.stop_recording()
        st.success("Recording saved to output.avi")

        if webrtc_ctx.video_processor.video_path:
            with open(webrtc_ctx.video_processor.video_path, "rb") as video_file:
                btn = st.download_button(
                    label="Download Video",
                    data=video_file,
                    file_name="output.avi",
                    mime="video/x-msvideo"
                )


