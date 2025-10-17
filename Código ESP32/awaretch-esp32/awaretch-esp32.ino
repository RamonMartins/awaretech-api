#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// 1. Dados da sua rede Wi-Fi
const char* ssid = "brisa-3012659";
const char* password = "xs324hhh";

const char* enviar_sensor_vibracao = "https://awaretech-api.up.railway.app/enviar_sensor_vibracao";
const char* enviar_sensor_corrente = "https://awaretech-api.up.railway.app/enviar_sensor_corrente";

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
  Serial.println("Conectado!");
}

void loop() {
  // Atualiza valores dos sensores
  sensor1 = random(20, 30) + random(0, 100)/100.0;
  sensor2 = random(100, 200) + random(0, 100)/100.0;

  // Envia leitura do sensor 1
  EnviarDados(enviar_sensor_vibracao, sensor1);

  // Envia leitura do sensor 2
  EnviarDados(enviar_sensor_corrente, sensor2);

  delay(5000); // Espera 5 segundos antes da próxima leitura
}

void EnviarDados(const char* endpoint, float leitura){

  if(WiFi.status()== WL_CONNECTED){
    HTTPClient http;
    
    http.begin(endpoint);  // Inicia requisição HTTP
    http.addHeader("Content-Type", "application/json"); // Cabeçalho JSON

    // Monta JSON usando ArduinoJson ou manualmente
    String jsonPayload = "{";
    jsonPayload += "\"leitura_sensor\": " + String(leitura, 2);
    jsonPayload += "}";

    int httpResponseCode = http.POST(jsonPayload);

    if(httpResponseCode > 0){
      String response = http.getString();
      Serial.println("Resposta API: " + response);
    } else {
      Serial.println("Erro na requisição: " + String(httpResponseCode));
    }

    http.end();  // Fecha conexão
  }

}