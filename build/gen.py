# builds the mellotom.music root page from the welcome center's styles
# usage: python3 gen.py <travelers-guide/index.html> <out.html>
import sys, re, random
src = open(sys.argv[1], encoding='utf-8').read().split('\n')
line10 = src[9]
root_vars = re.match(r'<style>(:root\{[^}]*\}html\[data-theme="light"\]\{[^}]*\})', line10).group(1)
tm_css = line10[line10.index('.tm{'):]
base_css = '\n'.join(src[10:101])          # lines 11-101: layout, card, footer, mobile
theme_js = src[656]
import os
_logo = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo.svg'), encoding='utf-8').read()
_inner = _logo[_logo.index('<g>'):_logo.rindex('</g>') + 4]
_inner = re.sub(r'\s*affinity:id="[^"]*"', '', _inner)
_inner = re.sub(r'\s*id="[^"]*"', '', _inner)
_inner = re.sub(r'>\s+<', '><', _inner)
# viewBox = the outline's bounding box (measured in a browser) plus 2px each side
LOGO = f'<svg class="logo-svg" viewBox="196.8 277.3 1519.8 339.6" fill="currentColor" aria-hidden="true" focusable="false">{_inner}</svg>'                         # line 657: light/dark toggle
# chance backgrounds (starry sky, aurora, rain): css rules, the picker script and the rain engine
_all_css = ''.join(re.findall(r'<style[^>]*>(.*?)</style>', '\n'.join(src), flags=re.S))
_rules, _depth, _start = [], 0, 0
for _j, _ch in enumerate(_all_css):
    if _ch == '{': _depth += 1
    elif _ch == '}':
        _depth -= 1
        if _depth == 0: _rules.append(_all_css[_start:_j + 1].strip()); _start = _j + 1
bg_css = ''.join(r for r in _rules if 'data-bgx' in r or 'data-rain' in r or 'rainfx' in r)
bg_pick = next(l for l in src if l.startswith('<script>(function(){var x="",q=(location.search.match(/[?&]bg='))
_r0 = next(n for n, l in enumerate(src) if l.startswith('<script>window.__rainOn='))
_r1 = next(n for n in range(_r0, len(src)) if src[n].startswith('</script>'))
rain_js = '\n'.join(src[_r0:_r1]) + '\n</script>'
assert len(bg_css) > 5000 and 'rainjs' in rain_js
footer_icons = re.findall(r'<a class="ib".*?</a>', '\n'.join(src[646:654]), flags=re.S)

THEMES = {
 'music':  dict(d=('#141412', '#1C1C19', '#F2F0EA', '#CFCCC4', '#96938B', '#2C2B28', '#E05AAE', '#141412'),
                l=('#F6F5F1', '#ECEAE4', '#141414', '#3A3935', '#6B6862', '#DAD7CF', '#B22A7E', '#FFFFFF')),
 'mm':     dict(d=('#141412', '#1C1C19', '#F2F0EA', '#CFCCC4', '#96938B', '#2C2B28', '#5188CF', '#141412'),
                l=('#F6F5F1', '#ECEAE4', '#141414', '#3A3935', '#6B6862', '#DAD7CF', '#3F74BD', '#FFFFFF')),
 'tg':     dict(d=('#141412', '#1C1C19', '#F2F0EA', '#CFCCC4', '#96938B', '#2C2B28', '#EAB421', '#141412'),
                l=('#F6F5F1', '#ECEAE4', '#141414', '#3A3935', '#6B6862', '#DAD7CF', '#A87A00', '#FFFFFF')),
}
KEYS = ['bg', 'pn', 'ink', 'ink2', 'mute', 'hair', 'acc', 'acc-ink']
theme_css = ''
for k, t in THEMES.items():
    theme_css += f'.k-{k}{{' + ';'.join(f'--{n}:{v}' for n, v in zip(KEYS, t['d'])) + '}'
    theme_css += f'html[data-theme="light"] .k-{k}{{' + ';'.join(f'--{n}:{v}' for n, v in zip(KEYS, t['l'])) + '}'

LANES = ['#3E7FD6', '#CF3F98', '#E38A26', '#D9BE22', '#22AFA6', '#8656D1', '#D7BB7D', '#262324']
ARROW = '<svg width="22" height="14" viewBox="0 0 22 14" aria-hidden="true"><path d="M1 7 H19 M13 1.5 L19.5 7 L13 12.5" fill="none" stroke="currentColor" stroke-width="1.8"></path></svg>'

