#ifndef MOTORCONTROLLER_H
#define MOTORCONTROLLER_H

#include <Arduino.h>

class MotorController {
public:
  MotorController(uint8_t pinINA1, uint8_t pinPWM);
  void begin();
  void setSpeed(uint8_t duty);  // 0-255
  void stop();
  
  uint8_t getCurrentDuty() const { return _currentDuty; }
  uint8_t getDutyPercent() const { return (_currentDuty * 100UL) / 255; }
  
private:
  uint8_t _pinINA1, _pinPWM;
  uint8_t _currentDuty;
};

#endif
