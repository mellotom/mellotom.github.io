# builds the [ blood_thinner ] page (mellotom.music/blood-thinner/) as a travelers guide sheet
# usage: python3 build/blood_thinner/gen.py ../dvca-navigator/index.html blood-thinner/index.html
import re, sys, math, datetime
tpl = open(sys.argv[1], encoding='utf-8').read()
out = sys.argv[2]
REV = datetime.date.today().strftime('%Y.%m')
import json, os
GUMROAD = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gumroad.json'), encoding='utf-8'))['blood_thinner']
TITLE = '[ blood_thinner ] · free eq eight preset by mellotom'
U = 'color: inherit; text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 2px'
INK, INK2, MUTE = 'var(--cF2F2F0)', 'var(--cD0D0CC)', 'var(--c96968F)'
BG, PANEL, FIELD, LINE = 'var(--c0E0E0F)', 'var(--c171718)', 'var(--c2A2A2B)', 'var(--c3A3A3B)'
R, P, O, B, Y, G, DARK = 'var(--cE5484D)', 'var(--cE83E8C)', 'var(--cF28A2A)', 'var(--c3FA7E0)', 'var(--cE8C534)', 'var(--c2FB36A)', 'var(--c111112)'
STRIPES = [R, P, O, B, 'var(--cE6E6E3)']

head = tpl[:tpl.find('<div id="frame">')]
head = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', head, count=1)
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="[ blood_thinner ]: a free ableton eq eight preset that clears low-end build-up on any track, with six macros for quick tone shaping and five eq bands left free.">', head, count=1)
head = head.replace('</style>', '.mmfig{display:block;width:100%;height:auto}.mmbtn{display:inline-flex;align-items:center;gap:8px;font-family:\'Roboto Mono\',monospace;font-weight:600;font-size:12px;padding:8px 12px;border:1.5px solid var(--cF2F2F0);color:var(--cF2F2F0);text-decoration:none}.mmbtn.go{background:var(--cE5484D);border-color:var(--cE5484D);color:var(--c111112)}.mmbtn:hover{border-color:var(--cF28A2A);color:var(--cF28A2A)}.mmbtn.go:hover{background:var(--cF28A2A);border-color:var(--cF28A2A);color:var(--c111112)}.mmacts{display:flex;flex-wrap:wrap;gap:8px}.btp{font-family:\'Archivo\',sans-serif;font-size:13.5px;line-height:1.5;color:var(--cD0D0CC);margin:6px 0 0}.btp b{color:var(--cF2F2F0)}@media screen and (max-width: 899px){.btdev .mmfig{width:100%}.btdev div[style*="width: 832px"]{width:auto!important;flex:1 1 auto!important}.btdev div[style*="display: flex; gap: 28px"]{flex-direction:column}}html.tall .btdev div[style*="width: 832px"]{width:auto!important;flex:1 1 auto!important}html.tall .btdev div[style*="display: flex; gap: 28px"]{flex-direction:column}@media screen and (max-width: 899px){.btdev{grid-column:auto!important;grid-row:auto!important}}html.tall .btdev{grid-column:1 / -1!important;grid-row:auto!important}@media screen and (max-width: 899px){h1.m-h1.long{font-size:min(44px,9.4vw)!important}}\n</style>', 1)
tail = tpl[tpl.find('</footer>') + len('</footer>'):]

def sec(n, col, title, sc, body):
    return (f'<section class="sec"><div class="sh"><span class="sn" style="background: {col}; color: {DARK}">{n:02d}</span>'
            f'<h2 class="st">{title}</h2><span class="sc">{sc}</span></div>{body}</section>')
def r(k, a): return f'<div class="r"><div class="kc">{k}</div><div class="a">{a}</div></div>'
def v(t): return f'<span class="v">{t}</span>'
def nm(t): return f'<span class="nm">{t}</span>'
def b(t): return f'<span class="b">[ {t} ]</span>'
def para(*ps): return ''.join(f'<p class="btp">{p}</p>' for p in ps)
def figsec(title, sc, svg):
    return (f'<section class="sec" style="gap: 8px"><div style="display: flex; justify-content: space-between; align-items: baseline; border-top: 4px solid {INK}; padding-top: 6px">'
            f'<span style="font-family: \'Archivo\', sans-serif; font-weight: 900; font-size: 20px; letter-spacing: -.015em">{title}</span><span class="sc">{sc}</span></div>{svg}</section>')
