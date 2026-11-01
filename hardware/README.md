# Hardware

No schematic or layout yet. This is the starting outline.

## Size budget

From `python3 tools/size_estimate.py`:

| | Area | Example outline |
|---|---|---|
| Component courtyards | ~157 mm² | |
| Single-sided board | ~300 mm² | ~22 × 14 mm |
| **Double-sided board (target)** | **~185 mm²** | **~17 × 11 mm** |

**Double-sided is the target:**
- **Top side:** both radios, the ESP32-C3 and the two antenna connectors.
- **Back side:** the decoupling capacitors, the regulator and the less sensitive passives.

The largest parts are the processor (about 5 × 5 mm) and the two radios (about 4 × 4 mm each). There's little left
to shrink without removing a feature.

## Stack-up (proposal)

4-layer HDI, about 0.8 mm thick, with laser microvias:

| Layer | Role |
|---|---|
| L1 | Radios, processor, connectors; 50 Ω RF lines as coplanar waveguide |
| L2 | Solid ground |
| L3 | Power and SPI / UART routing |
| L4 | Passives, regulator; ground pour |

## Pads

Four castellated pads on one short edge, in the common receiver order: **5V, GND, TX, RX**. A boot pad and a status
LED sit beside them.

## Parts to confirm against datasheets

| Part | Notes |
|---|---|
| Semtech LR1121 | Package size, RF pin allocation, ExpressLRS target support |
| ESP32-C3 with in-package flash | Flash size needed by the current ExpressLRS build |
| Dual-band LTCC diplexer | Insertion loss below 0.5 dB at 915 MHz and 2.44 GHz |
| TCXO, 32 MHz | Stability and supply voltage per the LR1121 reference design |
| u.FL / IPEX MHF1 | Low-profile version |
