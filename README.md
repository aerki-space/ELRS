# ELRS

A nano ExpressLRS receiver with dual-band true diversity and full telemetry, built to be as small as the radio
physics allows.

> **Status:** In active development. Hardware design files, firmware targets and validation results will be
> published as they are completed. Specifications below are design targets and may change.

## Key specifications

| | |
|---|---|
| Protocol | ExpressLRS |
| Bands | 900 MHz and 2.4 GHz, simultaneously |
| Diversity | True diversity: two complete radios, two antennas |
| Telemetry | Bidirectional: link quality, flight data, MAVLink |
| Output | CRSF over UART |
| Size | ~17 × 11 mm |
| Antennas | 2 × u.FL, dual-band |
| Input | 5 V |

## Repository layout

```
docs/
  architecture.md   radios, diversity, telemetry, processor, roadmap
  rf-design.md      dual-band front end, diplexers, antennas, layout rules
  link-budget.md    range estimates per mode (from tools/link_budget.py)
  integration.md    wiring, flight-controller setup, onboard use
hardware/
  README.md         outline, stack-up, pads, size budget
tools/
  link_budget.py    sensitivity and range per mode, control and telemetry links
  size_estimate.py  board-area budget
tests/              checks for the tools
```

## Quick start

```sh
python3 tools/link_budget.py
python3 tools/size_estimate.py
python3 -m unittest discover -s tests
```

## Roadmap

- Hardware design files
- Firmware target definition
- Range and diversity test results
- Native integration with the AERKI flight controller

More details coming soon.

## License

Hardware design and documentation: MIT, see [LICENSE](LICENSE). ExpressLRS firmware is GPL-3.0, and so is any
firmware change made for this receiver.
