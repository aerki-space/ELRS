#!/usr/bin/env python3
"""Line-of-sight range estimate per ExpressLRS-style LoRa mode, uplink (control) and downlink (telemetry).

Sensitivity uses the LoRa formula S = -174 + 10 log10(BW) + NF + SNR_min(SF).
The mode table (SF/BW per packet rate) is an assumption to check against the ExpressLRS
source for the firmware version you ship. Free-space only: terrain, Fresnel-zone
blockage and the airframe cost real range, so treat results as an upper bound.

    python3 tools/link_budget.py
"""
import math

SNR_MIN = {5: -2.5, 6: -5.0, 7: -7.5, 8: -10.0, 9: -12.5, 10: -15.0}   # dB, Semtech LoRa demodulator limits

# (band, label, frequency Hz, bandwidth Hz, SF)
MODES = [
    ('2.4 GHz', '500 Hz', 2.44e9, 812.5e3, 5),
    ('2.4 GHz', '250 Hz', 2.44e9, 812.5e3, 6),
    ('2.4 GHz', '150 Hz', 2.44e9, 812.5e3, 7),
    ('2.4 GHz', '50 Hz', 2.44e9, 812.5e3, 8),
    ('900 MHz', '200 Hz', 915e6, 500e3, 6),
    ('900 MHz', '100 Hz', 915e6, 500e3, 7),
    ('900 MHz', '50 Hz', 915e6, 500e3, 8),
    ('900 MHz', '25 Hz', 915e6, 500e3, 9),
]

NF_DB = 6.0                      # receiver noise figure (transceiver + matching/diplexer loss)
IMPL_LOSS_DB = 3.0               # demodulator / interference implementation loss vs. the ideal formula
H_PILOT_M, H_DRONE_M = 2.0, 120.0  # antenna heights for the radio-horizon limit
ANT_GAIN_DBI = {'2.4 GHz': 2.0, '900 MHz': 2.0}
FADE_MARGIN_DB = 15.0            # single antenna
DIVERSITY_GAIN_DB = 6.0          # selection diversity, two decorrelated antennas
UPLINK_EIRP_DBM = {'2.4 GHz': 20.0, '900 MHz': 24.0}    # transmitter module: 100 mW / 250 mW
DOWNLINK_TX_DBM = {'2.4 GHz': 12.0, '900 MHz': 20.0}    # receiver telemetry output (transceiver PA, no external PA)


def sensitivity_dbm(bw, sf):
    return -174 + 10 * math.log10(bw) + NF_DB + SNR_MIN[sf] + IMPL_LOSS_DB


def range_km(eirp_dbm, rx_gain_dbi, sens_dbm, freq_hz, margin_db):
    budget = eirp_dbm + rx_gain_dbi - sens_dbm - margin_db       # allowed free-space path loss
    # FSPL(dB) = 20 log10(d_km) + 20 log10(f_MHz) + 32.44
    return 10 ** ((budget - 20 * math.log10(freq_hz / 1e6) - 32.44) / 20)


def horizon_km():
    """Radio horizon with the standard 4/3-earth refraction model."""
    return 4.12 * (math.sqrt(H_PILOT_M) + math.sqrt(H_DRONE_M))


def main():
    hz = horizon_km()
    margin = FADE_MARGIN_DB - DIVERSITY_GAIN_DB
    print(f'fade margin {FADE_MARGIN_DB:g} dB minus {DIVERSITY_GAIN_DB:g} dB diversity gain = {margin:g} dB')
    print(f'{"band":8s} {"mode":7s} {"SF":>3s} {"sens.":>8s} {"control range":>14s} {"telemetry range":>16s}')
    for band, label, f, bw, sf in MODES:
        s = sensitivity_dbm(bw, sf)
        g = ANT_GAIN_DBI[band]
        up = range_km(UPLINK_EIRP_DBM[band], g, s, f, margin)
        down = range_km(DOWNLINK_TX_DBM[band] + g, g, s, f, margin)
        cap = lambda r: f'{min(r, hz):6.1f} km' + ('*' if r > hz else ' ')
        print(f'{band:8s} {label:7s} {sf:>3d} {s:6.1f} dBm {cap(up):>14s} {cap(down):>16s}')
    print(f'* limited by the radio horizon ({hz:.0f} km for {H_PILOT_M:g} m and {H_DRONE_M:g} m antenna heights)')
    print('line of sight, free space: terrain and the airframe will shorten these; telemetry is the shorter link')


if __name__ == '__main__':
    main()
