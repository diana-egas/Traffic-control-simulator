#include <SPI.h>
#include <Ethernet.h>

/**
 * Variables for the conection to the Firebase via proxy
 */
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
char serverName[] = "10.42.0.1";
IPAddress ip(10, 42, 0 , 5);
int serverPort = 8000;
EthernetClient client;
char pageAdd[64];

/**
 * Variables and constants for street A
 */
const int GREEN_A = 22;
const int YELLOW_A = 24;
const int RED_A = 26;
const int BUTTON_A = 31;
int BUTTON_STATE_A = 0;
int NUM_CARS_A = 0;
const int CARS_A1 = 32;
const int CARS_A2 = 34;
const int CARS_A3 = 36;
String STREET_STATE_A = "";
String PREV_ST_STATE_A = "Green";

/**
 * Variables and constants for street B
 */
const int GREEN_B = 38;
const int YELLOW_B = 40;
const int RED_B = 42;
const int BUTTON_B = 33;
int BUTTON_STATE_B = 0;
int NUM_CARS_B = 0;
const int CARS_B1 = 44;
const int CARS_B2 = 46;
const int CARS_B3 = 48;

/**
 * variables and constants for the crosswalk
 */
const int GREEN_P = 28;
const int RED_P = 30;
const int BUTTON_P = 35;
int BUTTON_STATE_P = 0;
int NUM_PEDESTRIANS = 0;
String STREET_STATE_B = "";

/**
 * Start Ethernet conection
 * Prepare the input and output elements
 * Define default state as green for street A
 */
void setup() {
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);
  Serial.println(F("Starting ethernet..."));
  Ethernet.begin(mac, ip);
  digitalWrite(10, HIGH);
  Serial.println(Ethernet.localIP());
  delay(2000);
  Serial.println(F("Ready"));
  pinMode(GREEN_A, OUTPUT);
  pinMode(YELLOW_A, OUTPUT);
  pinMode(RED_A, OUTPUT);
  pinMode(GREEN_B, OUTPUT);
  pinMode(YELLOW_B, OUTPUT);
  pinMode(RED_B, OUTPUT);
  pinMode(GREEN_P, OUTPUT);
  pinMode(RED_P, OUTPUT);
  pinMode(BUTTON_A, INPUT);
  pinMode(BUTTON_B, INPUT);
  pinMode(BUTTON_P, INPUT);
  pinMode(CARS_A1, OUTPUT);
  pinMode(CARS_A2, OUTPUT);
  pinMode(CARS_A3, OUTPUT);
  pinMode(CARS_B1, OUTPUT);
  pinMode(CARS_B2, OUTPUT);
  pinMode(CARS_B3, OUTPUT);
  green_light();
}

/**
 * Set green light for street A
 * Meaning red light for street B and crosswalk
 */
void green_light() {
  digitalWrite(GREEN_A, HIGH);
  digitalWrite(YELLOW_A, LOW);
  digitalWrite(RED_A, LOW);
  digitalWrite(GREEN_B, LOW);
  digitalWrite(YELLOW_B, LOW);
  digitalWrite(RED_B, HIGH);
  digitalWrite(GREEN_P, LOW);
  digitalWrite(RED_P, HIGH);
  flush_A();
}

/**
 * Set yellow light for street A
 * Keeping red light for street B and crosswalk
 */
void yellow_lightA() {
  digitalWrite(GREEN_A, LOW);
  digitalWrite(YELLOW_A, HIGH);
  digitalWrite(RED_A, LOW);
  digitalWrite(GREEN_B, LOW);
  digitalWrite(YELLOW_B, LOW);
  digitalWrite(RED_B, HIGH);
  digitalWrite(GREEN_P, LOW);
  digitalWrite(RED_P, HIGH);
}

/**
 * Set yellow light for street B
 * Keeping red light for street A and green for the crosswalk
 */
