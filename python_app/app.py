from flask import Flask, render_template, Response, request
import cv2
import serial
import threading
import time
import json
import argparse

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # веб камера

controlX, controlY = 0, 0  # глобальные переменные положения джойстика с web-страницы


def getFramesGenerator():
    """ Генератор фреймов для вывода в веб-страницу, тут же можно поиграть с openCV"""
    while True:
        time.sleep(0.01)    # ограничение fps (если видео тупит, можно убрать)
        success, frame = camera.read()  # Получаем фрейм с камеры
        if success:
            frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)  # уменьшаем разрешение кадров (если видео тупит, можно уменьшить еще больше)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   # перевод изображения в градации серого
            # _, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)  # бинаризуем изображение
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """ Генерируем и отправляем изображения с камеры"""
    return Response(getFramesGenerator(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """ Крутим html страницу """
    return render_template('index.html')


@app.route('/control')
def control():
    """ Пришел запрос на управления роботом """
    global controlX, controlY
    controlX, controlY = float(request.args.get('x')) / 100.0, float(request.args.get('y')) / 100.0
    return '', 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    # пакет, посылаемый на робота
    msg = {
        "speedA": 0,  # в пакете посылается скорость на левый и правый борт тележки
        "speedB": 0  #
    }

    # параметры робота
    speedScale = 0.65  # определяет скорость в процентах (0.50 = 50%) от максимальной абсолютной
    maxAbsSpeed = 100  # максимальное абсолютное отправляемое значение скорости
    sendFreq = 10  # слать 10 пакетов в секунду

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000, help="Running port")
    parser.add_argument("-i", "--ip", type=str, default='127.0.0.1', help="Ip address")
    parser.add_argument('-s', '--serial', type=str, default='/dev/ttyUSB0', help="Serial port")
    args = parser.parse_args()

    serialPort = serial.Serial(args.serial, 9600)   # открываем uart

    def sender():
        """ функция цикличной отправки пакетов по uart """
        global controlX, controlY
        while True:
            speedA = maxAbsSpeed * (controlY + controlX)    # преобразуем скорость робота,
            speedB = maxAbsSpeed * (controlY - controlX)    # в зависимости от положения джойстика

            speedA = max(-maxAbsSpeed, min(speedA, maxAbsSpeed))    # функция аналогичная constrain в arduino
            speedB = max(-maxAbsSpeed, min(speedB, maxAbsSpeed))    # функция аналогичная constrain в arduino

            msg["speedA"], msg["speedB"] = speedScale * speedA, speedScale * speedB     # урезаем скорость и упаковываем

            serialPort.write(json.dumps(msg, ensure_ascii=False).encode("utf8"))  # отправляем пакет в виде json файла
            time.sleep(1 / sendFreq)

    threading.Thread(target=sender, daemon=True).start()    # запускаем тред отправки пакетов по uart с демоном

    app.run(debug=False, host=args.ip, port=args.port)   # запускаем flask приложение
