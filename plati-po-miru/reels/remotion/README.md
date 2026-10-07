# PRO-монтаж рилсов (Remotion)

Что делает: хук с ударным наездом и тряской, обводка «ловушки» на кадре, плашки-заголовки со spring-ударом,
субтитры по словам (текущее слово жёлтое, «прыгает»), счётчик цены, штамп, подсказка «Сохрани»,
переходы со вспышкой и blur, полоса прогресса, закольцованный финал, SFX (boom/buzz/whoosh/pop/ding).

1. `npm install`
2. `python3 prep.py ../<папка-рилса>/reel.json` — скачивает кадры/голос, Whisper-тайминги, SFX → `public/timeline.json`
3. `npx remotion render src/index.ts Reel out/raw.mp4 --concurrency=6 --crf=20`
4. `ffmpeg -i out/raw.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k out/final.mp4`

Поля сегмента в reel.json: `title`, `title_color` (red/blue/green/yellow), `fx` (counter/stamp/save), `shake`, `subs`.
`overlays`: картинка → `circle` (обвести кнопку) / `receipt` (подсветить строку чека). Координаты оверлеев — в `src/Reel.tsx`.
Рендерили в песочнице Higgsfield (8 CPU): ~1,5 мин на 34-секундный рилс.
