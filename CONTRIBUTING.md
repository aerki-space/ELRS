# ELRS: contributor notes

A nano ExpressLRS receiver: two LR1121 dual-band radios in true diversity, an ESP32-C3, and CRSF telemetry.
Design stage: docs and planning scripts. No schematic or PCB yet.

## Where things live
- `docs/`: design decisions and the numbers behind them. Numbers come from `tools/*.py`; when assumptions change,
  change them in the script, rerun it and update the doc from its output.
- `hardware/`: outline, stack-up, pads. Schematic and layout files will go here.

## Conventions
- The hardware design and the docs are MIT. Any ExpressLRS firmware change is GPL-3.0, like ExpressLRS itself.
  Keep firmware changes in a clearly separate directory, with its own licence notice.
- Mark planning estimates as estimates. Ranges are line-of-sight upper bounds until measured.
- Respect the regulatory limits for every band (see `docs/rf-design.md`).

## Checks before committing
```sh
python3 -m unittest discover -s tests
python3 tools/link_budget.py && python3 tools/size_estimate.py
```
