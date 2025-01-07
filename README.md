# streamlit_rtsp
show rtsp stream in streamlit web via ffmpeg, You can set the hardware acceleration manually set it in the code.

## **1. Dependent Environment**
sudo apt install ffmpeg

pip3 install streamlit opencv-python

## **2. Change ffmpeg Configuration**


To change the FFmpeg settings in `st_rtsp_main.py`, modify lines 20-30 as follows:

If you do not have the relevant hardware or install the relevant drivers, do not modify it.


for intel vaapi(You need to install the relevant drivers yourself)
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

for nvidia h264(You need to install the relevant drivers yourself)
```python
process = subprocess.Popen(
    [
        'ffmpeg',
        '-hwaccel', 'cuda',
        '-hwaccel_device', '0',  # Use the first GPU
        '-i', self.stream.rtsp_url,
        '-c:v', 'h264_nvenc',     # Use NVIDIA's H.264 encoder
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

## **Welcome to star**
