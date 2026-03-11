#include <Arduino.h>
#include <motorController.h> // library for controlling DC motor

bool light = false;

// Opret motor objekt globalt
MotorController motor(4, 5, 6);

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);  // Start med LED slukket

  // Initialiser motoren
  motor.begin();

  motor.setDirection(false);

  motor.setSpeed(200);

}

void loop() {

  // Tjek for kommando
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    
    Serial.print("<");
    Serial.print("example:");
    Serial.print(0);
    Serial.print(";example:");
    Serial.print(0);
    Serial.println(">");

    
    if (cmd == "IDLE") {
    }

    else if (cmd == "HOMING"){
      motor.setSpeed(200);
    }

    else if (cmd == "DRILL"){

    }

    else if (cmd == "LIFT"){

    }

    else if (cmd == "EMPTY"){

    }

    else if (cmd == "WEIGH"){

    }

    else if (cmd == "TRANSPORT"){

    }

    else if (cmd == "ERROR") {
      motor.stop();
    }

  }

  delay(100);
}