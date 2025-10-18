#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// 1. Dados da sua rede Wi-Fi
const char* ssid = "brisa-3012659";
const char* password = "xs324hhh";

// URLs da API
const char* enviar_sensor_vibracao = "https://awaretech-api.up.railway.app/enviar_sensor_vibracao";
const char* enviar_sensor_corrente_1 = "https://awaretech-api.up.railway.app/enviar_sensor_corrente_1";
const char* enviar_sensor_corrente_2 = "https://awaretech-api.up.railway.app/enviar_sensor_corrente_2";
const char* enviar_sensor_corrente_3 = "https://awaretech-api.up.railway.app/enviar_sensor_corrente_3";

// Simula leituras de sensores
float sensor_vibracao = 0;
float sensor_corrente_1 = 0;
float sensor_corrente_2 = 0;
float sensor_corrente_3 = 0;

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
  // Atualiza valores dos sensores (simulação)
  sensor_vibracao = random(20, 30) + random(0, 100)/100.0;
  sensor_corrente_1 = random(100, 200) + random(0, 100)/100.0;
  sensor_corrente_2 = random(50, 150) + random(0, 100)/100.0;
  sensor_corrente_3 = random(10, 50) + random(0, 100)/100.0;

  // Envia leitura Sensor de Vibração
  if (sensor_vibracao >= 23 && sensor_vibracao <= 28){
    EnviarDados(enviar_sensor_vibracao, sensor_vibracao, "Estável");
  }else{
    EnviarDados(enviar_sensor_vibracao, sensor_vibracao, "Instável");
  }
  
  // Envia leitura Sensor de Corrente 1
  if(sensor_corrente_1 >= 130 && sensor_corrente_1 <= 180){
    EnviarDados(enviar_sensor_corrente_1, sensor_corrente_1, "Estável");
  }else{
    EnviarDados(enviar_sensor_corrente_1, sensor_corrente_1, "Instável");
  }

  // Envia leitura Sensor de Corrente 2
  if(sensor_corrente_2 >= 80 && sensor_corrente_2 <= 120){
    EnviarDados(enviar_sensor_corrente_2, sensor_corrente_2, "Estável");
  }else{
    EnviarDados(enviar_sensor_corrente_2, sensor_corrente_2, "Instável");
  }

  // Envia leitura Sensor de Corrente 3
  if(sensor_corrente_3 >= 80 && sensor_corrente_3 <= 120){
    EnviarDados(enviar_sensor_corrente_3, sensor_corrente_3, "Estável");
  }else{
    EnviarDados(enviar_sensor_corrente_3, sensor_corrente_3, "Instável");
  }


  delay(5000); // Espera 5 segundos antes da próxima leitura
}

void EnviarDados(const char* endpoint, float leitura, const char* status){
  if(WiFi.status()== WL_CONNECTED){
    HTTPClient http;
    
    http.begin(endpoint);  // Inicia requisição HTTP
    http.addHeader("Content-Type", "application/json"); // Cabeçalho JSON

    // Monta JSON usando ArduinoJson ou manualmente
    String jsonPayload = "{";
    jsonPayload += "\"leitura_sensor\": " + String(leitura, 2) + ",";
    jsonPayload += "\"status\": \"" + String(status) + "\"";
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