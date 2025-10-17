#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>

// 1. Dados da sua rede Wi-Fi
const char* ssid = "iPhone de ramon";
const char* password = "87654320";

// URLs da API
const char* enviar_sensor_vibracao = "https://awaretech-api.up.railway.app/receber_sensor_vibracao";
const char* enviar_sensor_corrente = "https://awaretech-api.up.railway.app/receber_sensor_corrente";

// Simula leituras de sensores
float sensor1 = 0;
float sensor2 = 0;

void setup() {
  Serial.begin(115200);
  
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado ao WiFi!");
}

void loop() {
  // Atualiza valores dos sensores (simulação)
  sensor1 = random(20, 30) + random(0, 100)/100.0;
  sensor2 = random(100, 200) + random(0, 100)/100.0;

  // Envia leitura do sensor 1
  EnviarDados(enviar_sensor_vibracao, sensor1);

  // Envia leitura do sensor 2
  EnviarDados(enviar_sensor_corrente, sensor2);

  delay(5000); // Espera 5 segundos antes da próxima leitura
}

void EnviarDados(const char* endpoint, float leitura) {
  if (WiFi.status() == WL_CONNECTED) {

    WiFiClientSecure client;
    client.setInsecure();  // Ignora verificação SSL (necessário para HTTPS sem certificado local)

    HTTPClient http;
    http.begin(client, endpoint);  // Usa conexão segura
    http.addHeader("Content-Type", "application/json"); // Cabeçalho JSON

    // Monta JSON manualmente
    String jsonPayload = "{";
    jsonPayload += "\"leitura_sensor\": " + String(leitura, 2);
    jsonPayload += "}";

    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Resposta da API: " + response);
    } else {
      Serial.println("Erro na requisição: " + String(httpResponseCode));
    }

    http.end(); // Fecha conexão
  } else {
    Serial.println("WiFi desconectado, tentando reconectar...");
    WiFi.reconnect();
  }
}
