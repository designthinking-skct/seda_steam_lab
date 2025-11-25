const int buzzer = 2; // Buzzer connected to pin 2
const int trigPin = 7; // Trigger pin of ultrasonic sensor
const int echoPin = 6; // Echo pin of ultrasonic sensor
const int blueBulb = 11;
const int redBulb = 10;


float duration, distance;
void setup() {
   pinMode(trigPin, OUTPUT);
   pinMode(echoPin, INPUT);
   pinMode(buzzer, OUTPUT);
   pinMode(blueBulb, OUTPUT);
   pinMode(redBulb, OUTPUT);
   Serial.begin(9600); // Initialize serial communication
}
void loop() {
   // Send a 10-microsecond pulse to TRIG pin
   digitalWrite(trigPin, LOW);
   delayMicroseconds(2);
   digitalWrite(trigPin, HIGH);
   delayMicroseconds(10);
   digitalWrite(trigPin, LOW);
   // Measure the duration of the echo pulse
   duration = pulseIn(echoPin, HIGH);
   // Calculate distance in cm
   distance = (duration * 0.034) / 2;
   Serial.print("Distance: ");
   Serial.print(distance);
   Serial.println(" cm");


    if (distance >= 10 && distance <= 15) {
        digitalWrite(blueBulb, HIGH); // Turn on LED
    }

    if (distance < 10 || distance > 15) {
         digitalWrite(blueBulb, LOW);
    }

    if (distance <= 5) {
        digitalWrite(redBulb, HIGH); // Turn on LED
    }

    if (distance > 5) {
        digitalWrite(redBulb, LOW);
    }

   // Activate buzzer if object is within 5 cm
   if (distance <= 5) {
       tone(buzzer, 1000); // Emit sound at 1000 Hz
   } else {
       noTone(buzzer); // Turn off buzzer
   }
   delay(100); // Short delay for stability
}