# --- drawings (theme tokens only, so they follow light/dark) ---
def record():
    s = ['<svg viewBox="0 0 400 400" width="100%" role="img" aria-label="a vinyl record">']
    s.append('<circle cx="200" cy="200" r="190" fill="var(--ink)"/>')
    for r in range(176, 80, -7):
        s.append(f'<circle cx="200" cy="200" r="{r}" fill="none" stroke="var(--pn)" stroke-opacity=".22" stroke-width="1"/>')
    s.append('<path d="M200 22 A178 178 0 0 1 378 200" fill="none" stroke="var(--pn)" stroke-opacity=".35" stroke-width="10" stroke-linecap="round"/>')
    s.append('<circle cx="200" cy="200" r="68" fill="var(--acc)"/>')
    s.append('<text x="200" y="184" text-anchor="middle" font-family="Archivo, sans-serif" font-weight="900" font-size="22" letter-spacing="-.5" fill="var(--acc-ink)">mellotom</text>')
    s.append('<text x="200" y="228" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="10" fill="var(--acc-ink)">side a</text>')
    s.append('<circle cx="200" cy="200" r="6" fill="var(--pn)"/>')
    s.append('</svg>')
    return ''.join(s)

def splices():
    rnd = random.Random(7)
    W, H, mid = 400, 260, 130
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="a waveform cut into evenly placed splices">']
    n = 100
    for i in range(n):
        x = 10 + i * (W - 20) / n
        env = 0.35 + 0.65 * abs(__import__('math').sin(i / n * 7.3))
        h = (18 + rnd.random() * 70) * env
        s.append(f'<rect x="{x:.1f}" y="{mid - h:.1f}" width="2.4" height="{2 * h:.1f}" fill="var(--ink2)"/>')
    for j in range(9):
        x = 10 + j * (W - 20) / 8
        s.append(f'<line x1="{x:.1f}" y1="18" x2="{x:.1f}" y2="{H - 22}" stroke="var(--acc)" stroke-width="2.5"/>')
        s.append(f'<path d="M{x - 6:.1f} 10 H{x + 6:.1f} L{x:.1f} 19 Z" fill="var(--acc)"/>')
        if j < 8:
            s.append(f'<text x="{x + (W - 20) / 16:.1f}" y="{H - 6}" text-anchor="middle" font-family="Roboto Mono, monospace" font-size="11" fill="var(--mute)">{j + 1:02d}</text>')
    s.append('</svg>')
    return ''.join(s)

def eqmini(W=400, H=120, y0=0):
    import math
    L, Rt = 8, 8
    X = lambda f: L + (math.log10(f) - math.log10(20)) / 3 * (W - L - Rt)
    def d(f):
        hp = -10 * math.log10(1 + (180 / f) ** 16)
        ls = -5 / (1 + (f / 640) ** 2)
        return hp + ls
    pts = []
    for i in range(121):
        f = 20 * 1000 ** (i / 120)
        y = y0 + 34 - d(f) * 4.2
        pts.append(f'{X(f):.1f},{min(y, y0 + H - 6):.1f}')
    s = [f'<rect x="{L}" y="{y0}" width="{W - L - Rt}" height="{H}" fill="var(--pn)"/>']
    for f in (100, 1000, 10000):
        s.append(f'<line x1="{X(f):.1f}" x2="{X(f):.1f}" y1="{y0}" y2="{y0 + H}" stroke="var(--hair)"/>')
    s.append(f'<line x1="{L}" x2="{W - Rt}" y1="{y0 + 34}" y2="{y0 + 34}" stroke="var(--hair)"/>')
    s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="var(--acc)" stroke-width="3"/>')
    return ''.join(s)
def eqfig():
    return f'<svg viewBox="0 0 400 260" width="100%" role="img" aria-label="the blood_thinner curve: a high pass and a gentle low shelf">{eqmini(400, 236, 12)}</svg>'
