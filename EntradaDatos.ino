
// SI EN EL SERIAL SE RECIBE LA CADENA"v;0;f", SE ENCENDERA EL LED13 POR 0.5SEG

char trama="0";
String bufferString;
String cadena;
int LED = 13;

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
}

void loop() {
  while(Serial.available()){
        trama=Serial.read();
        bufferString+=trama;
        if(trama=='f'){
          cadena=bufferString;
          bufferString="";
          Serial.println(cadena);
         }
    }
     
  if(cadena=="v;0;f"){
    digitalWrite(LED, HIGH);
    delay(500);
    digitalWrite(LED, LOW);
    cadena="0";
    } 
} 
