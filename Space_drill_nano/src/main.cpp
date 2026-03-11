#include <Arduino.h>
#include <motorController.h> // library for controlling DC motor

bool light = false;

// Opret motor objekt globalt
MotorController motor(5, 6);

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);  // Start med LED slukket

  // Initialiser motoren
  motor.begin();

}

void loop() {

  motor.setSpeed(200);

  // Tjek for kommando
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    
    Serial.print("<");
    Serial.print("cd_motor_current:");
    Serial.print(0);
    Serial.print(";example:");
    Serial.print(0);
    Serial.println(">");

    
  delay(100);}
}