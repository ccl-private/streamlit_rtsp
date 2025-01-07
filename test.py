import streamlit as st
from st_rtsp_main import RTSPVideoStream

def main():

    st.title("实时视频流")
    rtsp_url = "rtsp://admin:zxkj@123@192.168.2.13:554/cam/realmonitor?channel=1&subtype=0"
    video_stream = RTSPVideoStream(rtsp_url)
    video_stream.start_stream()


if __name__ == "__main__":
    main()