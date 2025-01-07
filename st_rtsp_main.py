import streamlit as st
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import numpy as np
import cv2

class VideoHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, stream=None, frame_callback=None, **kwargs):
        self.stream = stream
        self.frame_callback = frame_callback
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/video_feed':
            self.send_response(200)
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()

            process = subprocess.Popen(
                [
                    'ffmpeg',
                    '-i', self.stream.rtsp_url,
                    '-f', 'rawvideo',
                    '-pix_fmt', 'bgr24',
                    '-'
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # process = subprocess.Popen(
            #     [
            #         'ffmpeg',
            #         '-hwaccel', 'vaapi',
            #         '-vaapi_device', '/dev/dri/renderD128',
            #         '-i', self.stream.rtsp_url,
            #         '-f', 'rawvideo',
            #         '-pix_fmt', 'bgr24',
            #         '-'
            #     ],
            #     stdout=subprocess.PIPE,
            #     stderr=subprocess.PIPE
            # )

            width, height = self.stream.resolution
            try:
                while True:
                    raw_frame = process.stdout.read(width * height * 3)
                    if not raw_frame:
                        break

                    frame = np.frombuffer(raw_frame, np.uint8).reshape((height, width, 3))

                    if self.frame_callback is not None:
                        frame = self.frame_callback(frame)

                    _, jpeg = cv2.imencode('.jpg', frame)
                    self.wfile.write(b'--frame\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', str(len(jpeg)))
                    self.end_headers()
                    self.wfile.write(jpeg.tobytes())
                    self.wfile.write(b'\r\n')
            except Exception as e:
                print(f"Error: {e}")
            finally:
                process.stdout.close()
                process.stderr.close()
                process.wait()
        else:
            self.send_response(404)
            self.end_headers()

class RTSPVideoStream:
    def __init__(self, rtsp_url, port=5000):
        self.rtsp_url = rtsp_url
        self.port = port
        self.resolution = self.get_video_resolution()

    def get_video_resolution(self):
        command = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'csv=p=0',
            self.rtsp_url
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            resolution = result.stdout.decode('utf-8').strip().split(',')
            width, height = int(resolution[0]), int(resolution[1])
            return width, height
        else:
            print("Error:", result.stderr.decode('utf-8'))
            return None

    def run_server(self):
        while True:
            try:
                server_address = ('', self.port)
                httpd = HTTPServer(server_address, lambda *args, **kwargs: VideoHandler(*args, stream=self, **kwargs))
                httpd.serve_forever()
                break
            except Exception as e:
                print(e)
                self.port += 1

    def start_stream(self):
        threading.Thread(target=self.run_server, daemon=True).start()
        self.display_stream()

    def display_stream(self):
        flask_url = f"http://localhost:{self.port}"

        html_code = f"""
            <!doctype html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Video Feed</title>
                <style>
                    body {{ margin: 0; overflow: hidden; background-color: #000; }}
                    h1 {{ display: none; }}
                    #video {{ position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; object-fit: cover; }}
                    #controls {{ position: absolute; bottom: -100px; left: 0; right: 0; height: 80px; display: flex; justify-content: center; align-items: center; background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); transition: bottom 0.3s ease; }}
                    #controls.show {{ bottom: 0; }}
                    #fullscreenBtn, #refreshBtn {{ padding: 10px 20px; font-size: 16px; cursor: pointer; margin: 0 10px; background: rgba(255, 255, 255, 0.3); border: none; border-radius: 5px; transition: background 0.3s; }}
                    #fullscreenBtn:hover, #refreshBtn:hover {{ background: rgba(255, 255, 255, 0.5); }}
                </style>
            </head>
            <body>
                <img id="video" src="{flask_url}/video_feed" alt="Video Feed">
                <div id="controls">
                    <button id="fullscreenBtn">全屏</button>
                    <button id="refreshBtn">刷新</button>
                </div>
                <script>
                    const fullscreenBtn = document.getElementById('fullscreenBtn');
                    const refreshBtn = document.getElementById('refreshBtn');
                    const video = document.getElementById('video');
                    const controls = document.getElementById('controls');

                    video.addEventListener('mousemove', (event) => {{
                        const mouseY = event.clientY;
                        const videoHeight = window.innerHeight;

                        if (mouseY > videoHeight * 0.9) {{
                            controls.classList.add('show');
                        }} else {{
                            controls.classList.remove('show');
                        }}
                    }});

                    fullscreenBtn.addEventListener('click', () => {{
                        if (video.requestFullscreen) {{
                            video.requestFullscreen();
                        }} else if (video.mozRequestFullScreen) {{
                            video.mozRequestFullScreen();
                        }} else if (video.webkitRequestFullscreen) {{
                            video.webkitRequestFullscreen();
                        }} else if (video.msRequestFullscreen) {{
                            video.msRequestFullscreen();
                        }}
                    }});

                    refreshBtn.addEventListener('click', () => {{
                        video.src = video.src;
                    }});
                </script>
            </body>
            </html>
        """

        st.components.v1.html(html_code, height=360, width=640)

if __name__ == "__main__":
    rtsp_url = "rtsp://admin:zxkj@123@192.168.2.13:554/cam/realmonitor?channel=1&subtype=0"
    video_stream = RTSPVideoStream(rtsp_url)
    video_stream.start_stream()