def skinfig():
    # a synth panel reskinned: light header bars, silver knobs with dark pointers, a navy screen with a saw wave, no text
    import math
    s = ['<svg viewBox="0 0 400 260" width="100%" role="img" aria-label="a synth panel with silver knobs, light header bars and a dark screen">']
    s.append('<rect x="14" y="20" width="372" height="220" rx="6" fill="var(--pn)" stroke="var(--ink)" stroke-width="2"/>')
    for x0, w in ((14, 182), (204, 182)):
        s.append(f'<rect x="{x0 + 8}" y="30" width="{w - 16}" height="16" rx="2" fill="var(--ink2)" opacity=".85"/>')
        s.append(f'<rect x="{x0 + 16}" y="35" width="44" height="6" rx="3" fill="var(--pn)"/>')
        s.append(f'<rect x="{x0 + 8}" y="52" width="{w - 16}" height="76" rx="2" fill="var(--bg)" stroke="var(--hair)"/>')
    # saw on the left screen, triangle on the right
    s.append('<polyline points="32,118 104,62 104,118 176,62" fill="none" stroke="var(--acc)" stroke-width="3" stroke-linejoin="round"/>')
    s.append('<polyline points="222,118 258,62 294,118 330,62 368,118" fill="none" stroke="var(--acc)" stroke-width="3" stroke-linejoin="round" opacity=".7"/>')
    def knob(cx, cy, r, ang):
        a = math.radians(ang)
        out = [f'<circle cx="{cx}" cy="{cy}" r="{r + 4}" fill="none" stroke="var(--hair)" stroke-width="3"/>',
               f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="var(--ink2)"/>',
               f'<circle cx="{cx - r * .3:.1f}" cy="{cy - r * .35:.1f}" r="{r * .45:.1f}" fill="var(--ink)" opacity=".45"/>',
               f'<line x1="{cx + r * .25 * math.cos(a):.1f}" y1="{cy + r * .25 * math.sin(a):.1f}" x2="{cx + r * .85 * math.cos(a):.1f}" y2="{cy + r * .85 * math.sin(a):.1f}" stroke="var(--pn)" stroke-width="3" stroke-linecap="round"/>']
        return ''.join(out)
    angles = [200, 250, 300, 340, 225, 280, 320, 20]
    for i, cx in enumerate((48, 102, 156, 244, 298, 352)):
        s.append(knob(cx, 160, 15, angles[i]))
    for i, cx in enumerate((48, 102, 156, 244, 298, 352)):
        s.append(knob(cx, 210, 11, angles[(i + 3) % 8]))
    s.append('<line x1="200" y1="146" x2="200" y2="226" stroke="var(--hair)" stroke-width="2"/>')
    s.append('</svg>')
    return ''.join(s)
