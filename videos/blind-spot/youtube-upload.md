# 📤 YouTube — карточка №7 «You Go Blind Several Times a Second — And Never Notice»

Хронометраж ~11:00. Стиль Clinical v2. Голос **Cillian** (тихий, интимный, тревожный — как задано в script.md).
Формула (та же, что у видео №6): **спрятать механику, продать чувство + self-test во время просмотра → комменты + Shorts.**

> Примечание по инструменту: vidiq_score_thumbnail / vidiq_generate_titles не отработали в этой сессии («Not enough credits» — баланс vidIQ исчерпан). Оценки превью и заголовков ниже — экспертные (по правилам CTR-упаковки из системного промпта: контраст, один фокус, эмоция, curiosity gap), не автоматический скоринг vidIQ. Как только кредиты пополнятся — прогнать те же 4 превью и 4 заголовка через vidiq_score_thumbnail / vidiq_score_title для количественной проверки.

## ФОРМУЛА (канон залетевших — применяем ниже)
1. Заголовок 6–10 слов, про «ТЕБЯ», прячем ответ-механику (saccadic suppression / blind spot называем не в заголовке), продаём странность/физическое ощущение («ты слепнешь прямо сейчас»).
2. Описание: хук-абзац (ты слепнешь, читая ЭТО описание) → абзац сути с named-концептами (saccadic suppression, blind spot / optic disc, Mariotte 1668) → таймстампы по 10 блокам → SOURCES → хэштеги.
3. Теги: широкие (neuroscience/psychology/perception) + точечные (saccadic masking, blind spot, mariotte, saccades).
4. Category = Entertainment. Кастом-превью. Self-test во время просмотра = вовлечённость + комменты с числом.

---

## Заголовок (выбран — рабочее название канала подтверждено)
```
You Go Blind Several Times a Second — And Never Notice
```
A/B-запас: `You're Going Blind Right Now (And You'll Never Notice)` · `The Blind Spot You've Never Once Seen` · `Your Brain Is Deleting What You See`

Экспертная прикидка по CTR-принципам (front-load хука, длина для mobile ~50 симв., curiosity gap):
- **Основной** — "You Go Blind Several Times a Second" грузится в первые ~37 симв. до обрезки на мобильном, сам хук уже шокирующий и самодостаточный; "And Never Notice" — usил. твист. Сильно, специфично, не кликбейт (видео реально это доказывает через self-test).
- `You're Going Blind Right Now` — короче (28 симв.), ещё резче, но менее специфично («blind right now» может читаться как медицинская паника — риск неверных ожиданий).
- `The Blind Spot You've Never Once Seen` — фокус только на второй половине темы (слепое пятно), теряет саккады; хорошо для A/B, если проседает retention на первой половине.
- `Your Brain Is Deleting What You See` — сильный твист-заголовок (ближе к сути видео — не blur, а deletion), можно тестировать после недели на основном.

## Превью — 4 сгенерированных варианта (higgsfield z_image, 16:9, Clinical v2)

Стиль-префикс (как в image-prompts.md): бежевый фон #EFE7D6, чёрный контур, один красный акцент, тот же стикмен. Текст — крупно, 2-3 слова, играет на теме «исчезающей точки / слепого пятна / красной вспышки-обрыва», НЕ дублирует заголовок дословно (curiosity gap с заголовком, а не повтор).

### A «GONE» — ВЫБРАН, основной
- Крупный план стикмена, глаза широко открыты в упор на зрителя; рядом с головой — красная точка застигнута в момент исчезновения (наполовину стёрта в бежевый фон). Текст **GONE** — гигантский, в нижней трети, последняя буква сама «стирается» в красный.
- URL: `https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_053148_577a157f-a2bd-4a30-bc4a-05bf3afbe4bb.png`
- **Экспертная CTR-оценка: 90/100.** Один явный фокус (лицо + исчезающая точка), максимальный контраст красный/бежевый, слово «GONE» не повторяет заголовок → создаёт отдельный крючок («что именно gone?»). Читается на 120px: одно слово, толстый шрифт, нижняя треть свободна от деталей лица.

