// Include the CapacitiveSensor library
#include <CapacitiveSensor.h>

// Create two capacitive sensor objects
// First sensor: send pin 4, receive pin 6
CapacitiveSensor Sensor1 = CapacitiveSensor(4, 6);

// Second sensor: send pin 8, receive pin 10
CapacitiveSensor Sensor2 = CapacitiveSensor(8, 10);

// Variables to store sensor values
long val1;
long val2;

// Variable to track the LED state (0 = off, 1 = on)
int pos = 0;

// Define the LED pin (built-in LED on pin 13)
#define led 13

void setup() {
  // Start serial communication at 9600 baud rate for debugging
  Serial.begin(9600);

  // Set the LED pin as output
  pinMode(led, OUTPUT);
}

void loop() {
  // Read capacitive values from both sensors
  val1 = Sensor1.capacitiveSensor(30);  // 30 samples for averaging
  val2 = Sensor2.capacitiveSensor(30);

  // Print the sensor values to the Serial Monitor
  Serial.print(val1);
  Serial.print("\t"); // Tab space between values
  Serial.print(val2);
  Serial.println();   // Move to the next line

  // If either sensor detects touch (value ≥ 100), toggle the LED
  if (val1 >= 100 || val2 >= 100) {
    if (pos == 0) {
      digitalWrite(led, HIGH); // Turn LED on
      pos = 1;                 // Update state
    } else {
      digitalWrite(led, LOW);  // Turn LED off
      pos = 0;                 // Update state
    }

    // Add a short delay to debounce and prevent multiple triggers
    delay(500);
  }

  // Small delay before the next loop iteration
  delay(10);
}