MONO = 'font-family="Roboto Mono, monospace"'; SANS = 'font-family="Archivo, sans-serif"'

# ---- the default curve, from the preset's settings: 48 dB/oct high pass at 180 Hz, low shelf -5 dB at 640 Hz, high shelf 0 dB at 5 kHz
def shelf_db(f, f0, gain_db, low=True):
    # rbj shelf, slope 1, evaluated on the unit circle at 48 kHz
    fs = 48000.0; A = 10 ** (gain_db / 40); w0 = 2 * math.pi * f0 / fs; cw, sw = math.cos(w0), math.sin(w0)
    al = sw / 2 * math.sqrt(2); sA = 2 * math.sqrt(A) * al
    if low:
        b0 = A * ((A + 1) - (A - 1) * cw + sA); b1 = 2 * A * ((A - 1) - (A + 1) * cw); b2 = A * ((A + 1) - (A - 1) * cw - sA)
        a0 = (A + 1) + (A - 1) * cw + sA; a1 = -2 * ((A - 1) + (A + 1) * cw); a2 = (A + 1) + (A - 1) * cw - sA
    else:
        b0 = A * ((A + 1) + (A - 1) * cw + sA); b1 = -2 * A * ((A - 1) + (A + 1) * cw); b2 = A * ((A + 1) + (A - 1) * cw - sA)
        a0 = (A + 1) - (A - 1) * cw + sA; a1 = 2 * ((A - 1) - (A + 1) * cw); a2 = (A + 1) - (A - 1) * cw - sA
    w = 2 * math.pi * f / fs; z1 = complex(math.cos(w), -math.sin(w)); z2 = z1 * z1
    return 20 * math.log10(abs((b0 + b1 * z1 + b2 * z2) / (a0 + a1 * z1 + a2 * z2)))
def hp_db(f, fc, order=8):
    return -10 * math.log10(1 + (fc / f) ** (2 * order))
def curve():
    W, H, L, T, Rt, Bt = 400, 230, 34, 10, 6, 26
    fmin, fmax, dmin, dmax = 20, 20000, -18, 9
    X = lambda f: L + (math.log10(f) - math.log10(fmin)) / (math.log10(fmax) - math.log10(fmin)) * (W - L - Rt)
    Yd = lambda d: T + (dmax - d) / (dmax - dmin) * (H - T - Bt)
    s = [f'<svg class="mmfig" viewBox="0 0 {W} {H}" role="img" aria-label="the default blood_thinner curve">', f'<rect x="{L}" y="{T}" width="{W - L - Rt}" height="{H - T - Bt}" fill="{FIELD}"/>']
    for d in (6, 0, -6, -12):
        s.append(f'<line x1="{L}" x2="{W - Rt}" y1="{Yd(d):.1f}" y2="{Yd(d):.1f}" stroke="{LINE}"/><text x="{L - 5}" y="{Yd(d) + 3.5:.1f}" text-anchor="end" {MONO} font-size="9.5" fill="{MUTE}">{d:+d}</text>'.replace('+0', '0'))
    for f, t in ((100, '100'), (1000, '1k'), (10000, '10k')):
        s.append(f'<line x1="{X(f):.1f}" x2="{X(f):.1f}" y1="{T}" y2="{H - Bt}" stroke="{LINE}"/><text x="{X(f):.1f}" y="{H - 10}" text-anchor="middle" {MONO} font-size="9.5" fill="{MUTE}">{t} Hz</text>')
    pts = []
    for i in range(0, 241):
        f = fmin * (fmax / fmin) ** (i / 240)
        d = hp_db(f, 180) + shelf_db(f, 640, -5) + shelf_db(f, 5000, 0, low=False)
        d = max(d, dmin - 2)
        pts.append(f'{X(f):.1f},{Yd(d):.1f}')
    s.append(f'<clipPath id="btc"><rect x="{L}" y="{T}" width="{W - L - Rt}" height="{H - T - Bt}"/></clipPath>')
    s.append(f'<polyline clip-path="url(#btc)" points="{" ".join(pts)}" fill="none" stroke="{R}" stroke-width="2.5"/>')
    for f, d, n in ((180, hp_db(180, 180) + shelf_db(180, 640, -5), 1), (640, hp_db(640, 180) + shelf_db(640, 640, -5), 2), (5000, 0, 4)):
        s.append(f'<circle cx="{X(f):.1f}" cy="{Yd(d):.1f}" r="8" fill="{R}"/><text x="{X(f):.1f}" y="{Yd(d) + 3.5:.1f}" text-anchor="middle" {MONO} font-weight="700" font-size="10" fill="{DARK}">{n}</text>')
    s.append('</svg>')
    return ''.join(s)
