<h1 align="center">
  <a href=""><img src="https://github.com/TrashRobotics/CVbot/blob/main/img/robot.jpeg" alt="Робот для работы с openCV" width="800"></a>
  <br>
	Простой робот для работы с openCV
  <br>
</h1>

<p align="center">
  <a href="https://github.com/TrashRobotics/CVbot/blob/main/README.md">Русский</a> •
  <a href="https://github.com/TrashRobotics/CVbot/blob/main/README-en.md">English(Английский)</a> 
</p>

## Основные детали тележки
* orange pi zero 512мб;
* веб-камера;
* usb-разветвитель или преобразователь логических уровней;
* usb-ttl преобразователь;
* XL4005 dc/dc преобразователь;  
* arduino pro mini;
* MX1508 драйвер двигателей;
* 4x желтые ардуино TT-мотор-редукторы;
* 2x 18650 аккумуляторы и батарейный отсек для них;
* тумблер;
* доска или кусок фанеры;

## Настройка Orange pi

### Подключаемся к точке доступа
```shell
sudo armbian-config
```
Переходим в **Network->WiFi**, выбираем нужную точку доступа,
вводим пароль и подключаемся к ней.    
Чтобы узнать свой ip-адресс вводим 
```shell
ifconfig
```

### Установка зависимостей
Обновляемся:
```shell
sudo apt update
sudo apt upgrade
```
Загружаем питоновый менеджер пакетов и вспомогательные пакеты
```shell
sudo apt install python3-dev python3-pip python3-numpy
```
Загружаем еще немного зависимостей
```shell
pip3 install --upgrade pip setuptools wheel
pip3 install flask pyserial 
```
Загружаем openCV
```shell
sudo apt install python3-opencv
```

### Запуск приложения
Скачиваем репозиторий проекта
```shell
git clone https://github.com/TrashRobotics/CVbot
```
и запускаем приложение
```shell
cd CVbot/python_app
python3 app.py -i (ip-адресс orange pi) -p (порт) -s (последовательный порт)
```
Открываем браузер и вводим в нем 
```shell
(ip-адресс orange pi):(порт)
```
Например так:
```shell
192.168.42.1:5000
```     

Подробнее про все остальное смотрите в видео