### B «BLIND SPOT»
- Стикмен у большого зеркала в детальной ванной; в отражении на месте глаз — красный глитч-разрыв, у самого стикмена лицо спокойное. Текст **BLIND SPOT** сверху.
- URL: `https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_053156_b6b484ac-001c-42fe-bffc-bc1f06f11832.png`
- **Оценка: 76/100.** Твист с зеркалом хорош, но текст «BLIND SPOT» — прямое название темы, а не крючок; слабее curiosity gap, ближе к лейблу, чем к вопросу.

### C «YOU'RE BLIND»
- Крупный план лица стикмена в момент моргания; толстая красная цензур-полоса перекрывает глаза как глитч, остальное лицо спокойно и чётко. Текст **YOU'RE BLIND** сверху.
- URL: `https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_053222_8629af80-99b8-4e55-8001-cbd048bb0d16.png`
- **Оценка: 82/100.** Графически самый «стоп-скролл» вариант (цензур-полоса — сильный визуальный паттерн-интеррапт), но текст частично дублирует «go blind» из заголовка — небольшой минус за избыточность.

### D «CAN'T SEE THIS»
- Стикмен в профиль смотрит на крест слева; справа — красная точка растворяется в фоне (self-test слепого пятна). Текст **CAN'T SEE THIS** снизу.
- URL: `https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_053224_e75896b2-a48b-46f7-bcc5-5b876ae07afe.png`
- **Оценка: 88/100.** Парадокс-хук («не можешь это увидеть», пока смотришь ровно на это) — сильный самостоятельный крючок, отдельный от заголовка, плюс прямая отсылка к self-test блоку 7 сценария.

**Основное превью: A «GONE».** **A/B-запас для теста: D «CAN'T SEE THIS»** (второй по силе, другой визуальный сюжет — self-test вместо исчезающей точки крупным планом). C и B — резерв.

---

## Описание (EN) — хук-зеркало (ты слепнешь, читая ЭТО) + named-концепты + таймстампы + SOURCES
```
Hopefully you learn something new ☺️

Right now, reading this description, your eyes have already gone blind several times. Not blurred — blank. Your brain simply deleted those instants and never told you. You felt nothing, and you will never feel it, no matter how many times you try.

This video follows two gaps in your vision that you have never once caught red-handed. The first is saccadic suppression (also called saccadic masking) — the split-second blackout your brain forces on you 100,000 to 180,000 times a day, every time your eyes jump between words, faces, rooms. It is not motion blur. It is a deliberate shutdown, timed to begin before your eye even starts moving, targeting the one visual channel built to catch motion. The second is the blind spot — a patch on your retina with zero light-sensing cells, discovered by the French scientist Edme Mariotte in 1668 and used to make coins vanish in front of the royal court of Louis XIV. Both gaps are completely real. Neither one ever shows up as an empty patch, because your brain does not leave holes. It fills them, instantly, with a forecast dressed up as reality.

Then the twist that changes what "seeing" even means: your brain doesn't pause the picture during these gaps like a paused video. It deletes the frame, predicts what should be there, and hands you the forecast labeled as fact — a policy that runs thousands of times an hour, on every face you have ever loved.

Try the self-test while the video is still playing: close one eye, stare at a cross, and watch a dot disappear into a hole that has been sitting in your vision since before you were born — the same trick Mariotte showed a room full of nobles, 350 years ago.

So tell me — how many times do you think you just went blind, reading this description? Count it, and put the number below 👇

⏳ Chapters:
00:00 You're already blind (you just don't know it)
00:48 The jump has a name: saccade
01:53 The mirror trick that always fails
03:04 Not blur — a decision
04:12 The math of daily blindness
05:18 What every stranger knows about your own face
06:26 Find your blind spot right now
07:33 You never watched a recording
07:58 The twist: forecast, not fact
09:38 What's actually in front of you

New videos every week. Subscribe → @whyyou-win

━━━━━━━━━━━━━━━━━━━━
SOURCES
━━━━━━━━━━━━━━━━━━━━
▸ Matin, E. (1974). "Saccadic suppression: A review and an analysis." Psychological Bulletin, 81(12), 899–917.
▸ Volkmann, F. C. (1986). "Human visual suppression." Vision Research, 26(9), 1401–1416.
▸ Idrees, S., et al. (2020). "Perceptual saccadic suppression starts in the retina." Nature Communications, 11, 1977.
▸ Wikipedia: "Saccadic masking" — overview of active neural suppression during eye movements.
▸ Mariotte, E. (1668). Nouvelle découverte touchant la vue, communicated to the Royal Society; translated in Philosophical Transactions. Historical account: "Edme Mariotte (1620–1684): Pioneer of Neurophysiology," ScienceDirect / PubMed 17574069.
▸ Linda Hall Library, "Scientist of the Day — Edmé Mariotte" — historical account of the blind-spot demonstration at the court of Louis XIV.
▸ Ramachandran-style perceptual filling-in literature on the blind spot; e.g. Scholarpedia, "The Blind Spot," and subsequent filling-in studies (Journal of Vision).
▸ Daily saccade count and blackout-time estimates: secondary science summaries citing ~100,000–180,000 saccades/day; daily "blind time" estimates disputed, ranging roughly 30–40 minutes to ~2 hours.

#neuroscience #psychology #perception #blindspot #saccades #brain #science #mindblown
```

