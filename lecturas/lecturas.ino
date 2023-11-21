#include "DHT.h" // Librería del sensor DHT11
#include <WiFi.h>
#include <FirebaseESP32.h>

#define FIREBASE_HOST "casa-domotica-da5dd-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "5l8WfCDrWfhdayROEzQsIH32IoajKILtMJQJlvsL"

FirebaseData casaDomotica;
String ruta = "lecturas";
WiFiClient esp32Client;

const char* ssid     = "Apa";
const char* password = "12345678";

#define DHTPIN 5
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
char datos[40];
String resultS = "";
int pinLed = 19;
int pinAlarma = 21;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  delay(1000);

  Serial.print("Se está conectando a la red wifi");
  Serial.println(ssid);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);

  float t = dht.readTemperature();
  Serial.println(F("DHTxx test!"));
  dht.begin();
  if (isnan(t)) {
    Serial.println(F("Falla en la lectura del sensor"));
    return;
  }

  pinMode(pinLed, OUTPUT);
  pinMode(pinAlarma, OUTPUT); // Agregado: Inicializar el pin de la alarma
  delay(500);
}

void loop() {
  float t = dht.readTemperature();

  // Leer datos desde Firebase
  if (Firebase.getString(casaDomotica, ruta + "/luz")) {
    String estadoLed = casaDomotica.stringData();
    Serial.print("Estado del LED: ");
    Serial.println(estadoLed);

    if (estadoLed == "1") {
      digitalWrite(pinLed, HIGH);
    } else if (estadoLed == "0") {
      digitalWrite(pinLed, LOW);
    }

    delay(1000);
  }

  if (Firebase.getString(casaDomotica, ruta + "/alarma")) {
    String estadoAlarma = casaDomotica.stringData();
    Serial.print("Estado de la alarma: ");
    Serial.println(estadoAlarma);

    if (estadoAlarma == "activada") {
      digitalWrite(pinAlarma, HIGH);
    } else if (estadoAlarma == "desactivada") {
      digitalWrite(pinAlarma, LOW);
    }

    delay(1000);
  }

  Serial.print(F("%  Temperatura: "));
  Serial.print(t);
  Serial.print(F("°C "));
  sprintf(datos, "Valor temperatura: %d ", static_cast<int>(t));
  delay(1000);

  delay(13000);
  Firebase.setInt(casaDomotica, ruta + "/temperatura", static_cast<int>(t));
}
