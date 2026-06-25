# 🖼️ ПРОМТ-ШАБЛОН: генерация картинок под YouTube-сценарий (GPT Image 2.0)

> Единый стиль для всего канала «Forbidden Earth». Один кадр на каждый таймкод. Стиль-код ниже добавляется к КАЖДОМУ промпту — так все картинки выглядят как один фильм.

---

## КАК ПОЛЬЗОВАТЬСЯ
1. Скопируй блок **«СИСТЕМНАЯ ИНСТРУКЦИЯ»** в начало запроса к GPT Image 2.0.
2. Для каждого таймкода собери промпт по формуле:
   **`<сцена этого кадра на английском>` + `,` + `<STYLE SUFFIX>`**
3. Тип кадра определяет, какой стиль-блок применить: `фотореал` (по умолчанию), `[AI-видео]` (кадр трактуй как кинематографичный стилл того же действия), `[карта]` (стиль карты, не фотореал), `TITLE/бейдж` (титр).
4. Везде 16:9 горизонталь. В конце — список NEGATIVE.

---

## СИСТЕМНАЯ ИНСТРУКЦИЯ (вставить один раз)
> You are generating a sequence of still frames for ONE cinematic history documentary on YouTube. Every frame must share the SAME visual style, grade, and era so the video feels seamless. One distinct frame per timecode, illustrating exactly what the narrator says at that moment. Horizontal 16:9 only. Clean, centered, readable, nothing important cropped. No on-image text unless explicitly a title card or a map label. Photoreal frames look like stills from a high-end documentary; map frames look like animated infographic cartography; title cards are typographic. Maintain consistency across all frames.

---

## ★ STYLE SUFFIX — ФОТОРЕАЛ (добавлять к каждому фотореал/[AI-видео] кадру)
```
cinematic photorealistic documentary still, shot on anamorphic lenses, shallow depth of field,
moody low-key lighting, desaturated teal-and-slate shadows with warm amber and rust-orange (#C8551B) highlights,
crushed blacks, soft film bloom, volumetric haze, fine 35mm film grain, gentle vignette, dust in the air,
period-accurate American West / Texas, eerie melancholic abandoned mood, wide cinematic framing,
rule of thirds, strong depth, single clear focal subject, generous negative space,
ultra detailed, high dynamic range, 16:9 horizontal, no text
```
**Эпоха по контексту:** 1830s–1950s. Современные объекты (машины, провода, асфальт, телефоны) — только если кадр прямо про современность (трасса, кнопка Subscribe).

**Люди:** мелко, силуэтами или со спины, лица не детализируем (faceless-friendly). Архивные сцены — выцветшая сепия с тонкой колоризацией.

---

## ★ STYLE-БЛОК — КАРТЫ `[карта]`
```
animated infographic map graphic, aged dark parchment / slate base, clean minimal cartography,
glowing rust-orange (#C8551B) routes, dots and labels, subtle paper grain, soft vignette,
NOT photorealistic, flat editorial documentary map style, crisp legible labels, 16:9 horizontal
```
Счётчики/таймлайны/рейтинги — в этом же стиле: тёмный фон, ржаво-оранжевые цифры, чистый минималистичный UI.

---

## ★ STYLE-БЛОК — ТИТРЫ / БЕЙДЖИ НОМЕРОВ
```
title card, solid near-black background, bold condensed serif typography centered,
rust-orange (#C8551B) text, subtle film grain and vignette, cinematic, 16:9 horizontal
```
Бейдж номера: огромная ржаво-оранжевая цифра, один и тот же шрифт во всём ролике, в углу/нижней трети поверх фотореал-кадра.

---

## ★ NEGATIVE (добавлять в конце каждого промпта)
```
--no vertical, square, cropped subject, cut-off heads, broken anatomy, extra limbs, deformed hands,
warped faces, gibberish text, misspelled signs, watermark, logo, modern cars/wires/phones (unless intended),
oversaturation, neon HDR look, cartoon, 3d render look (except maps), motion blur glitch, duplicated objects, lowres
```

---

## ФОРМАТ (жёстко)
- Только **16:9 горизонталь** (1920×1080+). Не вертикаль, не квадрат.
- Один отдельный, отличающийся кадр на каждый таймкод.
- Чистая композиция, важные объекты не обрезаны, без глитчей и нечитаемого текста.
- Единый грейд и эпоха во всех кадрах (один фильм).

---

## ФОРМУЛА ПРОМПТА НА КАДР
```
<что в кадре: субъект + действие + ракурс/движение камеры>, <тип-блок стиля>, <NEGATIVE>
```

### Готовые примеры (из сценария Texas Ghost Towns)

**[0:00] фотореал**
```
Aerial wide shot pushing over the Dallas skyline at dusk, transitioning to oil derricks pumping on an open Texas plain, golden backlight, [+ STYLE SUFFIX фотореал] [+ NEGATIVE]
```

**[0:09] [AI-видео] → трактуем как стилл того же действия**
```
A deserted 1880s frontier main street, empty storefronts, dust and a tumbleweed blowing through the frame, low evening sun, ghostly stillness, [+ STYLE SUFFIX фотореал] [+ NEGATIVE]
```

**[0:12] [карта]**
```
An old hand-drawn map of Texas on dark parchment, twelve small glowing rust-orange location dots scattered across the state, clean minimal labels, [+ STYLE-БЛОК КАРТЫ] [+ NEGATIVE]
```

**[0:18] [AI-видео] hero**
```
A massive hurricane storm surge smashing through a wooden 1870s Texas gulf port, ships thrown against docks, dark towering clouds, sea spray, a faint fire glow starting on the right, dramatic, [+ STYLE SUFFIX фотореал] [+ NEGATIVE]
```

**[0:24] TITLE**
```
Title card reading "12 TEXAS GHOST TOWNS", bold condensed serif, rust-orange on near-black, [+ STYLE-БЛОК ТИТРЫ] [+ NEGATIVE]
```

---

## КОНСИСТЕНТНОСТЬ (важно)
- **Фиксируй seed/style** между кадрами одного города, чтобы локации совпадали.
- Один и тот же шрифт для всех цифр-бейджей и титров.
- Один грейд (teal-slate + rust-orange) во всех 161 кадре.
- Если объект повторяется (та же школа Toyah, та же статуя Indianola) — описывай его одинаково дословно.
- Для лиц-крупняков избегай узнаваемых реальных людей: давай обобщённый период-тип.

---

## ИТОГ, который жду от модели:
По одному горизонтальному 16:9 изображению на каждый таймкод сценария, все в едином стиле «Forbidden Earth», строго иллюстрируя слова диктора в этот момент.
