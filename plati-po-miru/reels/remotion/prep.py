#!/usr/bin/env python3
"""Готовит public/ для Remotion: скачивает кадры и озвучку, ускоряет голос,
распознаёт слова (faster-whisper), синтезирует SFX (sox) и пишет public/timeline.json.
Запуск: python3 prep.py ../01-ne-nazhimay/reel.json"""
import json, os, shutil, subprocess, sys

def sh(c): subprocess.run(c, shell=True, check=True)
def dur(f): return float(subprocess.check_output(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {f}", shell=True))

cfg = json.load(open(sys.argv[1]))
os.makedirs("public", exist_ok=True); os.chdir("public")
for name, url in cfg["files"].items():
    if not os.path.exists(name): sh(f"curl -sSf -o {name} '{url}'")
font = "/usr/share/fonts/truetype/higgsfield/Montserrat-ExtraBold.ttf"
if os.path.exists(font): shutil.copy(font, "Montserrat-ExtraBold.ttf")

segs, speed, GAP = cfg["segments"], cfg.get("speed", 1.0), 0.12
t, starts = 0.0, []
for i, s in enumerate(segs):
    sh(f"ffmpeg -v error -y -i {s['vo']} -af atempo={speed},apad=pad_dur={GAP} -ar 44100 -ac 1 seg{i}.wav")
    s["d"] = dur(f"seg{i}.wav"); starts.append(t); t += s["d"]
open("a.txt", "w").write("".join(f"file 'seg{i}.wav'\n" for i in range(len(segs))))
sh("ffmpeg -v error -y -f concat -safe 0 -i a.txt -c copy vo.wav")
total = t + 0.25

words, chunk = [], 0
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
for i, s in enumerate(segs):
    res, _ = m.transcribe(f"seg{i}.wav", language="ru", word_timestamps=True)
    ws = [w for r in res for w in r.words]
    for k, w in enumerate(ws):
        if k % 3 == 0: chunk += 1
        words.append({"s": round(starts[i] + w.start, 3), "e": round(starts[i] + w.end, 3), "w": w.word.strip(), "chunk": chunk})

MOVES = [(1.0, 1.14, .5, .5), (1.2, 1.04, .5, .38), (1.05, 1.18, .45, .6), (1.16, 1.02, .55, .5)]
ov, out, k = cfg.get("overlays", {}), [], 0
for i, s in enumerate(segs):
    n = max(1, round(s["d"] / 2.6)); pd = s["d"] / n; shots = []
    for j in range(n):
        img = s["imgs"][j % len(s["imgs"])]
        z0, z1, fx, fy = MOVES[k % len(MOVES)]; k += 1
        if i == 0 and j == 0: z0, z1, fx, fy = 1.0, 1.12, .42, .56
        if ov.get(img) == "circle": fx, fy = .42, .56  # держим «кнопку» в кадре
        shots.append({"img": img, "start": round(starts[i] + j * pd, 3), "dur": round(pd, 3), "z0": z0, "z1": z1,
                      "fx": fx, "fy": fy, "overlay": ov.get(img), "shake": bool(s.get("shake") and j == 0)})
    out.append({"start": round(starts[i], 3), "dur": round(s["d"], 3), "title": s.get("title", ""),
                "color": s.get("title_color", "red"), "fx": s.get("fx"), "subs": s.get("subs", True), "shots": shots})

# SFX
sh("sox -n -r 44100 -c 1 whoosh.wav synth 0.4 pinknoise band 2200 1800 fade q 0.12 0.4 0.25 gain -4")
sh("sox -n -r 44100 -c 1 pop.wav synth 0.09 sine 950:320 fade 0 0.09 0.07 gain -3")
sh("sox -n -r 44100 -c 1 buzz.wav synth 0.32 square 140 fade 0 0.32 0.06 gain -16")
sh("sox -n -r 44100 -c 1 ding.wav synth 0.7 sine 1568 synth 0.7 sine mix 2093 fade 0 0.7 0.65 gain -9")
sh("sox -n -r 44100 -c 1 boom.wav synth 0.55 sine 90:32 fade 0 0.55 0.5 gain -1")
sfx = [{"file": "boom.wav", "t": 0.0, "vol": 0.9}, {"file": "buzz.wav", "t": 0.5, "vol": 0.5}, {"file": "pop.wav", "t": 0.5, "vol": 0.5}]
for i, s in enumerate(out):
    if i: sfx += [{"file": "whoosh.wav", "t": s["start"] - 0.15, "vol": 0.55}, {"file": "pop.wav", "t": s["start"] + 0.05, "vol": 0.6}]
    if s["fx"] == "counter": sfx.append({"file": "ding.wav", "t": s["start"] + 1.35, "vol": 0.5})
    if s["fx"] == "stamp": sfx.append({"file": "boom.wav", "t": s["start"] + 0.45, "vol": 0.8})
    if s["fx"] == "save": sfx.append({"file": "ding.wav", "t": s["start"] + 0.35, "vol": 0.45})
    if any(sh_["overlay"] == "receipt" for sh_ in s["shots"]): sfx.append({"file": "pop.wav", "t": s["start"] + 0.3, "vol": 0.5})

json.dump({"total": round(total, 3), "segments": out, "words": words, "sfx": sfx}, open("timeline.json", "w"), ensure_ascii=False)
print("prep ok", round(total, 1), "s,", len(words), "words")
