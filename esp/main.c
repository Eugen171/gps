/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ajoie <ajoie@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/05/28 12:56:42 by ajoie             #+#    #+#             */
/*   Updated: 2021/05/28 14:57:10 by ajoie            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

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
	char *start = buffer;
	char *ptr = buffer;

	do {
		ptr = start;
		*start = mySerial.read();
		while (*start == '$' && ptr - start < 4)
			*++ptr = mySerial.read();
	} while (start[4] != 'G');
	start = ptr;
	do {
		if ((*++ptr = mySerial.read()) == '$')
			start = ptr;
		while (*start == '$' && ptr - start < 5)
			*++ptr = mySerial.read();
	} while (start[4] != 'G');
	*start = 0;
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