def toolsfig():
    # a generic ableton-style device: title bar, knobs, buttons and toggles, no text
    import math
    s = ['<svg viewBox="0 0 400 260" width="100%" role="img" aria-label="a generic ableton device with knobs and buttons">']
    s.append('<rect x="14" y="20" width="372" height="220" rx="8" fill="var(--pn)" stroke="var(--ink)" stroke-width="2"/>')
    s.append('<path d="M22 20 H378 a8 8 0 0 1 8 8 V50 H14 V28 a8 8 0 0 1 8 -8 Z" fill="var(--hair)"/>')
    s.append('<circle cx="34" cy="35" r="8" fill="var(--acc)"/>')
    s.append('<rect x="52" y="30" width="96" height="10" rx="5" fill="var(--mute)" opacity=".55"/>')
    for i in range(3): s.append(f'<circle cx="{332 + i * 18}" cy="35" r="6" fill="var(--mute)" opacity=".55"/>')
    def knob(cx, cy, r, frac, acc=True):
        a0, a1 = math.radians(225), math.radians(-45)
        p = lambda a: (cx + r * math.cos(a), cy - r * math.sin(a))
        x0, y0 = p(a0); x1, y1 = p(a1)
        s.append(f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 1 1 {x1:.1f} {y1:.1f}" fill="none" stroke="var(--hair)" stroke-width="5" stroke-linecap="round"/>')
        a = a0 + (a1 - a0) * frac; xa, ya = p(a); large = 1 if (a0 - a) > math.pi else 0
        col = 'var(--acc)' if acc else 'var(--ink)'
        s.append(f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 {large} 1 {xa:.1f} {ya:.1f}" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"/>')
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{xa:.1f}" y2="{ya:.1f}" stroke="var(--ink)" stroke-width="3" stroke-linecap="round"/>')
    for i, fr in enumerate((.32, .58, .8)):
        knob(66 + i * 72, 96, 24, fr)
    for i, fr in enumerate((.2, .5, .7, .4)):
        knob(48 + i * 46, 160, 13, fr, acc=False)
    for i, on in enumerate((1, 0, 1, 0, 0)):
        col = 'var(--acc)' if on else 'var(--hair)'
        s.append(f'<rect x="{30 + i * 40}" y="194" width="32" height="22" rx="3" fill="{col}"/>')
    s.append('<rect x="244" y="64" width="128" height="88" rx="4" fill="var(--bg)" stroke="var(--hair)"/>')
    pts = ' '.join(f'{252 + i * 1.12:.1f},{108 - 26 * math.sin(i / 100 * math.pi * 2) * math.exp(-i / 140):.1f}' for i in range(101))
    s.append(f'<polyline points="{pts}" fill="none" stroke="var(--acc)" stroke-width="3"/>')
    for i, on in enumerate((1, 0)):
        col = 'var(--acc)' if on else 'var(--hair)'
        s.append(f'<rect x="{244 + i * 66}" y="166" width="62" height="20" rx="3" fill="{col}"/>')
    s.append('<rect x="244" y="204" width="128" height="6" rx="3" fill="var(--hair)"/><rect x="244" y="204" width="84" height="6" rx="3" fill="var(--acc)"/><circle cx="328" cy="207" r="9" fill="var(--ink)"/>')
    s.append('</svg>')
    return ''.join(s)
def sheet():
    s = ['<svg viewBox="0 0 400 260" width="100%" role="img" aria-label="a travelers guide sheet">']
    s.append('<rect x="1" y="1" width="398" height="258" fill="var(--bg)" stroke="var(--ink)" stroke-width="2"/>')
    s.append('<text x="18" y="52" font-family="Archivo, sans-serif" font-weight="900" font-size="38" letter-spacing="-1.5" fill="var(--ink)">guide</text>')
    s.append('<rect x="132" y="28" width="96" height="7" fill="var(--ink)"/><rect x="132" y="40" width="72" height="7" fill="var(--acc)"/>')
    s.append('<rect x="18" y="60" width="270" height="5" fill="var(--ink)"/>')
    for i, c in enumerate(LANES[:5]):
        s.append(f'<rect x="0" y="{74 + i * 4}" width="400" height="2" fill="{c}"/>')
    cols = [(18, 80), (108, 80), (198, 80)]
    for ci, (x, w) in enumerate(cols):
        s.append(f'<rect x="{x}" y="104" width="14" height="10" fill="{LANES[ci]}"/><rect x="{x + 18}" y="105" width="{w - 30}" height="8" fill="var(--ink)"/>')
        for r in range(6):
            y = 124 + r * 18
            s.append(f'<rect x="{x}" y="{y}" width="20" height="5" fill="var(--mute)"/><rect x="{x + 26}" y="{y}" width="{w - 30 - (r * 7) % 18}" height="5" fill="var(--ink2)"/>')
    s.append('<rect x="290" y="96" width="94" height="148" fill="var(--pn)" stroke="var(--ink)" stroke-width="1.5"/>')
    s.append('<rect x="314" y="108" width="46" height="124" rx="2" fill="var(--bg)" stroke="var(--ink)" stroke-width="1.5"/>')
    for (cx, cy, r) in [(327, 128, 8), (347, 128, 8), (337, 156, 6), (327, 184, 4), (347, 184, 4), (327, 206, 4), (347, 206, 4)]:
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="var(--ink)" stroke-width="1.5"/>')
    s.append('<rect x="18" y="246" width="270" height="3" fill="var(--ink)"/>')
    s.append('</svg>')
    return ''.join(s)

CARDS = [
 dict(k='music', slug='linktr.ee/mellotom', n='01', maker='mellotom', kind='links', h='music', what='every link in one place',
      t1='_mellotom', t2='_for listening', href='https://linktr.ee/mellotom', ext=True, fig=record(), ratio='1 / 1', mw='300px',
      br='[ music ]', sub=['opens linktr.ee']),
 dict(k='mm', slug='tools', n='02', maker='free', kind='pay what you want', h='free tools + downloads', what='m4l devices, ableton presets + serum skins',
      t1='_devices + presets', t2='_each with its own guide', href='/tools/', ext=False, fig=toolsfig(), ratio='400 / 260', mw='400px',
      br='[ free tools ]', sub=['morpmarker', '·', 'blood_thinner', '·', 'massiv']),
 dict(k='tg', slug='travelers-guide', n='03', maker='eurorack', kind='one-page guides', h='travelers guide', what='the welcome center',
      t1='_welcome center', t2='_choose a destination', href='/travelers-guide/', ext=False, fig=sheet(), ratio='400 / 260', mw='400px',
      br='[ the guides ]', sub=['light / dark inside', '·', 'phone friendly', '·', 'print ready']),
]
import json as _json
GUM = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gumroad.json'), encoding='utf-8'))
def card(c):
    stripes = ''.join(f'<div style="height: 4px; background: var(--acc); opacity: {o}"></div>' for o in (1, .7, .45))
    tgt = ' target="_blank" rel="noopener"' if c['ext'] else ''
    return f'''<article class="card k-{c['k']}">
<div class="stripes" aria-hidden="true">{stripes}</div>
<div class="cin">
<div class="slug"><span>{c['slug']}</span><span class="dots" aria-hidden="true"></span><span>{c['n']} / {c.get('tot', '03')}</span></div>
<div class="slug m"><span>{c['maker']}</span><span class="dots" aria-hidden="true"></span><span>{c['kind']}</span></div>
<div class="head"><span class="num">{c['n']}</span><div class="hb"><h2>{c['h']}</h2><span class="what">{c['what']}</span></div></div>
<div class="tag"><span>{c['t1']}</span><span class="acc">{c['t2']}</span></div>
<a class="fig" href="{c['href']}"{tgt} aria-label="open {c['h']}" tabindex="-1"><div class="figbox" style="aspect-ratio: {c['ratio']}; max-width: {c['mw']}">{c['fig']}</div></a>
<a class="go" href="{c['href']}"{tgt}><span>{c.get('go', 'navigate')}</span> <span class="br">{c['br']}</span>{ARROW}</a>{('<a class="go dl" href="' + c['dl'] + '" target="_blank" rel="noopener"><span>free download</span> <span class="br">[ gumroad ]</span>' + ARROW + '</a>') if c.get('dl') else ''}
<div class="sub">{''.join(f'<span>{x}</span>' for x in c['sub'])}</div>
</div>
</article>'''

lanes = ''.join(f'<div style="height: 3px; background: {c}"></div>' for c in LANES)
crops = ''.join(f'<div class="crop" style="{a}" aria-hidden="true"></div>' for a in [
  'top: 24px; left: 24px; border-top-width: 2px; border-left-width: 2px', 'top: 24px; right: 24px; border-top-width: 2px; border-right-width: 2px',
  'bottom: 24px; left: 24px; border-bottom-width: 2px; border-left-width: 2px', 'bottom: 24px; right: 24px; border-bottom-width: 2px; border-right-width: 2px'])
page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>mellotom</title>
<meta name="description" content="mellotom: music, the morpmarker max for live device, and the travelers guide eurorack guides.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&amp;family=Roboto+Mono:wght@400;500;600;700&amp;display=swap">
<style>{root_vars}{theme_css}{tm_css}
{base_css}
.grid{{padding-bottom:4px}}.go.dl{{margin-top:8px}}h1.logo{{line-height:0}}.logo-svg{{display:block;height:clamp(64px,8.2vw,148px);width:auto;max-width:100%}}.vh{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}.hero{{grid-template-columns:minmax(0,1fr)}}
@media (min-width:1100px){{.wrap{{min-height:100vh;display:flex;flex-direction:column}}.grid{{flex:1}}}}
{bg_css}
</style>
{bg_pick}
</head>
<body>
<div class="wrap">
{crops}
<div class="slugs">
<div><span style="font-weight: 600">mellotom.music ................ 00.00_00</span><span>home ...................... 3 destinations</span></div>
<div class="tm-line"><span>mode ...................... <button type="button" class="tm" data-t="light" aria-pressed="false">light</button>/<button type="button" class="tm" data-t="dark" aria-pressed="false">dark</button></span></div>
<div class="r"><span>conceived by ............. <a href="https://linktr.ee/mellotom" target="_blank" rel="noopener" style="text-underline-offset: 2px">mellotom</a></span><span>rev ......................... 2026.11</span><span class="gc" data-path="TOTAL" data-l="37" style="visibility: hidden">visitors</span></div>
</div>
<header class="hero">
<div>
<div class="titlerow"><h1 class="logo"><span class="vh">mellotom</span>{LOGO}</h1>
<div class="sub2"><span>_home</span><span class="acc">_choose a destination</span></div></div>
<div class="bar"></div>
</div>
</header>
<div class="lanes" aria-hidden="true">{lanes}</div>
<div class="strip"><span>music · free tools · travelers guide</span><span>pick a window or press navigate</span><span>mellotom.music</span></div>
<main class="grid">
{''.join(card(c) for c in CARDS)}
</main>
<footer class="foot">
<div>design homage to the <a href="https://www.marvel.com/comics/guides/1556/house-of-xpowers-of-x" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 2px">house of x / powers of x</a> data pages — designed by tom muller with jonathan hickman<br>not affiliated with ableton, cycling '74, make noise, xfer records or marvel</div>
<div class="right">
{''.join(footer_icons)}
<span style="display: flex; flex-direction: column; align-items: flex-end"><span>conceived by <a class="l" href="https://linktr.ee/mellotom" target="_blank" rel="noopener">mellotom</a> · mellotom.music ... 00.00_01</span><span style="opacity: .62"><a href=https://mellotom.music/ai-usage-disclaimer/ style=color:inherit;text-underline-offset:2px>AI Usage Disclaimer</a></span></span>
</div>
</footer>
</div>
{theme_js}
<script src="/travelers-guide/palettes.js?v=20261121b"></script>
<script>(function(){{var T=window.TG_THEME;if(!T)return;
function rgb(h){{h=h.replace("#","");return [0,2,4].map(function(i){{return parseInt(h.substr(i,2),16);}});}}
function hex(c){{return "#"+c.map(function(v){{v=Math.max(0,Math.min(255,Math.round(v)));return (v<16?"0":"")+v.toString(16);}}).join("");}}
function lum(c){{c=c.map(function(v){{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4);}});return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2];}}
function contrast(a,b){{var x=lum(a),y=lum(b);return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05);}}
function hueSat(c){{var r=c[0]/255,g=c[1]/255,b=c[2]/255,mx=Math.max(r,g,b),mn=Math.min(r,g,b),d=mx-mn,l=(mx+mn)/2,s=d===0?0:d/(1-Math.abs(2*l-1)),h=0;
 if(d){{if(mx===r)h=((g-b)/d)%6;else if(mx===g)h=(b-r)/d+2;else h=(r-g)/d+4;h*=60;if(h<0)h+=360;}}return [h,s];}}
function readable(c,bg,toward){{var out=c,step=0;while(contrast(out,bg)<4.5&&step<20){{step++;out=c.map(function(v,i){{return v+(toward[i]-v)*step/20;}});}}return out;}}
var seen={{}},pool=[T.accent[0]].concat(T.lanes).filter(function(h){{h=h.toUpperCase();if(seen[h])return false;seen[h]=1;var c=rgb(h),L=lum(c);return hueSat(c)[1]>=0.25&&L>0.02&&L<0.8;}});
if(!pool.length)pool=[T.accent[0]];
var picks=[pool[0]];
while(picks.length<3&&picks.length<pool.length){{var best=null,bestGap=-1;pool.forEach(function(h){{if(picks.indexOf(h)>=0)return;var hh=hueSat(rgb(h))[0],gap=Math.min.apply(null,picks.map(function(p){{var d=Math.abs(hueSat(rgb(p))[0]-hh);return Math.min(d,360-d);}}));if(gap>bestGap){{bestGap=gap;best=h;}}}});picks.push(best);}}
while(picks.length<3)picks.push(picks[picks.length%pool.length]);
var DARK_BG=rgb("#141412"),LIGHT_BG=rgb("#F6F5F1"),INK_D=rgb("#141414"),INK_L=rgb("#FFFFFF"),css="";
["music","mm","tg"].forEach(function(k,n){{var c=rgb(picks[n]),d=readable(c,DARK_BG,[255,255,255]),l=readable(c,LIGHT_BG,[0,0,0]);
 function ink(x){{return contrast(x,INK_D)>=contrast(x,INK_L)?"#141414":"#FFFFFF";}}
 css+=".k-"+k+"{{--acc:"+hex(d)+";--acc-ink:"+ink(d)+"}}html[data-theme=light] .k-"+k+"{{--acc:"+hex(l)+";--acc-ink:"+ink(l)+"}}";}});
var st=document.createElement("style");st.id="cardacc";st.textContent=css;document.head.appendChild(st);}})();</script>
{rain_js}
<script data-goatcounter="https://mellotom.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
<script>(function(){{var e=document.querySelector('.gc');if(!e||!window.fetch)return;var p=e.getAttribute('data-path')||location.pathname,L=+e.getAttribute('data-l')||40;fetch('https://mellotom.goatcounter.com/counter/'+encodeURIComponent(p)+'.json').then(function(r){{return r.ok?r.json():null}}).then(function(j){{if(!j||j.count==null)return;var n=String(j.count).trim();e.textContent='visitors '+new Array(Math.max(3,L-9-n.length)).join('.')+' '+n;e.style.visibility='visible';}}).catch(function(){{}});}})();</script>
</body>
</html>
'''
open(sys.argv[2], 'w', encoding='utf-8').write(page)

# ---- free tools page (mellotom.music/tools/): one window per free download, each with its product page and a gumroad button
TOOLS = [
 dict(k='music', slug='blood_thinner', n='01', tot='03', maker='ableton eq eight', kind='preset', h='[ blood_thinner ]', what='clears low-end mud on every track',
      t1='_eq eight preset', t2='_six macros, five bands free', href='/blood-thinner/', ext=False, fig=eqfig(), ratio='400 / 260', mw='400px',
      br='[ product page ]', dl=GUM['blood_thinner'], sub=['free', '·', 'name your price']),
 dict(k='mm', slug='morpmarker', n='02', tot='03', maker='max for live', kind='device', h='morpmarker', what='splice markers for the morphagene',
      t1='_max for live device', t2='_for marking splices', href='/morpmarker/', ext=False, fig=splices(), ratio='400 / 260', mw='400px',
      br='[ product page ]', dl=GUM['morpmarker'], sub=['free', '·', 'name your price']),
 dict(k='tg', slug='massiv', n='03', tot='03', maker='xfer serum 2', kind='skin', h='[ massiv ]', what='a silver-knob, navy-screen reskin for serum 2',
      t1='_serum 2 skin', t2='_1x + 2x, mac + windows', href=GUM['massiv'], ext=True, fig=skinfig(), ratio='400 / 260', mw='400px',
      go='free download', br='[ gumroad ]', sub=['free', '·', 'name your price']),
]
tp = page
def _tswap(a, b):
    global tp
    assert tp.count(a) == 1, a[:60]
    tp = tp.replace(a, b)
_tswap('<title>mellotom</title>', '<title>free tools · mellotom</title>')
_tswap('content="mellotom: music, the morpmarker max for live device, and the travelers guide eurorack guides."', 'content="free max for live devices, ableton presets and serum skins by mellotom. download free on gumroad, or name your price."')
_tswap('<span>home ...................... 3 destinations</span>', f'<span>tools ................ {len(TOOLS)} free downloads</span>')
_tswap('<span class="gc" data-path="TOTAL" data-l="37"', '<span class="gc" data-l="37"')
_tswap('<span>_home</span><span class="acc">_choose a destination</span>', '<span>_free tools</span><span class="acc">_pay what you want</span>')
_tswap('<span>music · free tools · travelers guide</span><span>pick a window or press navigate</span><span>mellotom.music</span>', '<span>every download is free on gumroad · name your price if you like</span><span>downloads stay in your gumroad library</span><span>mellotom.music</span>')
tp = re.sub(r'<main class="grid">.*?</main>', lambda m: '<main class="grid">' + ''.join(card(c) for c in TOOLS) + '</main>', tp, count=1, flags=re.S)
_back = ('<span><a class="tm" href="/" style="display: inline-flex; align-items: center; gap: 5px"><svg width="14" height="9" viewBox="0 0 14 9" aria-hidden="true" style="display: block; flex: none">'
         '<path d="M13.2 4.5 H1.6 M5.1 1 L1.6 4.5 L5.1 8" fill="none" stroke="currentColor" stroke-width="1.3"></path></svg><span>back to mellotom.music</span></a></span>')
_tswap('<div class="tm-line"><span>mode', '<div class="tm-line">' + _back + '<span>mode')
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(sys.argv[2])), 'tools'), exist_ok=True)
open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[2])), 'tools', 'index.html'), 'w', encoding='utf-8').write(tp)
print('ok tools', len(tp))

# ---- ai usage disclaimer page: same shell as the home page, text from build/disclaimer.txt ----
import html as _html
_here = os.path.dirname(os.path.abspath(__file__))
_raw = open(os.path.join(_here, 'disclaimer.txt'), encoding='utf-8').read().strip().split('\n')
_meta = [l for l in _raw if l.startswith('[ ')]
_paras = [l[2:].strip() for l in _raw if l.startswith('>>')]
def _fmt(t):
    # __bold underlined__, **bold**, *italic*
    t = _html.escape(t)
    t = re.sub(r'__(.+?)__', r'<b><u>\1</u></b>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    return re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
def _meta_row(l):
    k, v = l.split(' : ', 1)
    return f'<div class="em"><span class="ek">{_html.escape(k)}</span><span class="es">:</span><span class="ev">{_html.escape(v)}</span></div>'
ENTRY = ('<main class="entry"><article class="ebox">' + ''.join(_meta_row(l) for l in _meta)
         + '<div class="ebody">' + ''.join(f'<p><span class="gt" aria-hidden="true">&gt;&gt;</span><span>{_fmt(t)}</span></p>' for t in _paras)
         + '</div></article></main>')
ENTRY_CSS = ('.entry{display:block;padding:28px 0 8px}'
 '.ebox{max-width:980px;margin:0 auto;border:2px solid var(--pa);padding:22px 30px 26px}'
 '.em{display:flex;gap:12px;font-family:"Roboto Mono",monospace;font-size:15px;line-height:1.7;color:var(--pi)}'
 '.ek{color:var(--pm);min-width:150px}.es{color:var(--pm)}.ev{font-weight:700;color:var(--pa)}'
 '.ebody{border-top:4px solid var(--pi);margin-top:14px;padding-top:6px}'
 '.ebody p{display:grid;grid-template-columns:34px minmax(0,1fr);gap:0 6px;margin:14px 0 0;font-size:19px;line-height:1.55;color:var(--pi)}'
 '.ebody b{font-weight:800}.ebody u{text-decoration-thickness:2px;text-underline-offset:4px}.gt{font-family:"Roboto Mono",monospace;font-weight:700;color:var(--pa);font-size:15px;line-height:1.95}'
 '@media (max-width:899px){.ebox{padding:16px 16px 20px}.em{flex-wrap:wrap;gap:0 8px;font-size:13px}.ek{min-width:0}.ebody p{grid-template-columns:26px minmax(0,1fr);font-size:16.5px}.gt{font-size:13px;line-height:1.9}}'
 '@media (min-width:1100px){.entry{flex:1}}')
BACK = ('<span><a class="tm" href="/" style="display: inline-flex; align-items: center; gap: 5px"><svg width="14" height="9" viewBox="0 0 14 9" aria-hidden="true" style="display: block; flex: none">'
        '<path d="M13.2 4.5 H1.6 M5.1 1 L1.6 4.5 L5.1 8" fill="none" stroke="currentColor" stroke-width="1.3"></path></svg><span>back to mellotom.music</span></a></span>')
d = page
def _swap(a, b):
    global d
    assert d.count(a) == 1, a[:60]
    d = d.replace(a, b)
_swap('<span class="gc" data-path="TOTAL" data-l="37"', '<span class="gc" data-l="37"')
_swap('<title>mellotom</title>', '<title>ai usage disclaimer · mellotom</title>')
_swap('content="mellotom: music, the morpmarker max for live device, and the travelers guide eurorack guides."', 'content="how mellotom uses ai on mellotom.music, and what it is never used for."')
_swap('<span>home ...................... 3 destinations</span>', '<span>entry .............. ai usage disclaimer</span>')
_swap('<div class="tm-line"><span>mode', '<div class="tm-line">' + BACK + '<span>mode')
_swap('<span>_home</span><span class="acc">_choose a destination</span>', '<span>_entry</span><span class="acc">_ai usage disclaimer</span>')
_swap('<span>music · free tools · travelers guide</span><span>pick a window or press navigate</span><span>mellotom.music</span>', '<span>ai usage disclaimer</span><span>linked from every page footer</span><span>mellotom.music</span>')
d = re.sub(r'<main class="grid">.*?</main>', lambda m: ENTRY, d, count=1, flags=re.S)
_swap('</style>\n' + bg_pick, ENTRY_CSS + '\n</style>\n' + bg_pick)
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(sys.argv[2])), 'ai-usage-disclaimer'), exist_ok=True)
open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[2])), 'ai-usage-disclaimer', 'index.html'), 'w', encoding='utf-8').write(d)
print('ok disclaimer', len(d))
print('ok', len(page))
