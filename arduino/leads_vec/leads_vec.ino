#include "WheelSpeedSensor.h"

#define PIN_LFWSS 2
#define PIN_RFWSS 3
#define PIN_LRWSS 4
#define PIN_RRWSS 5
#define PIN_MRWSS 6

WheelSpeedSensor wss = WheelSpeedSensor(new ArrayList<int>({2}));

void setup() {
    pinMode(PIN_LFWSS, INPUT);
    pinMode(PIN_RFWSS, INPUT);
    pinMode(PIN_LRWSS, INPUT);
    pinMode(PIN_RRWSS, INPUT);
    pinMode(PIN_MRWSS, INPUT);
}

void loop() {
    if (pulse(PIN_LFWSS))
        Serial.write("A\n;");
}