def macros():
    # the six macros as they sit on the rack
    cells = [('L_shelf', '- / +', '-5.00 dB', 'var(--cA46BE8)'), ('H_shelf', '- / +', '0.00 dB', 'var(--c2FB8C6)'), ('hi_pass', 'freq', '180 Hz', P),
             ('L : shelf', 'freq', '640 Hz', 'var(--cA46BE8)'), ('H : shelf', 'freq', '5.00 kHz', 'var(--c2FB8C6)'), ('intensity', '', '100 %', O)]
    W, cw, ch, gap = 400, 124, 98, 14
    s = [f'<svg class="mmfig" viewBox="0 0 {W} {2 * ch + gap}" role="img" aria-label="the six blood_thinner macros at their defaults">']
    for i, (a, bb, val, col) in enumerate(cells):
        x = (i % 3) * (cw + (W - 3 * cw) / 2); y = (i // 3) * (ch + gap)
        s.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="3" fill="{PANEL}" stroke="{LINE}"/>')
        s.append(f'<rect x="{x + 4}" y="{y + 4}" width="{cw - 8}" height="30" rx="2" fill="{col}"/>')
        s.append(f'<text x="{x + 28}" y="{y + 17}" {MONO} font-weight="700" font-size="11" fill="{DARK}">{a}</text><text x="{x + 28}" y="{y + 29}" {MONO} font-size="10" fill="{DARK}">{bb}</text>')
        cx, cy = x + cw / 2, y + 60
        s.append(f'<path d="M{cx - 13:.1f} {cy + 9:.1f} A16 16 0 1 1 {cx + 13:.1f} {cy + 9:.1f}" fill="none" stroke="{INK}" stroke-width="3"/>')
        s.append(f'<text x="{cx}" y="{y + ch - 8}" text-anchor="middle" {MONO} font-size="11" fill="{INK}">{val}</text>')
        s.append(f'<rect x="{x + 8}" y="{y + 11}" width="16" height="16" rx="2" fill="{DARK}"/><text x="{x + 16}" y="{y + 23}" text-anchor="middle" {MONO} font-weight="700" font-size="10.5" fill="{INK}">{i + 1}</text>')
    s.append('</svg>')
    return ''.join(s)
def waves():
    W = 400
    rows = [('100 Hz', '11.3 ft · 3.4 m', 1.0), ('1 kHz', '1.1 ft · 0.34 m', 0.1), ('10 kHz', '1.35 in · 3.4 cm', 0.01)]
    s = [f'<svg class="mmfig" viewBox="0 0 {W} 150" role="img" aria-label="the length of one wave at 100 hz, 1 khz and 10 khz">']
    for i, (f, lab, k) in enumerate(rows):
        y = 26 + i * 46; w = max(2.0, 330 * k)
        s.append(f'<text x="0" y="{y - 8}" {MONO} font-size="10.5" font-weight="700" fill="{INK}">{f}</text><text x="{W}" y="{y - 8}" text-anchor="end" {MONO} font-size="10" fill="{MUTE}">{lab}</text>')
        if w > 20:
            pts = ' '.join(f'{(i2 / 80) * w:.1f},{y + 10 - 9 * math.sin(2 * math.pi * i2 / 80):.1f}' for i2 in range(81))
            s.append(f'<polyline points="{pts}" fill="none" stroke="{R}" stroke-width="2.2"/>')
        else:
            s.append(f'<rect x="0" y="{y + 1}" width="{w:.1f}" height="18" fill="{R}"/>')
        s.append(f'<line x1="0" x2="{W}" y1="{y + 10}" y2="{y + 10}" stroke="{LINE}" stroke-dasharray="2 3"/>')
    s.append(f'<text x="0" y="146" {MONO} font-size="9.5" fill="{MUTE}">one full wave, to scale · each 10× up in frequency is 10× shorter</text></svg>')
    return ''.join(s)

import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'devfig.py'), encoding='utf-8').read())
def _pts(fx, dy, bottom):
    out = []
    for i in range(0, 241):
        f = 20 * 1000 ** (i / 240)
        d = hp_db(f, 180) + shelf_db(f, 640, -5) + shelf_db(f, 5000, 0, low=False)
        out.append(f'{fx(f):.1f},{min(dy(max(d, -40)), bottom):.1f}')
    return ' '.join(out)
