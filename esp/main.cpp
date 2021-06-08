#include <ESP8266WiFi.h>
#include <Hash.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <FS.h>

#include <Wire.h>
#include <SoftwareSerial.h>

const char* ssid = "Keenetic-7343";
const char* password = "pwaMMmmE";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

// Configere GPS
SoftwareSerial mySerial(D4, D3); //Rx, Tx

char *get_raw_nmea(char *buf) {
	int i = 0;
	while (i < 1024 - 1)
	{
		if (mySerial.available())
		{
			buf[i] = mySerial.read();
			Serial.println(buf[i]);
			i++;
		}
	}
	buf[i] = 0;
	char *start = strstr(buf, "$GPGGA");
	if (start == NULL)
		return ("ops1");
	char *end = strstr(start + 1, "$GPGGA");
	if (end == NULL)
		return ("ops2");
	*end = 0;
	// Serial.println(start);
	return (start);
}

void setup(){
	Serial.begin(115200);
	mySerial.begin(9600);

	// Connect to Wi-Fi
	WiFi.begin(ssid, password);
	while (WiFi.status() != WL_CONNECTED) {
		delay(1000);
		Serial.println("Connecting to WiFi..");
	}

	// Print ESP32 Local IP Address
	Serial.println(WiFi.localIP());

	// Route for root / web page
	server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    char buf[1024];
		request->send_P(200, "text/plain", get_raw_nmea(buf));
	});

	// Start server
	server.begin();
}

void loop(){
}

/*
#include <SoftwareSerial.h>

SoftwareSerial mySerial(D4, D3); //Rx, Tx

void setup()
{
  Serial.begin(115200);
  mySerial.begin(9600);
}

void loop() {
  if (mySerial.available())
    Serial.write(mySerial.read());
  if (Serial.available())
    mySerial.write(Serial.read());
}
*/




/*
#include <SoftwareSerial.h>

SoftwareSerial mySerial(D4, D3); //Rx, Tx

void setup()
{
  Serial.begin(115200);
  mySerial.begin(9600);
}

void loop() {
  if (mySerial.available())
    Serial.write(mySerial.read());
  if (Serial.available())
    mySerial.write(Serial.read());
}
*/



/*
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>

TinyGPSPlus gps;
SoftwareSerial mySerial(D4, D3);
const char* ssid = "Keenetic-7343";
const char* password = "pwaMMmmE";
float latitude, longitude;
int year, month, date, hour, minute, second;
String date_str, time_str, lat_str, lng_str;
WiFiServer server(80);

void setup()
{
	Serial.begin(9600);
	mySerial.begin(9600);
	Serial.println();
	Serial.print("connecting to");
	Serial.println(ssid);
	WiFi.begin(ssid, password);
	while (WiFi.status() != WL_CONNECTED)
	{
		delay(500);
		Serial.print(".");
	}
	Serial.println("");
	Serial.println("WiFI connected");
	server.begin();
	Serial.println("Server started");
	Serial.println(WiFi.localIP());
}

void loop()
{
	if (mySerial.available())
		Serial.write(mySerial.read());
	if (Serial.available())
		mySerial.write(Serial.read());
	while (mySerial.available() > 0)
		if (gps.encode(mySerial.read()))
		{
			if (gps.location.isValid())
			{
				latitude = gps.location.lat();
				lat_str = String(latitude, 6);
				longitude = gps.location.lng();
				lng_str = String(longitude, 6);
			}
			if (gps.date.isValid())
			{
				date_str = "";
				date = gps.date.day();
				month = gps.date.month();
				year = gps.date.year();
				if (date < 10)
					date_str = '0';
				date_str += String(date);
				date_str += "/";

				if (month < 10)
					date_str += '0';
				date_str += String(month);
				date_str += "/";
				if (year < 10)
					date_str += '0';
				date_str += String(year);
			}
			if (gps.time.isValid())
			{
				time_str = "";
				hour = gps.time.hour();
				minute = gps.time.minute();
				second = gps.time.second();
				time_str += String(hour);
				time_str += ":";
				if (minute < 10)
					time_str += '0';
				time_str += String(minute); //values of hour,minute and time are stored in a string
        time_str += " : ";
        if (second < 10)
         time_str += '0';
        time_str += String(second); //values of hour,minute and time are stored in a string
			}
		}
	WiFiClient client = server.available();
	if (!client)
	{
		return;
	}
	String s = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n <!DOCTYPE html> <html> <head> <title>GPS DATA</title> <style>";
	s += "a:link {background-color: YELLOW;text-decoration: none;}";
	s += "table, th, td </style> </head> <body> <h1 style=";
	s += "font-size:300%;";
	s += " ALIGN=CENTER> GPS DATA</h1>";
	s += "<p ALIGN=CENTER style=""font-size:150%;""";
	s += "><b>Location Details</b></p><table ALIGN=CENTER style=";
	s += "width:50%";
	s += "> <tr> <th>Latitude</th>";
	s += "<td ALIGN=CENTER >";
	s += lat_str;
	s += "</td> </tr> <tr> <th>Longitude</th> <td ALIGN=CENTER >";
	s += lng_str;
	s += "</td> </tr> <tr> <th>Date</th> <td ALIGN=CENTER >";
	s += date_str;
	s += "</td></tr> <tr> <th>Time</th> <td ALIGN=CENTER >";
	s += time_str;
	s += "</td> </tr> </table>";

	s += "</body> </html>";

	client.print(s);
	delay(100);
}
*/
