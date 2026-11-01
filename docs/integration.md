# Integration

## Wiring

| Pad | Connect to |
|---|---|
| 5V | Flight controller 5 V (receiver supply) |
| GND | Ground |
| TX | Flight controller UART RX |
| RX | Flight controller UART TX |

The pads are castellated, so the board can be soldered flat onto a carrier or wired with a short 4-wire lead. CRSF
runs at 420 000 baud by default.

## Flight controller setup

| Firmware | Setting |
|---|---|
| ArduPilot | `SERIALx_PROTOCOL = 23` (RCIN) on the receiver's UART; CRSF is auto-detected. Telemetry flows back automatically. |
| PX4 | `RC_CRSF_PRT_CFG` set to the receiver's UART |
| INAV / Betaflight | UART set to "Serial RX", receiver provider CRSF |

Confirm the parameter names against the firmware version you use.

## With the AERKI flight controller

The [AI-Flight-Controller](https://github.com/aerkii/AI-Flight-Controller) design reserves an internal UART and a
3.3 V supply for this receiver, along with an outline for mounting it on board. On that board, the two antenna
leads go to opposite arms of the frame, for diversity.

## Bench checks

1. Power up without antennas only briefly, and never transmit telemetry at high power without an antenna or a 50 Ω
   load.
2. Check the link statistics for both antennas. Their RSSI values should differ and change independently as the
   receiver moves, which shows the diversity paths are decorrelated.
3. Test cross-band mode by blocking one band, for example with a shield on one antenna, and confirm the link
   continues.