DEVICE = device_full(INK, INK2, MUTE, PANEL, FIELD, LINE, R, P, O, DARK, _pts)
devrow = ('<div class="btdev" style="grid-column: 1 / span 4; grid-row: 2; align-self: end">'
          + figsec('__fig.05 : the device', 'the rack + its eq eight, as they load in live', f'<div style="display: flex; gap: 28px; align-items: flex-start"><div style="flex: none; width: 832px; border: 1px solid {INK}; padding: 12px; background: {BG}">{DEVICE}</div><div style="min-width: 0; font-family: Archivo, sans-serif; font-size: 13px; line-height: 1.5; color: {INK2}"><p style="margin: 0 0 8px"><b style="color: {INK}">1:1</b> · every control where it sits in live, at its default</p><p style="margin: 0 0 8px"><b style="color: {INK}">left</b> · the rack and its six macros</p><p style="margin: 0 0 8px"><b style="color: {INK}">right</b> · the eq eight inside it · bands 1, 2 and 4 on · band 4 selected</p><p style="margin: 0"><b style="color: {INK}">free</b> · bands 3, 5, 6, 7 and 8 are off and ready for you</p></div></div>') + '</div>')
c1 = ''.join([
 sec(1, R, 'what it is', 'bt_01', ''.join([
   r(v('an eq eight preset'), 'an audio effect rack around ableton’s stock eq eight, with six macros'),
   r(v('one job'), 'stop low frequencies from piling up on every track'),
   r(v('quick'), 'six macros for fast tone shaping'),
   r(v('room to grow'), 'five eq bands left free for anything else'),
   r(v('price'), 'free · name your price if you want to'),
 ])),
 sec(2, R, 'where it goes', 'bt_02 · first in the chain', ''.join([
   r(v('almost every track'), 'at any stage of writing, not only at mix time'),
   r(v('position'), 'straight after the sound source · before any reverb, delay or other time-based effect'),
   r(v('kick + bass'), f'turn off band {nm(1)} the high pass on these · keep the shelves'),
   r(v('first move'), f'sweep {nm(3)} {b("hi_pass freq")} up until the sound thins, then back it off a touch'),
 ])),
 sec(3, P, 'install', 'bt_03', ''.join([
   r(v('download'), f'<a href="{GUMROAD}" target="_blank" rel="noopener" style="{U}">get the preset</a> · free, with a name-your-price option'),
   r(v('use it'), 'drag the file onto any audio track'),
   r(v('keep it'), 'drop it into your user library so it sits in live’s browser'),
 ])),
])
c2 = ''.join([
 sec(4, P, 'the macros', 'bt_04 · fig.02', ''.join([
   r(nm(1) + ' ' + v('low shelf'), b('L_shelf') + ' · boost or cut · ±15 dB · default −5 dB'),
   r(nm(4) + ' ' + v('low freq'), b('L : shelf freq') + ' · where the low shelf sits · default 640 Hz · sweep it for mud above 250 Hz the high pass can’t reach'),
   r(nm(3) + ' ' + v('high pass'), b('hi_pass freq') + ' · cutoff · 20–250 Hz · default 180 Hz'),
   r(nm(2) + ' ' + v('high shelf'), b('H_shelf') + ' · boost or cut · default 0 dB, so it does nothing until you turn it'),
   r(nm(5) + ' ' + v('high freq'), b('H : shelf freq') + ' · where the high shelf sits · default 5 kHz'),
   r(nm(6) + ' ' + v('intensity'), b('intensity') + ' · scales every boost and cut · 0–200 % · default 100 %'),
 ])),
 figsec('__fig.02 : the macros', 'defaults', macros()),
])
c3 = ''.join([
 sec(6, O, 'the defaults', 'bt_06 · as it loads', ''.join([
   r(v('band 1'), 'high pass · 48 dB/oct · 180 Hz'),
   r(v('band 2'), 'low shelf · −5 dB · 640 Hz'),
   r(v('band 4'), 'high shelf · 0 dB · 5 kHz · q 0.71'),
   r(v('bands 3 5 6 7 8'), 'off · yours to use'),
   r(v('mode'), 'stereo · adaptive q on · output 0 dB'),
 ])),
 sec(5, O, 'intensity', 'bt_05 · ' + nm(6), ''.join([
   r(v('what it moves'), 'eq eight’s scale control · 0 % = flat, 200 % = twice every shelf'),
   r(v('not the high pass'), 'the high pass has no gain, so intensity never changes it'),
   r(v('use it'), 'one knob to take the whole curve harder or softer once it’s set'),
 ])),
 sec(7, B, 'wide moves on purpose', 'bt_07 · why shelves', ''.join([
   r(v('broad strokes'), 'shelves and a high pass move whole regions, not narrow slices'),
   r(v('transparent'), 'gentle, wide curves change the balance of a sound without giving it a new character'),
   r(v('fast'), 'set it in seconds on every track, then move on'),
   r(v('surgery'), 'save narrow cuts for the five free bands'),
 ])),
])
c4 = ''.join([
 sec(8, B, 'why the low end', 'bt_08 · in short', ''.join([
   r(v('everything has it'), 'samples from big sample sites and instrument presets carry low end'),
   r(v('made to sell'), 'they’re tuned to sound great on their own · in a mix nothing plays on its own'),
   r(v('it adds up'), 'every pre-hyped sound brings its own low end, and it stacks'),
   r(v('headroom'), 'most of a mix’s headroom goes to the low end'),
   r(v('your bus'), 'mix compressors and limiters react to it long before a high frequency ever reaches the gain reduction meter'),
 ])),
 figsec('__fig.04 : how big a wave is', 'speed of sound ≈ 343 m/s', waves()),
 sec(9, Y, 'the send problem', 'bt_09 · reverb + delay', ''.join([
   r(v('stacked'), 'send several channels to one reverb or delay and their low end adds together'),
   r(v('smeared'), 'then it’s spread across time and the stereo field'),
   r(v('fix'), 'blood_thinner before the send keeps it out of the effect'),
 ])),
])
WHY = para(
 '<b>[ blood_thinner ] is my go-to eq preset.</b> it goes on nearly every track i make, at every stage of writing. it has one job: stop low frequencies building up, with a few quick controls for tone shaping, while leaving five eq bands free for anything else.',
 'almost every sound you load into a daw carries low end, especially samples from big sample sites and instrument presets. they’re made to sound great on their own, because that’s what sells them. in a mix nothing plays on its own: every element arrives pre-hyped, and all that low end piles up.',
 'low frequencies are physically big. a 100 Hz wave is about 11.3 ft (3.4 m) long, 1 kHz is just over 1 ft (0.34 m), and 10 kHz is 1.35 in (3.4 cm). every 10× up in frequency makes the wave 10× smaller and easier for a speaker to produce. leave the extra low end in and your monitors and sub spend their effort on it, and your mix compressors and limiters react to it long before a high frequency ever touches the gain reduction meter.',
 'sends make it worse. feed several channels into a reverb or delay and their low end adds up, then gets smeared across time and the stereo field.',
 'so blood_thinner goes first: straight after the sound source, before any time-based effect. i used to load a stock eq eight and draw this curve by hand on almost every track. now it’s one preset.')
