# from fastapi import FastAPI
# from fastapi.responses import StreamingResponse, HTMLResponse
# import cv2

# app = FastAPI()

# # 각 영상 파일 및 RTSP 주소
# video_path1 = "C:/Users/kty15/OneDrive/바탕 화면/capstone/tset.mp4"
# video_path2 = "C:/Users/kty15/OneDrive/바탕 화면/capstone/angle_1.mp4"
# video_path3 = "C:/Users/kty15/OneDrive/바탕 화면/capstone/angle_2.mp4"
# #rtsp_url = "rtsp://admin:a123456@poseman.ddns.net/stream1"

# # VideoCapture 객체 생성
# cap1 = cv2.VideoCapture(video_path1)
# cap2 = cv2.VideoCapture(video_path2)
# cap3 = cv2.VideoCapture(video_path3)
# #cap4 = cv2.VideoCapture(rtsp_url)

# # 공통 프레임 생성 함수
# def generate_frames(cap, rewind=False, reconnect_url=None):
#     while True:
#         success, frame = cap.read()
#         if not success:
#             if rewind:
#                 cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#                 continue
#             elif reconnect_url:
#                 cap.open(reconnect_url)
#                 continue
#             else:
#                 break

#         ret, buffer = cv2.imencode('.jpg', frame)
#         if not ret:
#             continue

#         yield (b"--frame\r\n"
#                b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

# # HTML 페이지 라우트
# @app.get("/", response_class=HTMLResponse)
# async def index():
#     return """
#     <html>
#         <head><title>FastAPI Multi-Video Stream</title></head>
#         <body>
#             <h1>Local Videos</h1>
#             <h3>Video 1</h3><img src="/video1" width="480"><br>
#             <h3>Video 2</h3><img src="/video2" width="480"><br>
#             <h3>Video 3</h3><img src="/video3" width="480"><br>
#             <h1>RTSP Stream</h1>
#             <h3>Camera Stream</h3><img src="/video4" width="480">
#         </body>
#     </html>
#     """

# # 각 스트리밍 엔드포인트
# @app.get("/video1")
# def video1():
#     return StreamingResponse(generate_frames(cap1, rewind=True), media_type="multipart/x-mixed-replace; boundary=frame")

# @app.get("/video2")
# def video2():
#     return StreamingResponse(generate_frames(cap2, rewind=True), media_type="multipart/x-mixed-replace; boundary=frame")

# @app.get("/video3")
# def video3():
#     return StreamingResponse(generate_frames(cap3, rewind=True), media_type="multipart/x-mixed-replace; boundary=frame")

# # @app.get("/video4")
# # def video4():
# #     return StreamingResponse(generate_frames(cap4, rewind=False, reconnect_url=rtsp_url), media_type="multipart/x-mixed-replace; boundary=frame")


# import cv2
# import threading
# import time
# from fastapi import FastAPI
# from fastapi.responses import StreamingResponse, HTMLResponse

# app = FastAPI()

# video_paths = [
#     "C:/Users/kty15/OneDrive/바탕 화면/capstone/tset.mp4",
#     "C:/Users/kty15/OneDrive/바탕 화면/capstone/angle_1.mp4",
#     "C:/Users/kty15/OneDrive/바탕 화면/capstone/angle_2.mp4"
# ]

# caps = [cv2.VideoCapture(p) for p in video_paths]
# frames = [None] * len(video_paths)

# def sync_video_loop():
#     global frames
#     fps = 30
#     while True:
#         for i, cap in enumerate(caps):
#             success, frame = cap.read()
#             if not success:
#                 cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#                 success, frame = cap.read()
#             frames[i] = frame
#         time.sleep(1 / fps)

# def generate(index: int):
#     while True:
#         frame = frames[index]
#         if frame is None:
#             continue
#         ret, buffer = cv2.imencode('.jpg', frame)
#         if not ret:
#             continue
#         yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

# @app.get("/")
# def index():
#     return HTMLResponse("""
#     <html><body>
#         <h1>동기화된 영상 스트림</h1>
#         <img src="/video0" width="480">
#         <img src="/video1" width="480">
#     </body></html>
#     """)

# @app.get("/video{idx}")
# def video(idx: int):
#     return StreamingResponse(generate(idx-1), media_type="multipart/x-mixed-replace; boundary=frame")

# # 백그라운드에서 동기화 루프 실행
# threading.Thread(target=sync_video_loop, daemon=True).start()

import cv2
import threading
import time
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse, HTMLResponse
import subprocess
import numpy as np

app = FastAPI()

# 영상 경로 및 VideoCapture 생성
video_paths = [
    "C:/Users/kty15/OneDrive/바탕 화면/capstone/angle_1_fps3.mp4",
    "C:/Users/kty15/OneDrive/바탕 화면/capstone/angle_2_fps3.mp4",
    "C:/Users/kty15/OneDrive/바탕 화면/capstone/angle_3_fps3.mp4",
]
rtsp_url = "rtsp://admin:a123456@poseman.ddns.net:554/stream1"
caps = [cv2.VideoCapture(p) for p in video_paths]

frames = [None] * len(caps)
fps_list = [cap.get(cv2.CAP_PROP_FPS) or 30 for cap in caps]  # fallback 30

# 각 비디오에 대해 동기화 루프 시작
def sync_reader(index: int):
    global frames
    cap = caps[index]
    fps = fps_list[index]
    delay = 1 / fps if fps > 0 else 1 / 30

    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        frames[index] = frame
        time.sleep(delay)

# 스트림 요청에 대한 응답 (최신 프레임만 MJPEG 전송)
def generate(index: int):
    while True:
        frame = frames[index]
        if frame is None:
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
    <head><title>FPS-Synced Multi Stream</title></head>
    <body>
        <h1>동기화된 영상 스트림</h1>
        <img src="/video1" width="480">
        <img src="/rtsp" width="480">
    </body>
    </html>
    """

@app.get("/video{idx}")
def video(idx: int):
    return StreamingResponse(generate(idx - 1), media_type="multipart/x-mixed-replace; boundary=frame")

def get_rtsp_stream(rtsp_url="rtsp://admin:a123456@poseman.ddns.net/stream1", width=1920, height=1080):
    FFMPEG_BIN = r"C:\Users\kty15\Downloads\ffmpeg-2025-06-04-git-a4c1a5b084-full_build\ffmpeg-2025-06-04-git-a4c1a5b084-full_build\bin\ffmpeg.exe"
    cmd = [
        FFMPEG_BIN,
        '-rtsp_transport', 'tcp',  # or 'udp'
        '-i', rtsp_url,
        '-f', 'image2pipe',
        '-pix_fmt', 'bgr24',
        '-vcodec', 'rawvideo', '-'
    ]
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    while True:
        raw = pipe.stdout.read(width * height * 3)
        if len(raw) != width * height * 3:
            continue

        # 1) numpy.ndarray 로 변환
        frame = np.frombuffer(raw, dtype=np.uint8).reshape((height, width, 3))

        # 2) JPEG 로 인코딩
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        # 3) MJPEG multipart header + JPEG 바이트 합쳐서 yield
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            jpeg.tobytes() +
            b'\r\n'
        )

@app.get("/rtsp")
def get_rtsp(
    rtsp_url: str = Query(default="rtsp://admin:a123456@poseman.ddns.net/stream1"),
    width: int = Query(default=1920),
    height: int = Query(default=1080)
):
    return StreamingResponse(
        get_rtsp_stream(rtsp_url, width, height),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# 비디오별 동기화 스레드 시작
for i in range(len(caps)):
    threading.Thread(target=sync_reader, args=(i,), daemon=True).start()
