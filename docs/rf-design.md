# RF design

## Front end (per chain)

```
                    ┌── sub-GHz match + low-pass ──┐
u.FL ── diplexer ───┤                              ├── LR1121 (sub-GHz RF and 2.4 GHz RF pins)
                    └── 2.4 GHz match + band-pass ─┘
```

- **Diplexer:** the LR1121 has separate RF pins for each band. A small LTCC diplexer (1608 size) joins them to one
  connector, so each chain needs only one dual-band antenna.
- **Matching:** each band has its own matching network and harmonic filter, using 0201 passives tuned on the real
  board with a network analyser. The receive and transmit paths share each network, with the transceiver's internal
  switching.
- **No external amplifier or low-noise amplifier:** both would add area, current and cost. The LR1121's receiver
  sensitivity and its built-in power amplifier are enough for a receiver.
- **TCXO:** one 32 MHz temperature-compensated oscillator per radio. Sub-GHz LoRa at narrow bandwidths needs that
  stability across the temperature swing of a drone.

## Antennas

| | Plan |
|---|---|
| Type | Dual-band dipole or T-antenna, 900 MHz + 2.4 GHz, on u.FL |
| Placement | The two antennas in different places on the airframe, ideally at 90° to each other, both clear of carbon fibre and batteries |
| Polarisation | Linear; orthogonal placement covers both orientations |

## Layout rules

- **Stack-up:** a 4-layer HDI board with a solid ground plane directly under every RF trace. 50 Ω coplanar
  waveguide from the connector to the diplexer and the radio.
- **Separation:** keep the two chains physically apart and mirrored, with a via fence between them. This limits
  cross-coupling, which would otherwise make the two diversity paths fade together.
- **Shared noise sources:** the ESP32-C3 and its 40 MHz crystal sit away from both RF chains. Its Wi-Fi radio is
  off in flight.
- **Clocks:** keep each radio's TCXO close to its LR1121, with short traces and nothing switching underneath.

## Regulatory

| Band | Typical limits (verify per country) |
|---|---|
| 2.4 GHz ISM | EU: 100 mW EIRP. US: FCC §15.247 allows up to 1 W conducted. |
| 868 MHz (EU) | Sub-band and duty-cycle limits apply; ExpressLRS has EU-specific regulatory builds |
| 915 MHz (US) | FCC §15.247 frequency hopping, up to 1 W |

The receiver's telemetry transmit power must respect the same limits. It's set in firmware, per regulatory domain.
