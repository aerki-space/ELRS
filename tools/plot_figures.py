#!/usr/bin/env python3
"""Regenerate the figures in docs/img from the planning tools.

    python3 tools/plot_figures.py
"""
import math
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'docs', 'img')
sys.path.insert(0, HERE)
import link_budget as lb  # noqa: E402

TARGET_KM = None        # headline range target to mark on the range chart, if any

INK, MUTED, GRID = '#1f2328', '#656d76', '#d0d7de'
BLUE, GREEN, ORANGE, RED, PURPLE = '#0969da', '#1a7f37', '#bf8700', '#cf222e', '#8250df'
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.edgecolor': GRID, 'axes.labelcolor': INK,
    'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.grid': True, 'grid.color': GRID,
    'grid.linewidth': 0.6, 'axes.spines.top': False, 'axes.spines.right': False,
    'figure.facecolor': 'white', 'axes.titleweight': 'bold', 'axes.titlesize': 11,
})


# --- board concept -------------------------------------------------------------
def part(ax, x, y, w, h, label, fc='#1c1f24', tc='white', fs=6.5):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle='round,pad=0,rounding_size=0.15',
                                fc=fc, ec='#0d0f12', lw=0.5, zorder=3))
    if label:
        ax.text(x, y, label, ha='center', va='center', color=tc, fontsize=fs, zorder=4, linespacing=1.05)


def board(ax, title):
    W, H = 17.0, 11.0
    ax.add_patch(FancyBboxPatch((0, 0), W, H, boxstyle='round,pad=0,rounding_size=0.8',
                                fc='#16271d', ec='#0b1610', lw=1.2))
    for i, lab in enumerate(('5V', 'GND', 'TX', 'RX')):          # castellated pads on the short edge
        y = 1.6 + i * 2.6
        ax.add_patch(Rectangle((-0.05, y - 0.6), 1.1, 1.2, fc='#c9a227', ec='none', zorder=3))
        ax.text(1.35, y, lab, fontsize=5.5, color='#c9d1d9', va='center', zorder=4)
    ax.set_title(title, loc='left', fontsize=9.5)
    ax.set_xlim(-1.5, W + 1.5)
    ax.set_ylim(-2.6, H + 0.8)
    ax.set_aspect('equal')
    ax.axis('off')
    return W, H


def fig_board():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.3))
    W, H = board(a1, 'Top: radios, processor, antenna connectors')
    part(a1, 6.4, 5.5, 5.0, 5.0, 'ESP32-C3\nExpressLRS', fs=7)
    part(a1, 11.4, 8.3, 3.9, 3.9, 'LR1121\nradio A', fs=6)
    part(a1, 11.4, 2.7, 3.9, 3.9, 'LR1121\nradio B', fs=6)
    for y in (8.3, 2.7):
        part(a1, 14.35, y + 1.25, 1.2, 1.0, 'DPX', fc='#57606a', fs=3.8)            # diplexer
        part(a1, 15.4, y - 0.6, 2.5, 2.5, 'u.FL', fc='#d0d7de', tc=INK, fs=5.5)
    part(a1, 4.0, 1.4, 1.8, 1.4, 'XTAL', fc='#57606a', fs=4.5)
    a1.annotate('', xy=(0, -1.3), xytext=(W, -1.3), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.8))
    a1.text(W / 2, -1.6, f'{W:g} mm', ha='center', va='top', fontsize=8.5)
    a1.annotate('', xy=(W + 0.9, 0), xytext=(W + 0.9, H), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.8))
    a1.text(W + 1.2, H / 2, f'{H:g} mm', rotation=90, va='center', fontsize=8.5)

    board(a2, 'Back (seen through the board): regulator, TCXOs, passives')
    for gx in np.arange(3.0, 9.6, 0.95):                                 # 0201 decoupling under the processor
        for gy in np.arange(2.6, 8.0, 0.75):
            a2.add_patch(Rectangle((gx, gy), 0.6, 0.3, fc='#bfa36b', ec='none', zorder=3))
    part(a2, 4.0, 9.4, 1.4, 1.4, 'LDO', fc='#57606a', fs=4.5)
    part(a2, 6.2, 9.4, 1.0, 0.6, '', fc='#e5534b')
    a2.text(7.0, 9.4, 'LED', fontsize=5, color='#c9d1d9', va='center', zorder=4)
    for y in (8.3, 2.7):
        part(a2, 11.0, y, 2.0, 1.6, 'TCXO', fc='#57606a', fs=4.5)
        a2.add_patch(Rectangle((12.5, y - 1.6), 3.6, 3.2, fill=False, ec='#8c959f', lw=0.6, ls='--', zorder=4))
        for i in range(3):
            for j in range(2):
                a2.add_patch(Rectangle((12.9 + i * 1.05, y - 0.9 + j * 1.2), 0.6, 0.3, fc='#bfa36b', ec='none',
                                       zorder=3))
        a2.text(14.3, y + (2.0 if y > 5 else -2.0), 'RF matching', fontsize=5, color='#8c959f',
                ha='center', va='center', zorder=4)
    fig.suptitle('Dual-band true-diversity receiver: concept placement', x=0.06, ha='left', fontweight='bold')
    fig.text(0.06, 0.885, '4-layer HDI, ~0.8 mm. Planning sketch from tools/size_estimate.py, not a PCB layout.',
             fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    return fig


# --- range -----------------------------------------------------------------------
def fig_range():
    hz = lb.horizon_km()
    margin = lb.FADE_MARGIN_DB - lb.DIVERSITY_GAIN_DB
    rows = []
    for band, label, f, bw, sf in lb.MODES:
        s = lb.sensitivity_dbm(bw, sf)
        g = lb.ANT_GAIN_DBI[band]
        up = lb.range_km(lb.UPLINK_EIRP_DBM[band], g, s, f, margin)
        down = lb.range_km(lb.DOWNLINK_TX_DBM[band] + g, g, s, f, margin)
        rows.append((f'{band}\n{label}', band, up, down))
    x = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(10, 4.6))
    for off, idx, name, col in ((-0.2, 2, 'control (uplink)', BLUE), (0.2, 3, 'telemetry (downlink)', GREEN)):
        vals = [min(r[idx], hz) for r in rows]
        bars = ax.bar(x + off, vals, width=0.38, color=col, label=name)
        for b, r in zip(bars, rows):
            if r[idx] > hz:
                b.set_hatch('///')
                b.set_edgecolor('white')
    ax.axhline(hz, color=MUTED, ls='--', lw=1)
    ax.text(len(rows) - 0.5, hz + 1, f'radio horizon, {hz:.0f} km (2 m and 120 m antennas)', ha='right',
            va='bottom', fontsize=8, color=MUTED)
    if TARGET_KM:
        ax.axhline(TARGET_KM, color=RED, lw=1.4)
        ax.text(-0.45, TARGET_KM + 1, f'{TARGET_KM} km target', color=RED, fontsize=8.5, fontweight='bold',
                va='bottom')
    ax.axvspan(3.5, 7.5, color='#f6f8fa', zorder=0)
    ax.set_xticks(x, [r[0] for r in rows], fontsize=8.5)
    ax.set_ylabel('line-of-sight range (km)')
    ax.set_ylim(0, hz * 1.15)
    ax.set_title('Range per packet rate, free space, with true diversity')
    ax.legend(frameon=False, loc='upper left')
    ax.grid(axis='x', visible=False)
    fig.text(0.01, -0.02, 'Hatched: free-space budget reaches past the radio horizon. Upper bounds from '
             'tools/link_budget.py; range tests will replace them.', fontsize=7.5, color=MUTED)
    fig.tight_layout()
    return fig


