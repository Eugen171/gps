#ifdef ESP32
	#include <WiFi.h>
	#include <ESPAsyncWebServer.h>
	#include <SPIFFS.h>
#else
	#include <Arduino.h>
	#include <ESP8266WiFi.h>
	#include <Hash.h>
	#include <ESPAsyncTCP.h>
	#include <ESPAsyncWebServer.h>
	#include <FS.h>
#endif
#include <Wire.h>
#include <SoftwareSerial.h>

const char* ssid = "Keenetic-7343";
const char* password = "pwaMMmmE";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

// Configere GPS
SoftwareSerial mySerial(D4, D3); //Rx, Tx 

char *get_raw_nmea(char *buffer){
	// gpgsa is begining
	int i;
	int prev_line_start = 0;

	i = 0;
	while (i != 6 || strncmp(buffer, "$GPGGA", 6) != 0) {
		buffer[i] = mySerial.read();
		if (buffer[i] == '$') {
			i = 0;
			buffer[0] = '$';
		}
		if (i > 2000) {
			buffer[0] = 0;
			return (buffer);
		}
		++i;
	}
	while (prev_line_start == 0
		|| i - prev_line_start != 6
		|| strncmp(&buffer[prev_line_start], "$GPGGA", 6) != 0)
	{
		buffer[i] = mySerial.read();

		if (buffer[i] == '$')
			prev_line_start = i;
		++i;
	}
	buffer[prev_line_start] = 0;
	return (buffer);
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
		char result[2048];
		get_raw_nmea(result);
		request->send_P(200, "text/plain", result);
	});

	// Start server
	server.begin();
}
 
void loop(){
}
