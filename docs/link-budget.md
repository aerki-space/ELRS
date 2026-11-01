# Link budget

From `python3 tools/link_budget.py`. The assumptions are at the top of the script.

**Inputs:**
- **Transmitter module:** 100 mW at 2.4 GHz, 250 mW at 900 MHz.
- **Receiver telemetry:** +12 dBm at 2.4 GHz, +20 dBm at 900 MHz.
- **Antennas:** 2 dBi on both ends.
- **Receiver:** 6 dB noise figure, plus 3 dB implementation loss.
- **Fade margin:** 15 dB, reduced by 6 dB for true diversity.

The packet-rate table (spreading factor and bandwidth for each rate) is an assumption; check it against the
ExpressLRS version you ship.

| Band | Packet rate | Sensitivity | Control range | Telemetry range |
|---|---|---|---|---|
| 2.4 GHz | 500 Hz | −108 dBm | ~11 km | ~6 km |
| 2.4 GHz | 250 Hz | −111 dBm | ~15 km | ~8 km |
| 2.4 GHz | 150 Hz | −113 dBm | ~20 km | ~10 km |
| 2.4 GHz | 50 Hz | −116 dBm | ~27 km | ~14 km |
| 900 MHz | 200 Hz | −113 dBm | horizon (~51 km) | horizon |
| 900 MHz | 25 – 100 Hz | −116 to −121 dBm | horizon | horizon |

**How to read these numbers:**
- They're line-of-sight, free-space upper bounds. Terrain, trees, the airframe and antenna placement will shorten
  them, often by a lot, so the real figures will come from range tests.
- The 900 MHz band beats 2.4 GHz mainly because path loss is lower at lower frequencies. In practice it's limited
  by the radio horizon: about 51 km for a pilot antenna at 2 m and a drone at 120 m.
- Telemetry is the weaker link, because the receiver transmits at low power. Plan failsafe behaviour on losing
  telemetry, not just control.
