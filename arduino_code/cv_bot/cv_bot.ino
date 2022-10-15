#include "ArduinoJson.h"
#define IN1_PIN 5  // MX1508 電機驅動引腳
#define IN2_PIN 6  //
#define IN3_PIN 9  //
#define IN4_PIN 10 //
#define LED_PIN 13

// 來自橙色 pi 的數據包的 json 緩衝區
StaticJsonDocument<200> jsondoc;

// 全局速度變量
int16_t speedA = 0;
int16_t speedB = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(IN3_PIN, OUTPUT);
  pinMode(IN4_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop()
{
  DeserializationError err = deserializeJson(jsondoc, Serial); // 通過 uart 從橙色 pi 接收消息
  if (err == DeserializationError::Ok)                         // 如果收到消息
  {
    speedA = (float)jsondoc["speedA"] * 2.55; // 範圍 [-100; 100]
    speedB = (float)jsondoc["speedB"] * 2.55; // 擴展到 [-255; 255]
  }
  else
  {
    while (Serial.available() > 0)
      Serial.read(); // 清除緩衝區
  }
  moveA(speedA); // 更新電機速度狀態
  moveB(speedB); //
  delay(10);
}

void moveA(int16_t speed)
{
  // speed = -speed;
  if (speed >= 0)
  {
    analogWrite(IN1_PIN, LOW);
    analogWrite(IN2_PIN, abs(speed));
    digitalWrite(LED_BUILTIN, LOW);
  }
  else
  {
    analogWrite(IN1_PIN, abs(speed));
    analogWrite(IN2_PIN, LOW);
    digitalWrite(LED_BUILTIN, HIGH);
  }
}

void moveB(int16_t speed)
{
  if (speed >= 0)
  {
    analogWrite(IN3_PIN, LOW);
    analogWrite(IN4_PIN, abs(speed));
    digitalWrite(LED_BUILTIN, LOW);
  }
  else
  {
    analogWrite(IN3_PIN, abs(speed));
    analogWrite(IN4_PIN, LOW);
    digitalWrite(LED_BUILTIN, HIGH);
  }
}
