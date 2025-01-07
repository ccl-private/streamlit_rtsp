# streamlit_rtsp
show rtsp stream in streamlit web via ffmpeg, You can set the hardware acceleration manually set it in the code.

## **1. Dependent Environment**
sudo apt install ffmpeg

pip3 install streamlit opencv-python

## **2. Change ffmpeg Configuration**


To change the FFmpeg settings in `st_rtsp_main.py`, modify lines 20-30 as follows:

```python
process = subprocess.Popen(
    [
        'ffmpeg',
        '-hwaccel', 'vaapi',
        '-vaapi_device', '/dev/dri/renderD128',
        '-i', self.stream.rtsp_url,
        '-f', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-'
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
```

## **3. Run Test**
streamlit run test.py

## **4. Showcase**
![image](https://github.com/ccl-private/streamlit_rtsp/blob/main/src/converted.gif)