panel = (f'<div class="m-panel" style="grid-row: 1 / span 2; display: flex; flex-direction: column; background: {PANEL}; color: {INK}; border: 2px solid {INK}; padding: 0 26px 18px; min-width: 0; min-height: 0">'
 '<div style="display: flex; flex-direction: column; gap: 2px; margin: 0 -26px 12px" aria-hidden="true">' + ''.join(f'<div style="height: 4px; background: {c}"></div>' for c in STRIPES) + '</div>'
 f'<div style="display: flex; justify-content: space-between; align-items: baseline"><span style="font-family: \'Archivo\', sans-serif; font-weight: 900; font-size: 27px; line-height: 1; letter-spacing: -.02em">__fig.01 : in my words</span><span class="sc">why it exists</span></div>'
 f'<div style="margin-top: 6px">{WHY}</div><div style="height: 16px"></div>' + figsec('__fig.03 : the default curve', 'drawn from the preset’s settings', curve()) + '<div style="flex: 1"></div>'
 f'<section class="sec" style="gap: 10px; margin-top: 14px"><div class="sh"><span class="sn" style="background: {R}; color: {DARK}">10</span><h2 class="st">get it</h2><span class="sc">bt_10 · free</span></div>'
 f'<div class="mmacts"><a class="mmbtn go" href="{GUMROAD}" target="_blank" rel="noopener">free download</a><a class="mmbtn" href="https://buymeacoffee.com/mellotom" target="_blank" rel="noopener">buy me a coffee</a></div></section>'
 '</div>')

