#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// WiFi credentials
const char* ssid = "WIFI_SSID";
const char* password = "WIFI_PASSWORD";

String lastLine1 = "";
String lastLine2 = "";

// LCD (change 0x27 to 0x3F if needed)
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Web server
ESP8266WebServer server(80);

// Handle requests
void handleSet()
{
  String line1 = server.arg("line1");
  String line2 = server.arg("line2");

  if(line1 == lastLine1 && line2 == lastLine2)
  {
    server.send(200, "text/plain", "No Change");
    return;
  }

  lcd.setCursor(0,0);

  String padded1 = line1;
  while(padded1.length() < 16)
    padded1 += " ";

  lcd.print(padded1);

  lcd.setCursor(0,1);

  String padded2 = line2;
  while(padded2.length() < 16)
    padded2 += " ";

  lcd.print(padded2);

  lastLine1 = line1;
  lastLine2 = line2;

  server.send(200, "text/plain", "Updated");
}

void setup()
{
  lcd.init();
  lcd.backlight();

  lcd.clear();
  lcd.print("Connecting...");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
  }

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connected!");

  lcd.setCursor(0, 1);
  lcd.print(WiFi.localIP());

  server.on("/set", handleSet);

  server.on("/", []() {
    server.send(200, "text/plain",
      "ESP8266 LCD Server Running\n"
      "Use:\n"
      "/set?line1=Hello&line2=World");
  });

  server.begin();
}

void loop()
{
  server.handleClient();
}
