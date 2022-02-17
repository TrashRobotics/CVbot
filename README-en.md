<h1 align="center">
  <a href=""><img src="https://github.com/TrashRobotics/CVbot/blob/main/img/robot.jpeg" alt="A robot to work with openCV" width="800"></a>
  <br>
	A simple robot to work with openCV
  <br>
</h1>

<p align="center">
  <a href="https://github.com/TrashRobotics/CVbot/blob/main/README.md">Русский(Russian)</a> •
  <a href="https://github.com/TrashRobotics/CVbot/blob/main/README-en.md">English</a> 
</p>

## Main parts of the platform
* orange pi zero 512mb;
* web-camera;
* usb splitter or logic level converter;
* usb-ttl converter;
* XL4005 dc/dc converter;  
* arduino pro mini;
* MX1508 motor driver;
* 4x yellow arduino TT gear motors;
* 2x 18650 batteries and battery compartment for them;
* toggle switch;
* wooden board or piece of plywood;

## Orange pi setup

### Connecting to an access point
```shell
sudo armbian-config
```
Go to **Network->WiFi**, select the needed access point,
enter the password and connect to it    
To find out your IP address, enter
```shell
ifconfig
```

### Installing dependencies
Updating:
```shell
sudo apt update
sudo apt upgrade
```
Installing the python package manager and supporting packages
```shell
sudo apt install python3-dev python3-pip python3-numpy
```
Installing some more dependencies
```shell
pip3 install --upgrade pip setuptools wheel
pip3 install flask pyserial 
```
Installing openCV
```shell
sudo apt install python3-opencv
```

### App launch
Downloading the project repository
```shell
git clone https://github.com/TrashRobotics/CVbot
```
and run the app
```shell
cd CVbot/python_app
python3 app.py -i (ip address orange pi) -p (port) -s (serial port)
```
Open a browser and type in
```shell
(ip address orange pi):(port)
```
For example:
```shell
192.168.42.1:5000
```     

For more details watch the video.