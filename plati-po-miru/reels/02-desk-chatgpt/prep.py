#!/usr/bin/env python3
"""Готовит public/ для DeskReel: ассеты из config.sources, шрифты, музыку и SFX (всё синтезировано,
без чужих треков) и сведённый public/mix.wav ровно на длину ролика."""
import json, os, re, shutil, subprocess, urllib.request
import numpy as np

cfg = json.load(open("config.json"))
os.makedirs("public", exist_ok=True)
P = lambda n: os.path.join("public", n)
for name, url in cfg["sources"].items():
    if not os.path.exists(P(name)):
        subprocess.run(f"curl -sSf -o {P(name)} '{url}'", shell=True, check=True)

def gfont(family, out):
    if os.path.exists(P(out)): return
    try:
        css = urllib.request.urlopen(urllib.request.Request(f"https://fonts.googleapis.com/css2?family={family}", headers={"User-Agent": "curl"}), timeout=20).read().decode()
        urls = re.findall(r"url\((https://[^)]+\.ttf)\)", css)
        urllib.request.urlretrieve(urls[0], P(out))
    except Exception as e:
        print("font fallback", family, e)
for c in ["/usr/share/fonts/truetype/higgsfield/Montserrat-ExtraBold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
    if os.path.exists(c) and not os.path.exists(P(cfg["assets"]["fontMain"])): shutil.copy(c, P(cfg["assets"]["fontMain"]))
gfont("Caveat:wght@700", cfg["assets"]["fontHand"])
gfont("PT+Mono", cfg["assets"]["fontMono"])
for k in ("fontHand", "fontMono"):
    if not os.path.exists(P(cfg["assets"][k])): shutil.copy(P(cfg["assets"]["fontMain"]), P(cfg["assets"][k]))

# ---------------- звук ----------------
SR, FPS = 48000, cfg["fps"]
DUR = cfg["durationInFrames"] / FPS
N = int(SR * DUR)
t_all = np.arange(N) / SR
rng = np.random.default_rng(7)
music = np.zeros(N); sfx = np.zeros(N)

def put(buf, start, sig, g=1.0):
    i = int(start * SR)
    if i >= N: return
    j = min(N, i + len(sig)); buf[i:j] += sig[: j - i] * g

def env_exp(n, k): return np.exp(-np.arange(n) / SR * k)
def lp(x, a=0.15):  # однополюсный ФНЧ
    y = np.zeros_like(x); acc = 0.0
    for i, v in enumerate(x): acc += a * (v - acc); y[i] = acc
    return y
def hp(x): return np.diff(np.concatenate([[0], x]))

BPM = 112; beat = 60 / BPM
def kick():
    n = int(0.32 * SR); tt = np.arange(n) / SR
    f = 45 + 110 * np.exp(-tt * 30); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env_exp(n, 9)
def hat():
    n = int(0.05 * SR); return hp(rng.standard_normal(n)) * env_exp(n, 90) * 0.5
def clap():
    n = int(0.16 * SR); x = hp(lp(rng.standard_normal(n), 0.5)); return x * env_exp(n, 22) * 0.7
def bassnote(freq, length):
    n = int(length * SR); tt = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * freq * h * tt) / h for h in range(1, 6))
    return lp(x, 0.08) * env_exp(n, 5) * 0.9
def chord(freqs, length):
    n = int(length * SR); tt = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt) for f in freqs)
    a = np.minimum(1, tt / 0.01) * env_exp(n, 3.5)
    return x * a * 0.12

