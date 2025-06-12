# from flask import Flask, Response, render_template
# import cv2

# app = Flask(__name__)

# video_path = "test.mp4"
# cap = cv2.VideoCapture(video_path)
# #cap = cv2.VideoCapture(video_path)

# def generate_frames():
#     while True:
#         success, frame = cap.read()

#         if not success:
#             # 영상이 끝났으면 처음으로 다시 열기
#             cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue

#         # 프레임을 JPEG 형식으로 인코딩
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()

#         # multipart 형식으로 반환 (MJPEG 스트리밍)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video')
# def video():
#     return Response(generate_frames(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

video_path1 = "C:/Users/kty15/OneDrive/바탕 화면/capstone/tset.mp4"
video_path2 = "C:/Users/kty15/OneDrive/바탕 화면/capstone/angle_1.mp4"
video_path3 = "C:/Users/kty15/OneDrive/바탕 화면/capstone/angle_2.mp4"
rtsp_url = "rtsp://admin:a123456@poseman.ddns.net/stream2"
cap4 = cv2.VideoCapture(rtsp_url)
cap1 = cv2.VideoCapture(video_path1)
cap2 = cv2.VideoCapture(video_path2)
cap3 = cv2.VideoCapture(video_path3)

# if not cap.isOpened():
#     raise IOError("❌ Could not open video file. Check path or codec.")
def generate_frames4():
    while True:
        success, frame = cap4.read()
        if not success:
            print("프레임 수신 실패, 재시도 중...")
            cap4.open(rtsp_url)
            continue

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
def generate_frames1():
    while True:
        success, frame = cap1.read()

        if not success:
            print("🔁 Rewinding video...")
            cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
def generate_frames2():
    while True:
        success, frame = cap2.read()

        if not success:
            print("🔁 Rewinding video...")
            cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
def generate_frames3():
    while True:
        success, frame = cap3.read()

        if not success:
            print("🔁 Rewinding video...")
            cap3.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video1')
def video1():
    return Response(generate_frames1(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/video2')
def video2():
    return Response(generate_frames2(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/video3')
def video3():
    return Response(generate_frames3(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video4')
def video4():
    return Response(generate_frames4(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', threaded=True)