crops = ''.join(f'<div class="crop" style="{p}" aria-hidden="true"></div>' for p in [
 f'top: 24px; left: 24px; border-top: 2px solid {INK}; border-left: 2px solid {INK}', f'top: 24px; right: 24px; border-top: 2px solid {INK}; border-right: 2px solid {INK}',
 f'bottom: 24px; left: 24px; border-bottom: 2px solid {INK}; border-left: 2px solid {INK}', f'bottom: 24px; right: 24px; border-bottom: 2px solid {INK}; border-right: 2px solid {INK}'])
ticks = ''.join(f'<div class="m-hide" style="position: absolute; {side}: 26px; top: 360px; bottom: 120px; width: 14px; background: repeating-linear-gradient(to bottom, {INK} 0 2px, transparent 2px 28px)" aria-hidden="true"></div>' for side in ('left', 'right'))
ARROW = '<svg width="14" height="9" viewBox="0 0 14 9" aria-hidden="true" style="display: block; flex: none"><path d="M13.2 4.5 H1.6 M5.1 1 L1.6 4.5 L5.1 8" fill="none" stroke="currentColor" stroke-width="1.3"></path></svg>'
def stat(n, lab, acc=False):
    return (f'<div style="padding: 7px 10px; border-right: 2px solid {INK}; border-bottom: 2px solid {INK}; display: flex; align-items: baseline; gap: 10px">'
            f'<span style="font-family: \'Archivo\', sans-serif; font-weight: 900; font-size: 30px; line-height: 1; letter-spacing: -.02em; color: {R if acc else INK}">{n}</span>'
            f'<span style="font-family: \'Roboto Mono\', monospace; font-size: 10px; color: {MUTE}; white-space: nowrap">{lab}</span></div>')
