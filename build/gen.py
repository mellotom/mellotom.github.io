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
footer_icons = re.findall(r'<a class="ib".*?</a>', '\n'.join(src[646:654]), flags=re.S)

THEMES = {
 'music':  dict(d=('#1A1418', '#231B20', '#F3ECEF', '#D3C6CC', '#A3939A', '#33282E', '#E05AAE', '#1A1418'),
                l=('#F7F2F4', '#EEE5E9', '#221A1E', '#4B3E44', '#776970', '#E2D7DC', '#B22A7E', '#FFFFFF')),
 'mm':     dict(d=('#141414', '#1C1C1C', '#F2F2F2', '#D4D4D4', '#9B9B9B', '#2E2E2E', '#5188CF', '#101010'),
                l=('#F4F3EF', '#EAE8E2', '#141414', '#34332F', '#67655F', '#D6D3CB', '#3F74BD', '#FFFFFF')),
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
 dict(k='mm', slug='morpmarker', n='02', maker='max for live', kind='device', h='morpmarker', what='splice markers for the morphagene',
      t1='_max for live device', t2='_for marking splices', href='/morpmarker/', ext=False, fig=splices(), ratio='400 / 260', mw='400px',
      br='[ manual + download ]', sub=['manual', '·', 'download']),
 dict(k='tg', slug='travelers-guide', n='03', maker='eurorack', kind='one-page guides', h='travelers guide', what='the welcome center',
      t1='_welcome center', t2='_choose a destination', href='/travelers-guide/', ext=False, fig=sheet(), ratio='400 / 260', mw='400px',
      br='[ the guides ]', sub=['light / dark inside', '·', 'phone friendly', '·', 'print ready']),
]
def card(c):
    stripes = ''.join(f'<div style="height: 4px; background: var(--acc); opacity: {o}"></div>' for o in (1, .7, .45))
    tgt = ' target="_blank" rel="noopener"' if c['ext'] else ''
    return f'''<article class="card k-{c['k']}">
<div class="stripes" aria-hidden="true">{stripes}</div>
<div class="cin">
<div class="slug"><span>{c['slug']}</span><span class="dots" aria-hidden="true"></span><span>{c['n']} / 03</span></div>
<div class="slug m"><span>{c['maker']}</span><span class="dots" aria-hidden="true"></span><span>{c['kind']}</span></div>
<div class="head"><span class="num">{c['n']}</span><div class="hb"><h2>{c['h']}</h2><span class="what">{c['what']}</span></div></div>
<div class="tag"><span>{c['t1']}</span><span class="acc">{c['t2']}</span></div>
<a class="fig" href="{c['href']}"{tgt} aria-label="open {c['h']}" tabindex="-1"><div class="figbox" style="aspect-ratio: {c['ratio']}; max-width: {c['mw']}">{c['fig']}</div></a>
<a class="go" href="{c['href']}"{tgt}><span>navigate</span> <span class="br">{c['br']}</span>{ARROW}</a>
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
.grid{{padding-bottom:4px}}h1.logo{{line-height:0}}.logo-svg{{display:block;height:clamp(64px,8.2vw,148px);width:auto;max-width:100%}}.vh{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}.hero{{grid-template-columns:minmax(0,1fr)}}
@media (min-width:1100px){{.wrap{{min-height:100vh;display:flex;flex-direction:column}}.grid{{flex:1}}}}
</style>
</head>
<body>
<div class="wrap">
{crops}
<div class="slugs">
<div><span style="font-weight: 600">mellotom.music ................ 00.00_00</span><span>home ...................... 3 destinations</span></div>
<div class="tm-line"><span>mode ...................... <button type="button" class="tm" data-t="light" aria-pressed="false">light</button>/<button type="button" class="tm" data-t="dark" aria-pressed="false">dark</button></span></div>
<div class="r"><span>conceived by ............. <a href="https://linktr.ee/mellotom" target="_blank" rel="noopener" style="text-underline-offset: 2px">mellotom</a></span><span>rev ......................... 2026.11</span></div>
</div>
<header class="hero">
<div>
<div class="titlerow"><h1 class="logo"><span class="vh">mellotom</span>{LOGO}</h1>
<div class="sub2"><span>_home</span><span class="acc">_choose a destination</span></div></div>
<div class="bar"></div>
</div>
</header>
<div class="lanes" aria-hidden="true">{lanes}</div>
<div class="strip"><span>music · morpmarker · travelers guide</span><span>pick a window or press navigate</span><span>mellotom.music</span></div>
<main class="grid">
{''.join(card(c) for c in CARDS)}
</main>
<footer class="foot">
<div>design homage to the <a href="https://www.marvel.com/comics/guides/1556/house-of-xpowers-of-x" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 2px">house of x / powers of x</a> data pages — designed by tom muller with jonathan hickman<br>not affiliated with ableton, cycling '74, make noise or marvel</div>
<div class="right">
{''.join(footer_icons)}
<span style="display: flex; flex-direction: column; align-items: flex-end"><span>conceived by <a class="l" href="https://linktr.ee/mellotom" target="_blank" rel="noopener">mellotom</a> · mellotom.music ... 00.00_01</span><span style="opacity: .62">created with claude</span></span>
</div>
</footer>
</div>
{theme_js}
<script data-goatcounter="https://mellotom.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
'''
open(sys.argv[2], 'w', encoding='utf-8').write(page)
print('ok', len(page))
