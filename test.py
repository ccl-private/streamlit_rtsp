import streamlit as st
from st_rtsp_main import RTSPVideoStream

def main():

    st.title("实时视频流")
    rtsp_url = "rtsp://127.0.0.1:8554/123"
    video_stream = RTSPVideoStream(rtsp_url)
    video_stream.start_stream()


if __name__ == "__main__":
    main()
