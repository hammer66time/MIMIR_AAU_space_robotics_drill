#include <Arduino.h>

bool light = false;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {

  // Send sensordata
  int value = analogRead(A0);
  Serial.println(value);

  // Tjek for kommando
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');

    if (cmd == "LED_ON") light = true;
    if (cmd == "LED_OFF") light = false;
  }

  if (light == true){
    digitalWrite(LED_BUILTIN, HIGH);
  }
  if (light != true){
    digitalWrite(LED_BUILTIN, LOW);
  }

  delay(100);
}