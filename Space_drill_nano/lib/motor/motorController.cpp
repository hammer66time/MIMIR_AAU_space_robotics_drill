#include "motorController.h"

MotorController::MotorController(uint8_t pinINA1, uint8_t pinPWM)
  : _pinINA1(pinINA1), _pinPWM(pinPWM), _currentDuty(0) {}

void MotorController::begin() {
  pinMode(_pinINA1, OUTPUT);
  //pinMode(_pinINA2, OUTPUT);
  pinMode(_pinPWM, OUTPUT);
  digitalWrite(_pinINA1, HIGH);  // Enable H-bridge/input
  stop();
}

void MotorController::setSpeed(uint8_t duty) {
  _currentDuty = duty;
  digitalWrite(_pinINA1, (_currentDuty > 0) ? HIGH : LOW);
  analogWrite(_pinPWM, _currentDuty);
}

void MotorController::stop() {
  setSpeed(0);
}