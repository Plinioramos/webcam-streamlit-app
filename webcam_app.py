# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 15:10:25 2024

@author: plini
"""

import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("Webcam Live Feed")
st.subheader("Using WebRTC and Streamlit")

webrtc_streamer(key="example")
