#!/usr/bin/env python3
"""Board-area estimate for the dual-band true-diversity nano receiver.

Footprint areas include courtyard; the packing factor covers routing, RF keep-outs and
matching networks. Package sizes are typical values - confirm each against its datasheet.

    python3 tools/size_estimate.py
"""
import math

# (part, qty, footprint mm x mm incl. courtyard)
PARTS = [
    ('LR1121 dual-band transceiver (QFN, ~4x4)', 2, (4.6, 4.6)),
    ('32 MHz TCXO (2016)', 2, (2.4, 2.0)),
    ('ESP32-C3 with in-package flash (QFN32 5x5)', 1, (5.6, 5.6)),
    ('40 MHz crystal (2016)', 1, (2.4, 2.0)),
    ('u.FL / IPEX MHF1 connector', 2, (3.0, 3.0)),
    ('Dual-band diplexer (LTCC 1608)', 2, (2.0, 1.2)),
    ('RF matching / filter passives (0201), per band per radio', 4, (2.0, 1.5)),
    ('3.3 V LDO (DFN 1x1)', 1, (1.4, 1.4)),
    ('Decoupling and bias passives (0201)', 1, (6.0, 3.0)),
    ('Status LED (0402) + boot pad', 1, (1.5, 1.2)),
    ('Solder pads: 5V, GND, TX, RX (castellated edge)', 1, (8.0, 1.6)),
]
PACKING = 1.9          # one-sided placement, 4-layer HDI, RF keep-outs
DOUBLE_SIDED = 0.62    # area fraction needed when the passives and connectors use the back side too


def area():
    raw = sum(q * w * h for _, q, (w, h) in PARTS)
    return raw, raw * PACKING, raw * PACKING * DOUBLE_SIDED


def main():
    raw, one, two = area()
    for name, q, (w, h) in PARTS:
        print(f'  {q} x {name:58s} {q*w*h:6.1f} mm2')
    print(f'component courtyard total: {raw:.0f} mm2')
    print(f'board area, single-sided : {one:.0f} mm2  (e.g. {math.sqrt(one*1.6):.1f} x {math.sqrt(one/1.6):.1f} mm)')
    print(f'board area, double-sided : {two:.0f} mm2  (e.g. {math.sqrt(two*1.6):.1f} x {math.sqrt(two/1.6):.1f} mm)')
    print('for reference: single-radio 2.4 GHz nano receivers are commonly ~10 x 10 mm')


if __name__ == '__main__':
    main()
