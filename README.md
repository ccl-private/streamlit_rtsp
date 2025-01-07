# streamlit_rtsp
show rtsp stream in streamlit web via ffmpeg, You can set the hardware acceleration manually set it in the code.

1. dependent environment:
sudo apt install ffmpeg
pip3 install streamlit opencv-python

2. change ffmpeg in st_rtsp_main.py line 20-32:

'''
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
'''

4. run test:
streamlit run test.py

5. showcase:
![image](https://github.com/ccl-private/streamlit_rtsp/blob/main/src/converted.gif)
