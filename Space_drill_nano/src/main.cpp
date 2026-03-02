#include <Arduino.h>

void setup() {
  Serial.begin(115200);
}

void loop() {

  // Send sensordata
  int value = analogRead(A0);
  Serial.println(value);

  // Tjek for kommando
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');

    if (cmd == "LED_ON") digitalWrite(13, HIGH);
    if (cmd == "LED_OFF") digitalWrite(13, LOW);
  }

  delay(100);
}