## Теги
```
saccadic masking, saccadic suppression, blind spot, blind spot test, optic disc, saccades, eye movement, visual perception, perception, brain glitch, mariotte, edme mariotte, vision science, neuroscience, psychology, brain science, filling in illusion, self test, you go blind, mind blown
```

## Настройки при загрузке
- Видео: `blind-spot.mp4` · Язык English · **Not made for kids** ✅
- **Категория: Entertainment** (как у видео №6 — шире охват, чем Education)
- Плейлист: «Your Brain» / «Everyday Glitches»
- End screen: подписка + видео №6 (голос в голове) / №5
- Закреп-коммент: `So — how many times do you think you just went blind, reading this description? Count it, and put the number below 👇 (Bonus: did the dot disappear for you in the self-test? Tell me at what distance.)`
- 3 хэштега над заголовком: #neuroscience #psychology #blindspot

## 🔥 Тренды упаковки 2026 (поверх формулы)
- **Заголовок фактический, но с шоковым хуком** — не переименовываем механику в заголовок (saccadic suppression/blind spot остаются «спрятанным ответом» внутри видео), продаём ощущение «ты слепнешь прямо сейчас».
- **Текст на превью — 2–3 слова, огромным**, отдельный крючок от заголовка (не дублируем «blind» дважды буквально — GONE и CAN'T SEE THIS работают как парадокс, а не повтор).
- **Первые 3 сек = текст-хук на экране** (караоке-сабы): «Right now, your eyes are jumping across this sentence.»
- **Вертикальные Shorts обязательны** (3–5, разные хуки): «you just went blind reading this», «find your blind spot in 10 seconds», «the 1668 coin trick that still works on you», «your brain is lying to you right now». Разные заголовки/описания у каждого!
- **Хэштеги под тренд:** + #fyp #shorts #didyouknow для Reels/TikTok-дублей.
- **Pinned-коммент сразу** + ответ на первые 10 комментариев с числом «сколько раз ты ослеп» — алгоритм 2026 сильно весит ранние ответы и числовые комменты (легко агрегировать в Community-пост позже).

## RU-вариант
Заголовок: `Ты слепнешь по несколько раз в секунду — и не замечаешь`
Закреп: `Так сколько раз ты, по-твоему, только что ослеп, читая это описание? Посчитай и напиши число ниже 👇 (Бонус: точка исчезла в тесте? На каком расстоянии?)`