void yellow_lightB() {
  digitalWrite(GREEN_A, LOW);
  digitalWrite(YELLOW_A, LOW);
  digitalWrite(RED_A, HIGH);
  digitalWrite(GREEN_B, LOW);
  digitalWrite(YELLOW_B, HIGH);
  digitalWrite(RED_B, LOW);
  digitalWrite(GREEN_P, HIGH);
  digitalWrite(RED_P, LOW);
}

/**
 * Set red light for street A
 * Meaning green light for street B and crosswalk
 */
void red_light() {
  digitalWrite(GREEN_A, LOW);
  digitalWrite(YELLOW_A, LOW);
  digitalWrite(RED_A, HIGH);
  digitalWrite(GREEN_B, HIGH);
  digitalWrite(YELLOW_B, LOW);
  digitalWrite(RED_B, LOW);
  digitalWrite(GREEN_P, HIGH);
  digitalWrite(RED_P, LOW);
  flush_B();
  flush_P();
}

/**
 * Read input from the button and increment number of cars on street A
 * Update values on Firebase
 */
void car_lights_A() {
  BUTTON_STATE_A = digitalRead(BUTTON_A);
  if (BUTTON_STATE_A == HIGH) {
    NUM_CARS_A = NUM_CARS_A + 1;
    if (NUM_CARS_A >= 11) {
      digitalWrite(CARS_A3, HIGH);
    }
    if (NUM_CARS_A >= 6) {
      digitalWrite(CARS_A2, HIGH);
    }
    if (NUM_CARS_A >= 1) {
      digitalWrite(CARS_A1, HIGH);
    }
    sprintf(pageAdd, "/update.php?arduino_data[street1_cars]=%d", NUM_CARS_A);
    getPage(serverName, serverPort, pageAdd);
    Serial.println();
  }
}

/**
 * Read input from the button and increment number of cars on street B
 * Update values on Firebase
 */
void car_lights_B() {
  BUTTON_STATE_B = digitalRead(BUTTON_B);
  if (BUTTON_STATE_B == HIGH) {
    NUM_CARS_B = NUM_CARS_B + 1;
    if (NUM_CARS_B >= 11) {
      digitalWrite(CARS_B3, HIGH);
    }
    if (NUM_CARS_B >= 6) {
      digitalWrite(CARS_B2, HIGH);
    }
    if (NUM_CARS_B >= 1) {
      digitalWrite(CARS_B1, HIGH);
    }
    sprintf(pageAdd, "/update.php?arduino_data[street2_cars]=%d", NUM_CARS_B);
    getPage(serverName, serverPort, pageAdd);
    Serial.println();
  }
}

/**
 * Read input from the button and increment number of pedestrians at the crosswalk
 * Update values on Firebase
 */
void pedestrians() {
  BUTTON_STATE_P = digitalRead(BUTTON_P);
  if (BUTTON_STATE_P == HIGH) {
    NUM_PEDESTRIANS = NUM_PEDESTRIANS + 1;
    sprintf(pageAdd, "/update.php?arduino_data[pedestrian_number]=%d", NUM_PEDESTRIANS);
    getPage(serverName, serverPort, pageAdd);
    Serial.println();
  }
}

/**
 * Reset number of cars on street A
 * Update values on Firebase
 */
void flush_A() {
  NUM_CARS_A = 0;
  digitalWrite(CARS_A3, LOW);
  digitalWrite(CARS_A2, LOW);
  digitalWrite(CARS_A1, LOW);
  sprintf(pageAdd, "/update.php?arduino_data[street1_cars]=%d", NUM_CARS_A);
  getPage(serverName, serverPort, pageAdd);
  Serial.println();
}

/**
 * Reset number of cars on street B
 * Update values on Firebase
 */
void flush_B() {
  NUM_CARS_B = 0;
  digitalWrite(CARS_B3, LOW);
  digitalWrite(CARS_B2, LOW);
  digitalWrite(CARS_B1, LOW);
  sprintf(pageAdd, "/update.php?arduino_data[street2_cars]=%d", NUM_CARS_B);
  getPage(serverName, serverPort, pageAdd);
  Serial.println();
}