# --- diversity ---------------------------------------------------------------------
def rayleigh_trace(rng, n, fd, fs, paths=32):
    """Sum-of-sinusoids (Jakes-style) Rayleigh fading envelope, power normalised to 1."""
    t = np.arange(n) / fs
    a = rng.uniform(0, 2 * np.pi, paths)
    ph = rng.uniform(0, 2 * np.pi, paths)
    h = np.exp(1j * (2 * np.pi * fd * np.cos(a)[:, None] * t + ph[:, None])).sum(0) / np.sqrt(paths)
    return t, np.abs(h) ** 2


def fig_diversity():
    rng = np.random.default_rng(7)
    fs, n = 20000, 2000
    fd = 20 / (299_792_458 / 2.44e9)           # 20 m/s at 2.4 GHz
    t, pa = rayleigh_trace(rng, n, fd, fs)
    _, pb = rayleigh_trace(rng, n, fd, fs)
    db = lambda p: 10 * np.log10(np.maximum(p, 1e-6))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.0), gridspec_kw=dict(width_ratios=[1.6, 1]))
    a1.plot(t * 1e3, db(pa), color=BLUE, lw=0.9, alpha=0.55, label='antenna A')
    a1.plot(t * 1e3, db(pb), color=ORANGE, lw=0.9, alpha=0.55, label='antenna B')
    a1.plot(t * 1e3, db(np.maximum(pa, pb)), color=INK, lw=1.4, label='true diversity (best of both)')
    a1.set_ylim(-30, 8)
    a1.set_xlim(0, 100)
    a1.set_xlabel('time (ms), drone at 20 m/s, 2.4 GHz')
    a1.set_ylabel('signal relative to mean (dB)')
    a1.set_title('Multipath fades hit each antenna at different times')
    a1.legend(frameon=False, loc='lower right', fontsize=8, ncol=3)

    x = np.logspace(-4, 1, 400)
    single = 1 - np.exp(-x)
    dual = single ** 2
    a2.semilogy(10 * np.log10(x), single, color=BLUE, lw=1.8, label='one antenna')
    a2.semilogy(10 * np.log10(x), dual, color=INK, lw=1.8, label='two antennas, selection')
    for p in (0.1, 0.01):
        s = 10 * math.log10(-math.log(1 - p))
        d = 10 * math.log10(-math.log(1 - math.sqrt(p)))
        a2.annotate('', xy=(d, p), xytext=(s, p), arrowprops=dict(arrowstyle='<->', color=RED, lw=1))
        a2.text(d + 0.8, p, f'{d - s:.0f} dB saved', ha='left', va='center', color=RED, fontsize=8.5)
    a2.set_xlim(-30, 8)
    a2.set_ylim(1e-3, 1)
    a2.set_xlabel('signal relative to mean (dB)')
    a2.set_ylabel('probability of a deeper fade')
    a2.set_title('Fade margin saved')
    a2.legend(frameon=False, loc='lower right', fontsize=8)
    fig.text(0.01, -0.02, 'Rayleigh fading, independent antennas. The link budget assumes 6 dB, the conservative '
             'end, because real antennas on one airframe are partly correlated.', fontsize=7.5, color=MUTED)
    fig.tight_layout()
    return fig


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, make in (('board.png', fig_board), ('range.png', fig_range), ('diversity.png', fig_diversity)):
        fig = make()
        fig.savefig(os.path.join(OUT, name), dpi=160, bbox_inches='tight')
        plt.close(fig)
        print('wrote', os.path.join('docs', 'img', name))


if __name__ == '__main__':
    main()
