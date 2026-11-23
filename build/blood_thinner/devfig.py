# the full device as it sits in live: the macro rack (left) and the eq eight inside it (right) · 832 x 238, laid out after a screenshot of the preset
def device_full(INK, INK2, MUTE, PANEL, FIELD, LINE, R, P, O, DARK, curve_pts_fn):
    PU, CY = 'var(--cA46BE8)', 'var(--c2FB8C6)'
    M = 'font-family="Roboto Mono, monospace"'; S = 'font-family="Archivo, sans-serif"'
    s = ['<svg class="mmfig" viewBox="0 0 832 238" role="img" aria-label="the blood_thinner rack and eq eight as they look in ableton live">']
    def rect(x, y, w, h, fill, stroke=None, rx=2):
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"' + (f' stroke="{stroke}"' if stroke else '') + '/>')
    def text(x, y, t, fs=9, fill=INK, anchor='start', w=500, font=M):
        s.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" {font} font-size="{fs}" font-weight="{w}" fill="{fill}">{t}</text>')
    def knob(cx, cy, r, frac, col=INK):
        import math
        a0, a1 = math.radians(225), math.radians(-45)
        p = lambda a: (cx + r * math.cos(a), cy - r * math.sin(a))
        x0, y0 = p(a0); x1, y1 = p(a1)
        s.append(f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 1 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{LINE}" stroke-width="3"/>')
        if frac > 0.001:
            a = a0 + (a1 - a0) * frac; xa, ya = p(a); large = 1 if (a0 - a) > math.pi else 0
            s.append(f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 {large} 1 {xa:.1f} {ya:.1f}" fill="none" stroke="{col}" stroke-width="3"/>')
        a = a0 + (a1 - a0) * frac; xa, ya = p(a)
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{xa:.1f}" y2="{ya:.1f}" stroke="{col}" stroke-width="2"/>')
    # ---- rack
    rect(0, 0, 218, 238, PANEL, LINE, 4)
    rect(0, 0, 218, 22, FIELD, None, 4)
    s.append(f'<circle cx="12" cy="11" r="6" fill="{R}"/>'); text(24, 15, '[ blood_thin…', 10, INK, w=700)
    for i, t in enumerate(['R', 'M']):
        s.append(f'<circle cx="{138 + i * 16}" cy="11" r="6.5" fill="{LINE}"/>'); text(138 + i * 16, 14.5, t, 8.5, INK, 'middle', 700)
    for i in range(3): s.append(f'<circle cx="{172 + i * 15}" cy="11" r="5.5" fill="{LINE}"/>')
    for i in range(5): s.append(f'<circle cx="12" cy="{38 + i * 22}" r="6" fill="{R if i in (0, 3) else LINE}"/>')
    cells = [('L_shelf', '- / +', '-5.00 dB', PU, .33), ('H_shelf', '- / +', '0.00 dB', CY, .5), ('hi_pass', 'freq', '180 Hz', P, .58),
             ('L : shelf', 'freq', '640 Hz', PU, .55), ('H : shelf', 'freq', '5.00 kHz', CY, .62), ('intensity', '', '100 %', O, .5)]
    for i, (a, b, val, col, fr) in enumerate(cells):
        x = 28 + (i % 3) * 62; y = 28 + (i // 3) * 104
        rect(x, y, 58, 100, FIELD)
        rect(x + 2, y + 2, 54, 30, col)
        text(x + 29, y + 15, a, 8.5, DARK, 'middle', 700); text(x + 29, y + 26, b, 8.5, DARK, 'middle', 600)
        knob(x + 29, y + 60, 15, fr)
        text(x + 29, y + 92, val, 8.5, INK, 'middle')
    # ---- eq eight
    X0 = 224
    rect(X0, 0, 608, 238, PANEL, LINE, 4)
    rect(X0, 0, 608, 22, FIELD, None, 4)
    s.append(f'<circle cx="{X0 + 12}" cy="11" r="6" fill="{R}"/>'); text(X0 + 24, 15, '[ blood_thinner ]', 10, INK, w=700)
    for i in range(3): s.append(f'<circle cx="{X0 + 560 + i * 15}" cy="11" r="5.5" fill="{LINE}"/>')
    # left knobs (selected band: 4)
    for i, (lab, val, fr) in enumerate([('Freq', '5.00 kHz', .78), ('Gain', '0.00 dB', .5), ('Q', '0.71', .2)]):
        y = 30 + i * 68
        text(X0 + 32, y + 8, lab, 9, INK, 'middle', 600, S)
        knob(X0 + 32, y + 30, 14, fr)
        text(X0 + 32, y + 58, val, 8.5, INK, 'middle')
    # display
    DX, DY, DW, DH = X0 + 62, 26, 448, 160
    rect(DX, DY, DW, DH, FIELD)
    for k, d in enumerate([12, 6, 0, -6, -12]):
        yy = DY + 12 + k * 33
        s.append(f'<line x1="{DX + 28}" x2="{DX + DW}" y1="{yy}" y2="{yy}" stroke="{LINE}" stroke-width=".8"/>')
        text(DX + 16, yy + 3, str(d), 8.5, INK2, 'middle')
    import math
    fx = lambda f: DX + 28 + (math.log10(f) - math.log10(20)) / 3 * (DW - 28)
    for f, t in ((100, '100'), (1000, '1k'), (10000, '10k')):
        s.append(f'<line x1="{fx(f):.1f}" x2="{fx(f):.1f}" y1="{DY}" y2="{DY + DH}" stroke="{LINE}" stroke-width=".8"/>')
        text(fx(f), DY + DH - 4, t, 8.5, INK2, 'middle')
    dy = lambda d: DY + 12 + (12 - d) / 24 * 132
    pts = curve_pts_fn(fx, dy, DY + DH)
    s.append(f'<clipPath id="btd"><rect x="{DX + 28}" y="{DY}" width="{DW - 28}" height="{DH}"/></clipPath>')
    s.append(f'<polyline clip-path="url(#btd)" points="{pts}" fill="none" stroke="{O}" stroke-width="1.8"/>')
    # bands row
    for i in range(8):
        x = DX + i * 56
        on = i in (0, 1, 3)
        rect(x + 2, DY + DH + 4, 52, 16, LINE)
        text(x + 28, DY + DH + 16, ['HP48', 'LS', 'bell', 'HS', 'bell', 'bell', 'bell', 'LP'][i], 8, INK, 'middle')
        rect(x + 8, DY + DH + 25, 10, 10, O if on else FIELD, None if on else MUTE, 1)
        text(x + 30, DY + DH + 34, str(i + 1), 9, INK, 'middle', 600)
    # right column
    RX = X0 + 520
    rect(RX + 6, 28, 22, 16, LINE); rect(RX + 32, 28, 22, 16, R)
    for j, (lab, val, hi) in enumerate([('Mode', 'Stereo', False), ('Edit', 'L', False), ('Adapt. Q', 'On', True), ('Scale', '100 %', False), ('Output', '0.00 dB', False)]):
        y = 56 + j * 34
        text(RX + 6, y + 8, lab, 9, INK, 'start', 700, S)
        rect(RX + 6, y + 12, 74, 15, R if hi else FIELD)
        text(RX + 43, y + 23, val, 8.5, DARK if hi else INK, 'middle')
    s.append('</svg>')
    return ''.join(s)