K, H, CL = kick(), hat(), clap()
prog = [(55.0, [220, 261.6, 329.6]), (43.65, [174.6, 220, 261.6]), (65.4, [261.6, 329.6, 392]), (49.0, [196, 246.9, 293.7])]
b = 0; tb = 0.0
while tb < DUR:
    bar = int(b // 4); root, ch = prog[bar % 4]
    put(music, tb, K, 0.9 if b % 1 == 0 else 0)
    put(music, tb + beat / 2, H, 0.55)
    if b % 4 in (1, 3): put(music, tb, CL, 0.45)
    put(music, tb, bassnote(root, beat * 0.9), 0.5)
    put(music, tb + beat / 2, bassnote(root * 2, beat * 0.45), 0.22)
    if b % 4 == 0: put(music, tb, chord(ch, beat * 4), 1.0)
    if b % 2 == 1: put(music, tb + beat * 0.75, chord([c * 2 for c in ch], beat * 0.6), 0.5)
    b += 1; tb = b * beat

# автоматизация громкости музыки по сценам
pts = [(0, 1.0), (2.95, 1.0), (3.05, 0.12), (5.35, 0.12), (5.6, 1.0), (8.0, 1.0), (8.3, 0.7), (12.3, 0.7), (12.6, 0.95), (18.4, 0.85), (19.9, 0.0), (DUR, 0.0)]
music *= np.interp(t_all, [p[0] for p in pts], [p[1] for p in pts])

# SFX
def tock(f0=700):
    n = int(0.12 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f0 * tt) * env_exp(n, 40) + hp(rng.standard_normal(n)) * env_exp(n, 160) * 0.6)
def thud():
    n = int(0.4 * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * (60 + 40 * np.exp(-tt * 20)) * tt) * env_exp(n, 9)
def slap():
    n = int(0.14 * SR); x = lp(rng.standard_normal(n), 0.35) * env_exp(n, 28) * 1.2
    tk = tock(380); x[:len(tk)] += tk * 0.5
    return x
def click():
    n = int(0.03 * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * 2400 * tt) * env_exp(n, 220)
def rip(length=0.7):
    n = int(length * SR); x = hp(rng.standard_normal(n))
    crack = (rng.random(n) < 0.004).astype(float); crack = np.convolve(crack, np.ones(120) / 40, mode="same")
    amp = np.clip(np.sin(np.linspace(0, np.pi, n)) * 1.2, 0, 1) * (0.5 + crack)
    return lp(x * amp, 0.55) * 1.6
def whoosh(length=0.5, a0=0.05, a1=0.5):
    n = int(length * SR); x = rng.standard_normal(n); y = np.zeros(n); acc = 0.0
    al = np.linspace(a0, a1, n)
    for i in range(n): acc += al[i] * (x[i] - acc); y[i] = acc
    return y * np.sin(np.linspace(0, np.pi, n)) ** 2 * 1.4
def chime():
    n = int(1.4 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1046.5 * tt) + 0.6 * np.sin(2 * np.pi * 1568 * tt) + 0.3 * np.sin(2 * np.pi * 2093 * tt)) * env_exp(n, 3.2) * 0.35
def scribble(length=0.5):
    n = int(length * SR); return hp(rng.standard_normal(n)) * (0.4 + 0.6 * np.abs(np.sin(np.linspace(0, 18, n)))) * 0.25

for tt_, g in [(0.0, 0.9), (0.4, 0.9), (0.8, 0.9)]: put(sfx, tt_, tock(), g)
put(sfx, 3.0, thud(), 0.9); put(sfx, 3.2, slap(), 0.9)
put(sfx, 6.03, click(), 0.6); put(sfx, 6.2, rip(0.72), 0.8); put(sfx, 6.75, whoosh(0.5), 0.6)
put(sfx, 8.0, whoosh(0.4, 0.03, 0.25), 0.35); put(sfx, 9.4, scribble(0.55), 0.6)
put(sfx, 12.5, whoosh(0.6, 0.03, 0.2), 0.45); put(sfx, 14.2, rip(0.45) * 0.5, 0.5)
put(sfx, 16.0, chime(), 1.0)

mix = music * 0.5 + sfx * 0.8
mix /= max(1e-9, np.max(np.abs(mix))) / 0.89
import wave
with wave.open(P(cfg["assets"]["audio"]), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("prep ok", round(DUR, 2), "s audio")
