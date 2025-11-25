# Code Walkthrough — speedbreaker_alert_system

This walkthrough explains the Arduino sketch `code.ino` line-by-line and gives notes on behavior, tuning points, and simple improvements.

**File location (in your package):** `should be under the file code.ino`  
**Reference diagrams:** See `Proj csr.pdf` — Pages 3–5 for the original block & circuit diagrams.

---


## Note
All code is enclosed in between 
```cpp
.
.
.

```



## Top-level overview

The sketch reads distance from an HC-SR04 ultrasonic sensor and activates a buzzer when the measured distance is below a threshold (15 cm by default). It also prints distance values to the Serial Monitor for debugging and calibration.

---

## Full annotated code

```cpp
#define trigPin 9
#define echoPin 10
#define alertPin 7  // Buzzer
```
- Defines three constants for pins. Change these if you wire the sensor/buzzer to different pins.

```cpp
void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(alertPin, OUTPUT);
  digitalWrite(alertPin, LOW);
}
```
- `Serial.begin(9600)` starts serial logging so you can view distances in the Serial Monitor.
- `pinMode` sets the TRIG pin as an output (we drive it), ECHO as input (sensor drives it), and ALERT (buzzer) as output.
- `digitalWrite(alertPin, LOW)` ensures the buzzer is off initially.

```cpp
void loop() {
  long duration;
  int distance;
```
- `duration` will hold the echo pulse width in microseconds.
- `distance` will hold the computed distance in centimeters.

```cpp
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
```
- Standard HC-SR04 trigger sequence: hold TRIG low (clear), send a 10 µs HIGH pulse to request one measurement.

```cpp
  duration = pulseIn(echoPin, HIGH, 30000UL);
```
- `pulseIn()` measures the time (microseconds) that ECHO stays HIGH.
- The third parameter `30000UL` is a timeout (30,000 µs = 30 ms). If no echo is received within the timeout, `pulseIn()` returns 0, preventing the sketch from blocking indefinitely.

```cpp
  if (duration == 0) {
    distance = 999;
  } else {
    distance = duration * 0.034 / 2;
  }
```
- If `duration == 0` we set `distance` to `999` as a sentinel meaning “out of range / no echo”.
- Otherwise we convert microseconds to centimeters using the speed of sound approximation: `0.034 cm/µs`. We divide by 2 because the measured time is for a round trip (there and back).

```cpp
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
```
- Logs readings to Serial Monitor (9600 baud). Useful for observing behavior while calibrating.

```cpp
  if (distance > 0 && distance < 15) {
    digitalWrite(alertPin, HIGH);
  } else {
    digitalWrite(alertPin, LOW);
  }
```
- A simple threshold check: if distance is less than 15 cm, the buzzer turns ON; otherwise it is OFF.
- `distance > 0` avoids triggering on sentinel values like `999`.

```cpp
  delay(200);
}
```
- Adds a 200 ms pause between successive measurements. Adjust for faster or slower sampling.

---

## Tuning points and suggestions

- **Change trigger distance:** Edit `15` in the `if (distance > 0 && distance < 15)` check to your desired threshold, or replace with a named constant:
  ```cpp
  const int THRESHOLD_CM = 15;
  ```
  and then use `THRESHOLD_CM` in the `if`.

- **Timeout:** The 30 ms `pulseIn` timeout limits measurable range. 30 ms corresponds to a theoretical max range of about 5 meters (speed-of-sound round-trip). Adjust if you need longer range.

- **Filtering noisy readings:** To reduce false triggers, take multiple samples and average or require `N` consecutive below-threshold readings before sounding the buzzer. Example idea:
  - Read 5 times, compute median, then compare.

- **Debounce logic:** Require, for example, 3 consecutive measurements below threshold before turning on the buzzer, and 3 consecutive above to turn it off.

- **Buzzer current:** Some buzzers draw more current than an Arduino pin can safely supply. If your buzzer behaves erratically or is loud, use an NPN transistor (e.g., 2N2222) as a low-side switch with a base resistor (4.7kΩ) and a diode if needed. Connect emitter to GND, collector to buzzer negative, buzzer positive to 5V, and base to the Arduino pin via resistor. Keep GND common.

- **Power and wiring:** For stable results make sure the ultrasonic sensor has a stable 5V supply and good GND connections. Loose wires or long jumper wires can add noise.

---

## Quick checklist for debugging from code perspective

1. Upload `Blink` example to verify Board/Port.
2. Upload `speedbreakrr.ino`.
3. Open Serial Monitor at 9600 — you should see "Distance: XX cm" lines.
4. If you see `999` consistently, check wiring or point sensor at a reflective surface; very absorbent surfaces may not return a measurable echo.
5. If buzzer never sounds, verify pin mapping (buzzer to D7), and that buzzer negative is connected to GND.

---

## Where to look in your notes / diagrams

- Wiring and component list are in your scanned notebook: **`/mnt/data/Proj csr.pdf` — Pages 3–5**. Use that as the authoritative wiring reference.

---

## Small example: add averaging (idea)

```cpp
int readDistance() {
  long sum = 0;
  const int SAMPLES = 5;
  for (int i = 0; i < SAMPLES; ++i) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    long dur = pulseIn(echoPin, HIGH, 30000UL);
    if (dur == 0) return 999;
    sum += dur * 0.034 / 2;
    delay(20);
  }
  return sum / SAMPLES;
}
```

Call `readDistance()` in `loop()` instead of the single measurement to reduce jitter.

---

