# Testing & Calibration Guide

## Setup Checklist
- Arduino UNO  
- HC-SR04 Ultrasonic Sensor  
- Buzzer  
- Jumper wires  
- USB cable  
- Arduino IDE installed  
- Files: speedbreakrr.ino, Proj csr.pdf, README.md, testing.md

Refer to **Proj csr.pdf (pages 3–5)** for wiring.

---

## Step 1: Basic Arduino Test
1. Connect Arduino to PC.
2. Upload “Blink” example:
   File → Examples → 01.Basics → Blink
3. If onboard LED blinks → Arduino is working.

---

## Step 2: Upload Project Code
1. Open speedbreakrr.ino.
2. Upload it.
3. Open Serial Monitor @ 9600 baud.
4. Move your hand near the sensor → distance updates.

---

## Calibration
1. Default threshold = 15 cm.
2. Move object closer → buzzer ON below 15 cm.
3. If needed, edit this value in the .ino:
   `if (distance > 0 && distance < THRESHOLD)`

---

## Troubleshooting
### No distance output
- Check: TRIG → 9, ECHO → 10, VCC → 5V, GND → GND.
- Serial monitor must be 9600 baud.

### Distance stuck at 0 or 999
- Sensor wired incorrectly.
- Object too close or too far.

### Buzzer not working
- Positive → D7, Negative → GND.
- Try another buzzer.

### Arduino not detected
- Different USB port or cable.

---

## Observations
- Distance when buzzer activates
- Reading stability
- Reaction delay
- Effect of surface types
