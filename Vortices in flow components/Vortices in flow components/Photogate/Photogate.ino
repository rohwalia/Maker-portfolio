
int sensor_pin=A0;
int led_pin=13;
int sensorValue=0;
int trigger=0;
int currentValue=0;
int difference=0;
int previousValue =0;
int difference_t=0;
float frequency=0;
const int len=200;
float f[len];
int arrayIndex = 0;
float k;
float sum=0;
float current_sum=0;
int i=1;
unsigned long startMillis;  //some global variables available anywhere in the program
unsigned long currentMillis;
const unsigned long period = 1000;  //the value is a number of milliseconds
void setup() {
  Serial.begin(9600);
  pinMode(led_pin, OUTPUT);
  digitalWrite(led_pin, HIGH);
  startMillis = millis();  //initial start time
  // put your setup code here, to run once:
}

void loop() {
  while (arrayIndex<=(len+1)){
    if (arrayIndex<=len) {
    currentValue = analogRead(sensor_pin);
    difference = currentValue - previousValue;
    currentMillis = millis();
      if (difference >= 2)  //test whether the period has elapsed
      {
        difference_t= currentMillis - startMillis;
        frequency = 1.0 / (difference_t/1000.0);
        Serial.println(frequency);
        f[arrayIndex]=frequency;
        startMillis = currentMillis;  //IMPORTANT to save the start time of the current LED state.
        arrayIndex = arrayIndex +1;
      }
    //Serial.println(difference);
    previousValue = currentValue;
    delay(10);
    }
    else {
      while (i<=len) {
      current_sum=sum+f[i];
      sum=current_sum;
      i++;
      }
      k = (float)sum / len;
      Serial.println(k);
      break;
   }
  }
}
