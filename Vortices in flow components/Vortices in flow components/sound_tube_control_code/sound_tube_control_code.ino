
//velocity control
  float starting_v = 0.1; 
  float v_max = 20;
  float d_v = 0.1;
  int vel_time = 2500;
  const int pwm_pin = 9;

//sound sensor
  int sound = 0;
  int sound_pin = A3;
  int sound_threshold = 90;
  int sound_t = 2000;
  int sound_n = 200;

//wind sensor
  double sensor_min = 0;
  double sensor_max = 0;
  double sensor_mean = 0;
  int measuring_time = 5000;
  int measuringcount = 500;
  #define PIN_SENSOR_OUT A0
  #define PIN_SENSOR_TEMP A2


int calc_pwm(float vel) {
  int pwm = 27.82*exp(0.19*vel);
  return pwm;
}
float measureWind()
{
  int windADunits = analogRead(PIN_SENSOR_OUT);
  float windMPH =  pow((((float)windADunits - 264.0) / 85.6814), 3.36814);
  return windMPH*0.44704;
}
 void measurement(int duration, int number)
{
  float wind;
  sensor_min = 0;
  sensor_max = 0;
  sensor_mean = 0;
  for (int n = 0; n < number; n++)
  {
    wind = measureWind();
    sensor_min = min(wind, sensor_min);
    if (sensor_min == 0)
    {
      sensor_min = wind;
    }
    sensor_max = max(wind, sensor_max);
    sensor_mean += wind;
    delay(duration/number);
  }
  sensor_mean /= number;

}
 int measure_sound(int duration, int number)
{
  float sound;
  int sound_max = 0;
  for (int n = 0; n < number; n++)
  {
    sound = analogRead(sound_pin);
    sound_max = max(sound, sound_max);
    delay(duration/number);
  return sound_max;
}
}
int print_data(int i, int r)
{
    Serial.print (i);
    Serial.print (",");
    Serial.print(sensor_mean);
    Serial.print (",");
    Serial.print(sensor_min);
    Serial.print (",");
    Serial.print(sensor_max);
    Serial.print (",");
    Serial.print (r);
    Serial.print("\n");
}



void setup() {
  Serial.begin(9600);
  pinMode(pwm_pin, OUTPUT);
 delay(5000);
}

void loop() {

 


 for (float v = starting_v; v < v_max; v+=d_v)
 {
  int rot_speed = calc_pwm(v);
   analogWrite(pwm_pin,rot_speed);
//  for (int u =0; u < 10; u++){
//
//  Serial.println(analogRead(A3));
//  delay(100);
// }
   int current_maximum = measure_sound(sound_t,sound_n);
  if ( current_maximum > sound_threshold){
    measurement(measuring_time, measuringcount);
    print_data(rot_speed, current_maximum);
  }

  
 delay(4);

  }
}
 
