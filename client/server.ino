#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "ESP32";  
const char* password = "01234567"; 

WebServer server(80);
String s = "";
String sa = "";
int t = 0;
bool f = true;
void setup() {
  Serial.begin(115200);
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }
  
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.on("/", handle_OnConnect);
  server.on("/1", handle_1);
  server.on("/2", hf);
  server.onNotFound(handle_NotFound);
  server.begin();
  Serial.println("server started");
}

void loop() {
  if (f){
  int x = analogRead(34);
  sa = sa+String(x)+" ";
  t = t + 1;
  if (t==6000){
    t = 0;
    s = sa;
    sa = "";
    f = false;
    server.handleClient();
  }
  delay(1);
  }else{
    server.handleClient();
    delay(500);
  }
}
void handle_OnConnect() {
  server.send(200, "text/plain", s); 
}
void handle_1() {
  s = "";
  f = false;
  server.send(200, "text/plain", s); 
}
void hf(){
  f = true;
  server.send(200, "text/plain", s);
}
void handle_NotFound(){
  server.send(404, "text/plain", "Not found");
}


