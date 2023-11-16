#include <util/atomic.h>
#define ENCODER_A 2 // Amarillo
#define ENCODER_B 3 // Verde
#define BUTTON_MOD 4

//Datos de la trama
char trama="0";
String bufferString;
String cadena;
int LED = 13;

char corte = ";";
String mode = "";
String lecture = "";


// Pin del Potenciómetro
const int pot = A0;


// Pines de Control Shield
const int E1Pin = 9;   // Velocidad 1   /// SE CAMBIO DEL PIN 10 AL 9 // HACER CAMBIO AL 10 EN CASO DE FALLA
const int M1Pin = 12;   // Direccion 1
const int E2Pin = 11;   // Velocidad 2
const int M2Pin = 13;   // Direccion 2

// Traducción de E1 para dirección con dos lineas
const int Ain1 = 6;
const int Ain2 = 7;

//Variable global de posición compartida con la interrupción
volatile int theta = 0;

//Variable global de pulsos compartida con la interrupción
volatile int pulsos = 0;
unsigned long timeold;
float resolution = 374.22;

//Variable Global Velocidad
int vel = 0;

//Variable Global Posicion
int ang = 0;

//Variable Global MODO
bool modo = false;

//Estructura del Motor
typedef struct{
  byte enPin;
  byte directionPin;
}

Motor;  // CLASE MOTOR
//Creo el objeto "motor" de la clase "Motor"
const Motor motor = {E1Pin, M1Pin};

//Constantes de dirección del Motor
const int Forward = LOW;
const int Backward = HIGH;

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

void setup(){
  // set timer 1 divisor to 1024 for PWM frequency of 30.64 Hz
  TCCR1B = TCCR1B & B11111000 | B00000101;
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  //Encoders como entradas
  pinMode(Ain1, OUTPUT);
  pinMode(Ain2, OUTPUT);
  pinMode(ENCODER_A, INPUT);
  pinMode(ENCODER_B, INPUT);
  //Pulsadores
  pinMode(BUTTON_MOD, INPUT_PULLUP);
  //Configura Motor
  pinMode(motor.enPin, OUTPUT);
  pinMode(motor.directionPin, OUTPUT);
  //Configurar Interrupción
  timeold = 0;
  attachInterrupt(digitalPinToInterrupt(ENCODER_A),leerEncoder,RISING);
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

void loop(){
  tramadatos();
  
  float posicion;
  float rpm;
  int value,dir=true;
  //Lee el Valore del Potenciometro
  value = lecture.toInt();
  //Serial.print("Valor::::  "); Serial.println(value);
  //Cambia de Modo Velociadad o Posición
  
  if(mode=="v"){
    modo=true;
  }else{
    modo=false;
  }
  delay(1);
  
  if(modo){
    //Transforma el valor del Pot a velocidad
    vel = map(value,0,1023,0,255);
    //Activa el motor dirección Forward con la velocidad
    setMotor(motor, vel, false);
    //Espera un segundo para el calculo de las RPM
    if (millis() - timeold >= 1000){
      //Modifica las variables de la interrupción forma atómica
      ATOMIC_BLOCK(ATOMIC_RESTORESTATE){
        //rpm = float(pulsos * 60.0 / 374.22); //RPM
        rpm = float((60.0 * 1000.0 / resolution ) / (millis() - timeold) *
        pulsos);
        timeold = millis();
        pulsos = 0;
      }
    }
      //Serial.print("SPEED WORKING HERE...  Vel:   "); Serial.print(vel); Serial.print("         RPM:    "); Serial.println(rpm);
      Serial.println(rpm);
      delay(50);
  }
  else{
    //Transforma el valor del Pot a ángulo
    ang = map(value,0,1023,0,360);
    //Modifica las variables de la interrupción forma atómica
    ATOMIC_BLOCK(ATOMIC_RESTORESTATE){
    posicion = (float(theta * 360.0 /resolution));
    }
    //Posiciona el ángulo con tolerancia +- 2
    if(ang > posicion+2){
      vel = 200;
      dir = true;
    }
    else if(ang < posicion-2){
      vel = 200;
      dir = false;
    }
    else{
      vel = 0;
    }
    setMotor(motor, vel, dir);
    //Serial.print("POSITION WORKING HERE...  Ang:   "); Serial.println(ang);
    Serial.println(ang);
    delay(50);
  }
}

//      FUNCIONES       ////////////////////////////////////////////////////////////////////////

//Función para dirección y velocidad del Motor  // MODIFICACION PARA L293D, L298N, TB6612FNG
void setMotor(const Motor motor, int vel, bool dir){
  analogWrite(motor.enPin, vel); 
  if(dir){
    digitalWrite(motor.directionPin, Forward);
    digitalWrite(Ain1, HIGH);
    digitalWrite(Ain2, LOW);
  }
  else{
    digitalWrite(motor.directionPin, Backward);
    digitalWrite(Ain1, LOW);
    digitalWrite(Ain2, HIGH);
  }
}




//Función para la lectura del encoder
void leerEncoder(){
  //Lectura de Velocidad
  if(modo)
  pulsos++; //Incrementa una revolución
  //Lectura de Posición
  else{
    int b = digitalRead(ENCODER_B);
    if(b > 0){
      //Incremento variable global
      theta++;
    }
    else{
      //Decremento variable global
      theta--;
    }
  }
}


//SEPARA LA TRAMA DE DATOS ENTRANTE
void tramadatos(){
  bufferString="";
  bool var1=false;
  bool var2=false;
  bool libre=true;
  
  while(Serial.available()){
        trama=Serial.read();  //Leer el siguiente Char de la cadena
        
        if(trama==';' && var1==false && libre==true){
          mode=bufferString;
          bufferString="";
          var1=true;
          libre=false;
          //Serial.print("mode=== ");
          //Serial.println(mode);
        }
        
        if(trama==';' && var1==true && var2==false && libre==true){
          lecture=bufferString;
          bufferString="";
          var2=true;
          libre=false;
          //Serial.print("lecture=== ");
          //Serial.println(lecture);
        }

        if(trama!=';'){
        bufferString+=trama; //Agrega el Char a la memoria temporal
        //Serial.println(trama);
        //Serial.println(bufferString);
        libre=true;
        }
        
        if(trama=='f'){
          bufferString="";
          /*Serial.println("RESULTADO DE TRAMA SEPARADA");
          Serial.println("_____________________");
          Serial.print("Mode: >>>>>"); Serial.println(mode);
          Serial.print("lecture: >>>>"); Serial.println(lecture);
          Serial.println("_____________________");*/
          return("");
         }
    }
}
