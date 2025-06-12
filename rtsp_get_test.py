from flask import Flask, Response, render_template_string
import cv2

app = Flask(__name__)

# RTSP 주소
rtsp_url = "rtsp://admin:a123456@poseman.ddns.net:554/stream1"
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    raise RuntimeError("RTSP 스트림을 열 수 없습니다.")

# MJPEG 프레임 생성 함수
def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            print("프레임 수신 실패, 재시도 중...")
            cap.open(rtsp_url)
            continue

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# HTML 페이지 렌더링
@app.route('/')
def index():
    return render_template_string('''
    <html>
    <head><title>RTSP Stream</title></head>
    <body>
        <h1>RTSP 실시간 영상 스트리밍</h1>
        <img src="/video" width="720" height="480">
    </body>
    </html>
    ''')

# 브라우저에서 MJPEG 요청을 처리하는 엔드포인트
@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
