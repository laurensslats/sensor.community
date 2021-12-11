#include <Notecard.h>
#define serialDebug Serial
#define productUID "{productUID}" // add your Blues Wireless productUID
Notecard notecard;

//DHT11 setup
#include <DHT.h>
#define DHTPIN 5 // connect sensor to pin 5
#define DHTTYPE    DHT22     // DHT 22
DHT dht(DHTPIN, DHTTYPE);

//SDS011 setup
#include "SdsDustSensor.h"
int rxPin = 9;
int txPin = 6;
SdsDustSensor sds(rxPin, txPin);

float temperature = 0;
float humidity = 0;
float pm25 = 0;
float oldpm25 = 0;
float pm10 = 0;
float oldpm10 = 0;

void setup() {
  delay(2500);
  serialDebug.begin(115200);
  notecard.setDebugOutputStream(serialDebug);
  notecard.begin();

  J *req = notecard.newRequest("hub.set");
  JAddStringToObject(req, "product", productUID);
  JAddStringToObject(req, "mode", "periodic");
  JAddNumberToObject(req, "outbound", 60);
  JAddNumberToObject(req, "inbound", 120);
  notecard.sendRequest(req);

  dht.begin();
  sds.begin(); // this line will begin Serial1 with given baud rate (9600 by default)
}

void loop() {
  // get data from sds011
  sds.wakeup();
  delay(30000); // working 30 seconds

  // take 3 readings and send the average
  PmResult pm = sds.queryPm();
  delay(3000);
  PmResult pm2 = sds.queryPm();
  delay(3000);
  PmResult pm3 = sds.queryPm();

  float pm25a = pm.pm25;
  float pm10a = pm.pm10;
  float pm25b = pm2.pm25;
  float pm10b = pm2.pm10;
  float pm25c = pm3.pm25;
  float pm10c = pm3.pm10;
  float pm25 = (pm25a+pm25b+pm25c)/3;
  float pm10 = (pm10a+pm10b+pm10c)/3;

  Serial.print("PM2.5 = ");
  Serial.println(pm25);
  Serial.print("PM10 = ");
  Serial.println(pm10);
  
  WorkingStateResult state = sds.sleep();

  // get data from DHT22
  float temperature = dht.readTemperature(false); // false == Celsius, true == Fahrenheit
  float humidity = dht.readHumidity(false);
  Serial.print("Temperature = ");
  Serial.println(temperature);
  Serial.print("Humidity = ");
  Serial.println(humidity);
  
  // to reduce data, only send data if pm25 or pm10 changed with >= 1
  if (abs(oldpm25-pm25) >= 1 || abs(oldpm10-pm10) >= 1){
    oldpm25 = pm25;
    oldpm10 = pm10;

    // send data
    J *req = notecard.newRequest("note.add");
    if (req != NULL) {
        JAddBoolToObject(req, "sync", true);
        J *body = JCreateObject();
        if (body != NULL) {
            JAddNumberToObject(body, "temperature", temperature);
            JAddNumberToObject(body, "humidity", humidity);
            JAddNumberToObject(body, "pm25", pm25);
            JAddNumberToObject(body, "pm10", pm10);
            JAddItemToObject(req, "body", body);
            }
        notecard.sendRequest(req);
    } 
  }
  
  delay(270000); // wait 4.5 minutes minutes
}
