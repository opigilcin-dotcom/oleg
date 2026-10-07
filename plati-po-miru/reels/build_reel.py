#!/usr/bin/env python3
"""Собирает вертикальный рилс 1080x1920 из кадров + озвучки.
Запуск (в песочнице Higgsfield или локально с ffmpeg + faster-whisper):
  python3 build_reel.py reel.json
reel.json: {"files": {"имя": "url"}, "speed": 1.1, "segments": [
  {"vo": "file.mp3", "imgs": ["a.png", ...], "title": "ТЕКСТ\\nВ ДВЕ СТРОКИ", "title_color": "red", "subs": true}]}
"""
import json, os, subprocess, sys

W, H, FPS = 1080, 1920, 30
FONT = "Montserrat ExtraBold"
COLORS = {"red": "&H003B30FF", "blue": "&H00B67700", "black": "&H00000000", "yellow": "&H0000D7FF"}


def sh(cmd):
    subprocess.run(cmd, shell=True, check=True)


def dur(f):
    return float(subprocess.check_output(
        f"ffprobe -v error -show_entries format=duration -of csv=p=0 {f}", shell=True))


def ts(t):
    h, t = divmod(t, 3600); m, s = divmod(t, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


cfg = json.load(open(sys.argv[1]))
segs, speed = cfg["segments"], cfg.get("speed", 1.0)
for name, url in cfg.get("files", {}).items():
    if not os.path.exists(name):
        sh(f"curl -sSf -o {name} '{url}'")

# 1) озвучка: ускорение + пауза 0.12с после каждой фразы
GAP = 0.12
starts, t = [], 0.0
for i, s in enumerate(segs):
    sh(f"ffmpeg -v error -y -i {s['vo']} -af atempo={speed},apad=pad_dur={GAP} -ar 44100 -ac 1 seg{i}.wav")
    d = dur(f"seg{i}.wav"); starts.append(t); s["d"] = d; t += d
open("a.txt", "w").write("".join(f"file 'seg{i}.wav'\n" for i in range(len(segs))))
sh("ffmpeg -v error -y -f concat -safe 0 -i a.txt -c copy vo.wav")
total = t

# 2) слова с таймингами (faster-whisper), fallback — равномерно по сегменту
words = []
try:
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    for i, s in enumerate(segs):
        res, _ = m.transcribe(f"seg{i}.wav", language="ru", word_timestamps=True)
        for r in res:
            for w in r.words:
                words.append((i, starts[i] + w.start, starts[i] + w.end, w.word.strip()))
except Exception as e:
    print("whisper fallback:", e)
    for i, s in enumerate(segs):
        ws = s.get("text", "").split()
        step = (s["d"] - GAP) / max(len(ws), 1)
        for k, w in enumerate(ws):
            words.append((i, starts[i] + k * step, starts[i] + (k + 1) * step, w))

# 3) клипы: Ken Burns, смена плана каждые ~2.5с (длинный сегмент режется на под-клипы)
MOVES = [  # (z0, z1, fx, fy) — фокус в долях кадра
    (1.00, 1.12, .5, .5), (1.18, 1.04, .5, .35), (1.05, 1.17, .45, .6), (1.15, 1.02, .55, .5)]
clips, k = [], 0
for i, s in enumerate(segs):
    n = max(1, round(s["d"] / 2.6))
    parts = [s["d"] / n] * n
    for j, pd in enumerate(parts):
        img = s["imgs"][j % len(s["imgs"])]
        z0, z1, fx, fy = MOVES[k % len(MOVES)]
        if i == 0 and j == 0:
            z0, z1 = 1.25, 1.0  # хук: резкий наезд-отъезд
        frames = max(2, round(pd * FPS))
        z = f"{z0}+({z1}-{z0})*on/{frames}"
        vf = (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
              f"zoompan=z='{z}':x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)*{fy}':d={frames}:s={W}x{H}:fps={FPS},"
              f"eq=contrast=1.06:saturation=1.12,format=yuv420p")
        sh(f"ffmpeg -v error -y -loop 1 -i {img} -vf \"{vf}\" -frames:v {frames} -c:v libx264 -crf 18 -preset fast c{k}.mp4")
        clips.append(f"c{k}.mp4"); k += 1
open("v.txt", "w").write("".join(f"file '{c}'\n" for c in clips))
sh("ffmpeg -v error -y -f concat -safe 0 -i v.txt -c copy v.mp4")

# 4) субтитры ASS: заголовок сегмента сверху + слова по 3 с подсветкой текущего
ass = [
    "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    f"Style: Title,{FONT},104,&H00FFFFFF,&H00FFFFFF,&H003B30FF,&H003B30FF,-1,0,0,0,100,100,0,0,3,18,0,8,60,60,0,1",
    f"Style: Sub,{FONT},96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,7,3,5,60,60,0,1",
    "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
]
for i, s in enumerate(segs):
    if not s.get("title"):
        continue
    col = COLORS.get(s.get("title_color", "red"))
    txt = s["title"].replace("\n", "\\N")
    pop = "{\\fscx80\\fscy80\\t(0,120,\\fscx100\\fscy100)}"
    ass.append(f"Dialogue: 1,{ts(starts[i])},{ts(starts[i] + s['d'])},Title,,0,0,0,,"
               f"{{\\an8\\pos({W//2},300)\\3c{col}\\4c{col}}}{pop}{txt}")
SUBY = 1180
ev = []
for i, s in enumerate(segs):
    if not s.get("subs", True):
        continue
    ws = [w for w in words if w[0] == i]
    for c in range(0, len(ws), 3):
        chunk = ws[c:c + 3]
        for n, (_, a, b, w) in enumerate(chunk):
            end = chunk[n + 1][1] if n + 1 < len(chunk) else b + 0.05
            line = " ".join(("{\\c&H0000E5FF&}" + x[3].upper() + "{\\c&H00FFFFFF&}") if m_ == n else x[3].upper()
                            for m_, x in enumerate(chunk))
            ev.append([a, end, line])
ev.sort()
for n, (a, end, line) in enumerate(ev):
    if n + 1 < len(ev):
        end = min(end, ev[n + 1][0])  # одна строка субтитров на экране за раз
    ass.append(f"Dialogue: 0,{ts(a)},{ts(end)},Sub,,0,0,0,,{{\\an5\\pos({W//2},{SUBY})}}{line}")
open("subs.ass", "w").write("\n".join(ass) + "\n")

# 5) свуш на склейках сегментов
sh("sox -n -r 44100 -c 1 wh.wav synth 0.35 pinknoise band -n 2500 1500 fade q 0.02 0.35 0.25 gain -22 || true")
mix = "[1:a]volume=1.0[vo]"
inputs, labels = "", "[vo]"
if os.path.exists("wh.wav"):
    for i in range(1, len(segs)):
        ms = int(starts[i] * 1000) - 120
        inputs += " -i wh.wav"
        mix += f";[{i+1}:a]adelay={ms}|{ms}[w{i}]"
        labels += f"[w{i}]"
    mix += f";{labels}amix=inputs={len(segs)}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]"
else:
    mix += ";[vo]loudnorm=I=-14:TP=-1.5:LRA=11[a]"
out = cfg.get("out", "reel.mp4")
sh(f"ffmpeg -v error -y -i v.mp4 -i vo.wav{inputs} -filter_complex \"{mix}\" -map 0:v -map \"[a]\" "
   f"-vf \"ass=subs.ass\" -c:v libx264 -crf 19 -preset medium -profile:v high -pix_fmt yuv420p "
   f"-c:a aac -b:a 192k -ar 44100 -movflags +faststart -t {total:.2f} {out}")
# 6) обложка = первый кадр хука с заголовком
sh(f"ffmpeg -v error -y -ss 0.9 -i {out} -frames:v 1 -q:v 2 cover.jpg")
print("DONE", out, f"{total:.1f}s", len(words), "words")
