from flask import Flask, render_template, Response, request
import cv2
import serial
import threading
import time
import json
import argparse

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # camera

controlX, controlY = 0, 0  # global joystick position variables from the web page


def getFramesGenerator():
    """ 用於輸出到網頁的幀生成器，您可以在此處使用 openCV"""
    while True:
        time.sleep(0.01)    # fps 限制（如果視頻很愚蠢，您可以將其刪除）
        success, frame = camera.read()  # 從相機獲取幀
        if success:
            # 降低幀分辨率（如果視頻很暗淡，可以進一步降低）
            frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 將圖像轉換為灰度
            # _, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)  # binarize the image
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """We generate and send images from the camera"""
    return Response(getFramesGenerator(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """ I am creating a html page """
    return render_template('index.html')


@app.route('/control')
def control():
    """ Received a request to control the robot """
    global controlX, controlY
    controlX, controlY = float(request.args.get(
        'x')) / 100.0, float(request.args.get('y')) / 100.0
    return '', 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    # 發送給機器人的數據包
    msg = {
        "speedA": 0,  # 數據包將速度發送到轉向架的左右兩側
        "speedB": 0  #
    }

    # 機器人參數
    speedScale = 0.65  # 將速度定義為最大絕對值的百分比 (0.50 = 50%)
    maxAbsSpeed = 100  # 要發送的最大絕對速度值
    sendFreq = 10  # 每秒發送 10 個數據包

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int,
                        default=5000, help="Running port")
    parser.add_argument("-i", "--ip", type=str,
                        default='127.0.0.1', help="Ip address")
    parser.add_argument('-s', '--serial', type=str,
                        default='/dev/ttyUSB0', help="Serial port")
    args = parser.parse_args()

    serialPort = serial.Serial(args.serial, 9600)   # 打開uart

    def sender():
        """ uart循環發送數據包功能 """
        global controlX, controlY
        while True:
            speedA = maxAbsSpeed * (controlY + controlX)    # 轉換機器人的速度
            speedB = maxAbsSpeed * (controlY - controlX)    # 取決於操縱桿的位置

            # 功能類似於arduino中的約束
            speedA = max(-maxAbsSpeed, min(speedA, maxAbsSpeed))
            # 功能類似於arduino中的約束
            speedB = max(-maxAbsSpeed, min(speedB, maxAbsSpeed))

            msg["speedA"], msg["speedB"] = speedScale * \
                speedA, speedScale * speedB     # 降低速度和包裝

            serialPort.write(json.dumps(msg, ensure_ascii=False).encode(
                "utf8"))  # 將包作為 json 文件發送
            time.sleep(1 / sendFreq)

    # 使用守護進程啟動一個線程以通過 uart 發送數據包
    threading.Thread(target=sender, daemon=True).start()

    app.run(debug=False, host=args.ip, port=args.port)   # 運行燒瓶應用程序
