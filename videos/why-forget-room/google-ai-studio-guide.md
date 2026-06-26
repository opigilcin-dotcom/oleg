# 🎙️ Google AI Studio (Gemini TTS) — методичка озвучки (крутой уровень)

Source research: blog.google, ai.google.dev, aitoolanalysis.com (2026).

## Что важно знать (факты 2026)
- **Модели:** Gemini 2.5 Flash TTS (быстро), 2.5 Pro TTS (качество), новейшая **3.1 Flash TTS** (лучше всех слушается стиль-промт). Для озвучки бери **Pro TTS** или **3.1 Flash TTS**.
- **Голоса:** 30+ (Charon — informative, Zephyr — bright, Puck — upbeat, Kore — firm, Fenrir — excitable, Aoede — breezy и др.). 70+ языков, включая RU и EN.
- **Управление = обычным текстом** (не нашими скобками). Можно задать тон, темп, шёпот, паузы, акценты словами.
- **Лимит:** 32k токенов на сессию (~24 000 слов). Наш сценарий ~1000 слов → **в один заход.**
- 🚨 **КОММЕРЦИЯ:** бесплатный выхлоп AI Studio **НЕ лицензирован** для коммерческого использования. Для монетизируемого YouTube нужен **платный Cloud Billing (Gemini API)**. Цена токенная, ~25 токенов/сек аудио — копейки за ролик.

---

## ШАГ 1. Модель и голос
- Модель: **Gemini 2.5 Pro TTS** (или 3.1 Flash TTS).
- Голос (стиль Zenn — спокойный любопытный объяснитель): начни с **Charon** (informative). Протестируй ещё 2: **Iapetus / Algenib** (если есть) или **Puck**. Один и тот же голос на весь ролик.

## ШАГ 2. Стиль-промт (вставляется в поле инструкции, НЕ в текст)

### EN style prompt
```
You are a warm, curious documentary narrator explaining a fascinating idea to one friend.
Default tone: calm, clear, serious but friendly. Pace about 150 words per minute.
Slow down and lower your voice on the insight lines and the reveals.
Lift slightly with emphasis on key reveals such as "the Doorway Effect" and "Four."
Take a short, natural pause at each paragraph break.
Stay conversational, never theatrical or like a movie trailer.
Read only the narration text below. Do not read these instructions aloud.
```

### RU стиль-промт
```
Ты — тёплый, любопытный документальный рассказчик, объясняешь интересную идею одному другу.
Базовый тон: спокойный, ясный, серьёзный, но дружелюбный. Темп около 150 слов в минуту.
Замедляйся и понижай голос на инсайтах и раскрытиях.
Делай лёгкий акцент на ключевых раскрытиях, например «эффект дверного проёма» и «Четыре».
Делай короткую естественную паузу на каждом разрыве абзаца.
Оставайся разговорным, без театральности и «голоса из трейлера».
Читай только текст ниже. Эти инструкции вслух не читай.
```

## ШАГ 3. Текст
Подавай **чистый текст** (без тегов): EN — `voiceover-clean (PART A)`, RU — `voiceover-flow-ru / clean`.
Абзацы = естественные паузы (стиль-промт это подхватит). Весь ролик за один запуск.

## ШАГ 4. Как это даёт «дорого»
- Стиль-промт переносит наши теги ([CALM]/[LOW]/[SLOW]/[EMPHASIS]) в инструкцию словами.
- Одна сессия = один голос, один грейд подачи → консистентно.
- Для России — отдельный запуск с RU-текстом и RU стиль-промтом.

## ШАГ 5. Коммерция (обязательно для монетизации)
- В AI Studio бесплатно — только для тестов/выбора голоса.
- Финальное аудио для канала рендерь через **Gemini API на платном Cloud Billing** (тот же голос/промт), тогда права на коммерческое использование есть.
