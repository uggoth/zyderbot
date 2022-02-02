int i = 0;
unsigned long time = 0;
bool flag = HIGH;
int test1 = 50;

void setup() {
  Serial.begin(115200);
  pinMode(10, OUTPUT); //direction control PIN 10 with direction wire 
  pinMode(11, OUTPUT); //PWM PIN 11  with PWM wire
}

void loop() {
  if (millis() - time > 10000)  {
    flag = !flag;
    digitalWrite(10, flag);
    time = millis();
  }
 for (test1 = 0; test1<170; test1++) {
      analogWrite(11, test1);  //input speed (must be int)
      delay(50);
 
  for(int j = 0;j<8;j++)  {
    i += pulseIn(9, HIGH, 500000); //SIGNAL OUTPUT PIN 9 with  white line,cycle = 2*i,1s = 1000000us，Signal cycle pulse number：27*2
  }
  i = i >> 3;
  Serial.print(111111 / i); //speed   r/min  (60*1000000/(45*6*2*i))
  Serial.println("  r/min");
  i = 0;
 }
}