header = f'''<header style="padding-top: 30px; display: flex; flex-direction: column; gap: 14px">
<div class="m-slugs" style="display: flex; justify-content: space-between; font-family: 'Roboto Mono', monospace; font-size: 10.5px; line-height: 1.45; color: {INK}">
<div style="display: flex; flex-direction: column"><span style="font-weight: 600">blood_thinner ................. 00.00_02</span><span>eq eight preset ..... <a href="{GUMROAD}" target="_blank" rel="noopener" style="{U}">free download</a></span></div>
<div class="tm-line" style="display: flex; flex-direction: column; align-items: center"><span><a class="tm" href="/tools/" style="display: inline-flex; align-items: center; gap: 5px">{ARROW}<span>back to free tools</span></a></span><span>mode ....................... <button type="button" class="tm" data-t="alt" aria-pressed="false">light</button>/<button type="button" class="tm" data-t="native" aria-pressed="false">dark</button></span><span class="vw-line">view ............. <button type="button" class="tm" data-v="sheet" aria-pressed="false">sheet</button>/<button type="button" class="tm" data-v="scroll" aria-pressed="false">scroll</button></span></div>
<div style="display: flex; flex-direction: column; text-align: right; position: relative"><span>made by ................ <a href="https://linktr.ee/mellotom" target="_blank" rel="noopener" style="{U}">mellotom</a></span><span>rev ............................ {REV}</span><span class="gc" data-l="40" style="position: absolute; right: 0; top: 100%; white-space: nowrap; visibility: hidden">visitors</span></div>
</div>
<div class="m-hgrid" style="display: grid; grid-template-columns: minmax(0, 1fr) 720px; gap: 56px; align-items: end">
<div style="display: flex; flex-direction: column; gap: 12px; min-width: 0">
<div class="m-titlerow" style="display: flex; align-items: flex-end; gap: 28px">
<h1 class="m-h1 long" style="margin: 0; font-family: 'Archivo', sans-serif; font-weight: 900; font-size: 116px; line-height: .8; letter-spacing: -.035em; white-space: nowrap">[ blood_thinner ]</h1>
<div class="m-sub mmacts" style="padding-bottom: 6px; gap: 10px"><a class="mmbtn go" style="font-size: 17px; padding: 12px 18px" href="{GUMROAD}" target="_blank" rel="noopener">free download</a></div>
</div>
<div class="ttlbar" style="height: 14px; background: {INK}"></div>
</div>
<div style="display: flex; flex-direction: column; gap: 10px">
<div class="stx" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); border-top: 2px solid {INK}; border-left: 2px solid {INK}">{stat('180', 'Hz high pass by default', True)}{stat('6', 'macros')}{stat('5', 'eq bands left free')}</div>
<div style="display: flex; flex-wrap: wrap; gap: 6px 18px; font-family: 'Roboto Mono', monospace; font-size: 11px; color: {INK2}; align-items: baseline"><span>[ name ] = a macro on the rack</span><span>numbers = fig.02</span><span>ableton eq eight</span></div>
</div>
</div>
</header>'''
stripes = '<div class="m-stripes" style="display: flex; flex-direction: column; gap: 3px; margin: 16px -64px 0" aria-hidden="true">' + ''.join(f'<div style="height: 3px; background: {c}"></div>' for c in STRIPES + [INK]) + '</div>'
strip = f'<div class="m-strip" style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid {INK}; font-family: \'Roboto Mono\', monospace; font-size: 10.5px; color: {MUTE}"><span>clears low-end build-up on any track · high pass + two shelves on six macros · first in the chain, before reverb and delay</span><span></span><span></span></div>'
grid = ('<div class="m-grid" style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)) minmax(0, 1.55fr); gap: 28px; padding-top: 14px; align-items: stretch; flex: 1; min-height: 0">'
        + ''.join(f'<div class="col" style="align-self: stretch">{c}</div>' for c in (c1, c2, c3, c4)) + panel + devrow + '</div>')
footer = f'''<footer class="m-footer" style="margin-top: 12px; margin-bottom: 24px; height: 50px; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)) minmax(0, 1.55fr); column-gap: 28px; font-family: 'Roboto Mono', monospace; font-size: 10.5px; line-height: 1.5; color: {MUTE}">
<div style="grid-column: 1 / span 4; border-top: 4px solid {INK}; display: flex; align-items: center"><span>design homage to the <a href="https://www.marvel.com/comics/guides/1556/house-of-xpowers-of-x" target="_blank" rel="noopener" style="{U}">house of x / powers of x</a> data pages — designed by tom muller with jonathan hickman<br>not affiliated with ableton or marvel</span></div>
<div style="display: flex; flex-direction: column; align-items: flex-end; justify-content: center; padding-top: 4px; color: {INK}; white-space: nowrap"><span style="display: block">conceived by&nbsp;<a href="https://linktr.ee/mellotom" target="_blank" rel="noopener" style="{U}">mellotom</a>&nbsp;· blood_thinner ... 00.00_02</span><span style="display: block; opacity: .62"><a href=https://mellotom.music/ai-usage-disclaimer/ style=color:inherit;text-underline-offset:2px>AI Usage Disclaimer</a></span></div>
</footer>'''
sheet = (f'<div id="frame">\n<div id="sheet" style="position: absolute; top: 0; left: 0; width: 2560px; height: 1440px; transform-origin: 0 0; box-sizing: border-box; background: {BG}; color: {INK}; display: flex; flex-direction: column; padding: 0 64px">\n'
         + crops + ticks + header + stripes + strip + grid + footer)
open(out, 'w', encoding='utf-8').write(head + sheet + tail)
print('ok')