/**
 * Reset number of pedestrians at the crosswalk
 * Update values on Firebase
 */
void flush_P() {
  NUM_PEDESTRIANS = 0;
  sprintf(pageAdd, "/update.php?arduino_data[street1_pedestrians]=%d", NUM_PEDESTRIANS);
  getPage(serverName, serverPort, pageAdd);
  Serial.println();
}

/**
 * Connect to Firebase
 * Write information on Firebase
 * Disconect from Firebase
 */
byte getPage(char *ipBuf, int thisPort, char *page) {
  int inChar;
  char outBuf[128];
  Serial.print(F("connecting..."));
  if(client.connect(ipBuf, thisPort)) {
    Serial.println(F("connected"));
    sprintf(outBuf,"GET %s HTTP/1.1", page);
    client.println(outBuf);
    sprintf(outBuf,"Host: %s", serverName);
    client.println(outBuf);
    client.println(F("Connection: close\r\n"));
  } 
  else {
    Serial.println(F("failed"));
    return 0;
  }
  int connectLoop = 0;
  while(client.connected()) {
    while(client.available()) {
      inChar = client.read();
      Serial.write(inChar);
      connectLoop = 0;
    }
    connectLoop++;
    if(connectLoop > 10000) {
      Serial.println();
      Serial.println(F("Timeout"));
      client.stop();
    }
    delay(250);
  }
  Serial.println();
  Serial.println(F("disconnecting."));
  client.stop();
  return 1;
}

/**
 * Connect to Firebase
 * Read state of street A on Firebase
 * Disconect from Firebase
 */
byte readStreetA(char *ipBuf, int thisPort, char *page) {
  char inChar;
  char outBuf[128];
  STREET_STATE_A = "";
  bool reading = false;
  Serial.print(F("connecting..."));
  if(client.connect(ipBuf, thisPort)) {
    Serial.println(F("connected"));
    sprintf(outBuf,"GET %s HTTP/1.1", page);
    client.println(outBuf);
    sprintf(outBuf,"Host: %s", serverName);
    client.println(outBuf);
    client.println(F("Connection: close\r\n"));
  } 
  else {
    Serial.println(F("failed"));
    return 0;
  }
  int connectLoop = 0;
  while(client.connected()) {
    while(client.available()) {
      inChar = client.read();
       if (reading && inChar != '"') {
        STREET_STATE_A += inChar;
      }
      if (inChar == '"') {
        reading = !reading;
      }
      Serial.write(inChar);
      connectLoop = 0;
    }
    connectLoop++;
    if(connectLoop > 10000) {
      Serial.println();
      Serial.println(F("Timeout"));
      client.stop();
    }
    delay(250);
  }
  Serial.println();
  Serial.println(F("disconnecting."));
  client.stop();
  return 1;
}

/**
 * Increment the number of cars on the streets and the crosswalk only when there is a red light
 * Read street A light state on Firebase (STREET_STATE_A)
 * Change the light of the streets according to the state on Firebase
 * Reset number of cars on the streets when the light is yellow
 * Reset number of pedestrians at the crosswalk when street A has red light
 */
void loop() {
  if (PREV_ST_STATE_A == "Red") {
    car_lights_A();
  }
  if (PREV_ST_STATE_A == "Green") {
    car_lights_B();
    pedestrians();
  }
  sprintf(pageAdd, "/read_street1.php");
  readStreetA(serverName, serverPort, pageAdd);
  Serial.println();
  if(PREV_ST_STATE_A == "Green" && STREET_STATE_A == "Red") {
    yellow_lightA();
    delay(1000);
    red_light();
    PREV_ST_STATE_A = STREET_STATE_A;    
  }
  else if(PREV_ST_STATE_A == "Red" && STREET_STATE_A == "Green") {
    yellow_lightB();
    delay(1000);
    green_light();
    PREV_ST_STATE_A = STREET_STATE_A;    
  }
}
