#include <DHT.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

constexpr byte sensorPin = 2;
constexpr byte switchPin = 4;
constexpr byte bluePin = 6;
constexpr byte redPin = 7;
constexpr byte fanPin = 9;
constexpr byte ventPin = 10;
constexpr float temperatureLimit = 28.0;
constexpr float humidityLimit = 65.0;

DHT sensor(sensorPin, DHT22);
LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo fan;
Servo vent;
float temperature = NAN;
float humidity = NAN;
unsigned long lastRead = 0;
int lastMode = -1;

void setup() {
  pinMode(switchPin, INPUT_PULLUP);
  pinMode(bluePin, OUTPUT);
  pinMode(redPin, OUTPUT);
  sensor.begin();
  lcd.init();
  lcd.backlight();
  lcd.print("Initializing...");
  fan.attach(fanPin);
  vent.attach(ventPin);
  fan.write(0);
  vent.write(0);
}

void updateActuators() {
  bool hot = !isnan(temperature) && temperature >= temperatureLimit;
  bool humid = !isnan(humidity) && humidity >= humidityLimit;
  digitalWrite(redPin, hot);
  digitalWrite(bluePin, humid);
  fan.write(hot ? 90 : 0);
  vent.write(humid ? 90 : 0);
}

void showReading(bool humidityMode) {
  lcd.clear();
  float value = humidityMode ? humidity : temperature;
  lcd.print(humidityMode ? "Humidity" : "Temperature");
  lcd.setCursor(0, 1);
  if (isnan(value)) {
    lcd.print("Sensor error");
    return;
  }
  lcd.print(value, 1);
  lcd.print(humidityMode ? " %" : " C");
}

void loop() {
  int mode = digitalRead(switchPin);
  if (millis() - lastRead >= 2100) {
    lastRead = millis();
    temperature = sensor.readTemperature();
    humidity = sensor.readHumidity();
    updateActuators();
    showReading(mode == LOW);
    lastMode = mode;
  } else if (lastMode != -1 && mode != lastMode) {
    showReading(mode == LOW);
    lastMode = mode;
  }
}
