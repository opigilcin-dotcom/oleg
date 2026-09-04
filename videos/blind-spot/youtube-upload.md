# 📤 YouTube — карточка №7 «You Go Blind Several Times a Second — And Never Notice»

Хронометраж ~11:00. Стиль Clinical v2. Голос **Cillian** (тихий, интимный, тревожный — как задано в script.md).
Формула (та же, что у видео №6): **спрятать механику, продать чувство + self-test во время просмотра → комменты + Shorts.**

> Примечание по инструменту: vidiq_score_thumbnail / vidiq_generate_titles не отработали в этой сессии («Not enough credits» — баланс vidIQ исчерпан). Оценки превью и заголовков ниже — экспертные (по правилам CTR-упаковки из системного промпта: контраст, один фокус, эмоция, curiosity gap), не автоматический скоринг vidIQ. Повторная попытка в раунде 2 (варианты E-H) — снова «Not enough credits», не тратил больше времени на ретраи. Как только кредиты пополнятся — прогнать все 8 превью и 4 заголовка через vidiq_score_thumbnail / vidiq_score_title для количественной проверки.

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

## Превью — раунд 1: 4 варианта (higgsfield z_image, 16:9, Clinical v2, спокойный тон)

Стиль-префикс (как в image-prompts.md): бежевый фон #EFE7D6, чёрный контур, один красный акцент, тот же стикмен. Текст — крупно, 2-3 слова, играет на теме «исчезающей точки / слепого пятна / красной вспышки-обрыва», НЕ дублирует заголовок дословно (curiosity gap с заголовком, а не повтор).

### A «GONE» — базовый выбор раунда 1
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

---

## Превью — раунд 2: 4 усиленных варианта (higgsfield z_image, 16:9, Clinical v2 + эффекты/глитч/драма)

По запросу — те же правила бренда (бежевый #EFE7D6, чёрный контур, стикмен с круглой головой и точками-глазами, ОДИН красный акцент), но акцент теперь не спокойная точка, а **агрессивный рваный глитч-разрыв через кадр**, экстремальный крупный план лица/глаз с сильной эмоцией (шок/ужас), тёмная виньетка по краям, резкий свет/тень, текст с эффектом «исчезновения» (буквы частично съедены красным глитчем).

### E «IT'S GONE»
- Экстремальный крупный план — глаза и верхняя часть лица стикмена заполняют почти весь кадр, глаза раскрыты в шоке и ужасе. Диагональная красная трещина-глитч рвёт один глаз, из неё сочатся горизонтальные красные шумовые полосы. Тёмная виньетка со всех сторон держит взгляд на глазах. Текст **IT'S GONE** в нижней трети, правая часть слов буквально осыпается в красный глитч-шум.
- rawUrl: `https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_060133_8c520219-7fc7-4e84-9e9a-fde16f93d71f.png`
- **Экспертная CTR-оценка: 88/100.** Сильнейшая эмоция (шок крупным планом) и лучшая визуальная метафора темы (глаз буквально «трескается» ровно там, где рвётся зрение). Минус: апостроф + «осыпающиеся» буквы в правой части слова — небольшой риск читаемости на 120px именно этого фрагмента текста; смысл слова всё равно считывается по силуэту.

### F «CAN'T SEE»
- Экстремальный крупный план — только два глаза стикмена на весь кадр: один спокойный и целый, второй — с красной трещиной-глитч вместо зрачка, трещины расходятся по всей этой половине кадра. Тяжёлая тёмная виньетка. Текст **CAN'T SEE** в нижней трети, буквы у «разбитого» глаза съедены красным статик-шумом.
- rawUrl: `https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_060138_c5a0b499-3678-4c14-aef4-c06fd1cac91f.png`
- **Экспертная CTR-оценка: 90/100.** Композиция «один глаз цел — второй разбит» в одном кадре сама по себе рассказывает историю без текста (сильнейший визуальный сторителлинг, до-и-после без слов) — это самый «умный» кадр из четырёх. Текст читается лучше, чем в E, т.к. повреждена только половина слова у края.

### G «BLIND NOW»
- Крупный план лица стикмена анфас, рот приоткрыт в беззвучном крике, оба глаза широко раскрыты от ужаса. Через центр всего кадра — один массивный рваный красный разрыв (будто сама картинка порвана пополам), из краёв разрыва сыплются шумовые блоки. Текст **BLIND NOW** расположен ровно на линии разрыва, каждая буква частично «съедена» глитчем именно там, где её пересекает трещина.
- rawUrl: `https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_060140_31664754-71fd-47ef-9a63-962c8484f588.png`
- **Экспертная CTR-оценка: 87/100.** Самый физически драматичный кадр (разрыв через ВЕСЬ кадр, а не только глаз) — максимальный «стоп-скролл» эффект. Два минуса: (1) разрыв проходит через КАЖДУЮ букву текста, а не только часть слова — это самый высокий риск читаемости из четырёх на 120px; (2) «BLIND NOW» почти дословно повторяет «go blind» из заголовка — меньше самостоятельного curiosity gap, чем у остальных трёх.

### H «NO SIGNAL»
- Экстремальный крупный план шокированного лица стикмена на почти чёрном фоне (сильная виньетка). Толстые горизонтальные красные глитч-полосы и рваный статик-шум идут ровно по линии глаз — как у телевизора, теряющего сигнал. Несколько мелких фрагментов комнаты рассыпаются на глитч-блоки вокруг головы. Текст **NO SIGNAL** в нижней трети, часть букв с одной стороны заменена красными статик-блоками.
- rawUrl: `https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_060143_a204fdcb-91fc-44d6-a62c-c7a74bc24bb9.png`
- **Экспертная CTR-оценка: 92/100.** Лучший вариант раунда 2 и лучший из всех восьми. Причины: (1) сильнейший curiosity gap — «NO SIGNAL» не повторяет ни слова «blind», ни слова из заголовка, зритель обязан кликнуть, чтобы понять связь с «ты слепнешь»; (2) метафора ТВ-помех — самая точная визуализация именно saccadic suppression (мозг буквально «теряет сигнал» на долю секунды) — точнее передаёт суть видео, чем исчезающая точка (A) или разрыв (G); (3) повреждена только ОДНА сторона текста, а не всё слово или его правая половина как в E/G — лучшая читаемость на 120px среди «глитч»-вариантов; (4) один явный фокус (лицо в центре, чёрная виньетка гарантированно тянет взгляд туда).

**Итог по 8 вариантам, честно:** новые варианты (раунд 2) в среднем сильнее по эмоции/драме, но с реальной ценой — текст с «эффектом исчезновения» частично жертвует мгновенной читаемостью ради метафоры. С учётом этого компромисса:

- **Новый рекомендуемый основной: H «NO SIGNAL» (92/100)** — обгоняет A «GONE» (90/100) за счёт более сильного curiosity gap (не повторяет «blind» вообще) и более точной метафоры темы, при этом текст пострадал меньше всего среди глитч-вариантов.
- **A/B-запас #1 для теста: F «CAN'T SEE» (90/100)** — редкий случай, когда сама композиция (один глаз цел/один разбит) продаёт историю без текста; хорошо сработает как второй тест-вариант с иным типом крючка (сравнение, а не крупный план одного лица).
- **A/B-запас #2 (спокойный тон): A «GONE» (90/100)** — если H/F окажутся визуально «слишком шумными» на реальном фиде YouTube (у глитч-текста есть некоторый риск читаемости, который экспертная оценка не может проверить 100% без реального A/B на канале), откатываемся на A как проверенный спокойный вариант с тем же скором.
- Резерв: E (88), G (87), C (82), B (76).

## Превью — раунд 3: чёрный фон вместо бежевого (максимальный контраст с лентой)

Гипотеза: 90%+ превью в нише светлые/бежевые — чёрный фон физически выбивается из ленты сильнее любого текстового эффекта. Перегенерировали топ-4 концепта раунда 2 на глубоком чёрном фоне (вместо Clinical-бежевого), сохранив персонажа/красный акцент/крупный текст.

### I «NO SIGNAL» (чёрный фон)
- Прямой немигающий взгляд стикмена в упор на зрителя, почти чёрный фон, тяжёлая виньетка. Горизонтальные красные ТВ-помехи ровно по линии глаз. Текст **NO SIGNAL**, часть букв справа съедена красным статик-шумом.
- rawUrl: `https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_125033_fd4244d1-7da1-4be0-947c-c463aeeea85d.png`
- **Экспертная CTR-оценка: 94/100 — новый лидер.** Один явный фокус (прямой взгляд), максимальный физический контраст с лентой (чёрный среди бежевых/цветных конкурентов), метафора темы точнее всего (потеря сигнала = saccadic suppression), текст повреждён только с одной стороны — читаемость лучше всего среди глитч-вариантов.

### J «GONE» (чёрный фон)
- Тот же крупный план, красная точка у головы поймана в момент исчезновения в чёрном фоне. Текст **GONE**, последняя буква рассыпается в красные частицы.
- rawUrl: `https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_125036_6f8cb783-09a7-4285-97a0-9dcbf4693c40.png`
- **Оценка: 91/100.** Чище и спокойнее I, но менее драматично — хороший «спокойный» A/B-запас с тем же чёрным контрастом.

### K «CAN'T SEE» (чёрный фон)
- Split-композиция: крест слева, наполовину растворившаяся в черноте красная точка справа, глаз стикмена держит взгляд на кресте между ними.
- rawUrl: `https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_125037_a977b574-f6a7-4abd-a01b-8045dc207fc3.png`
- **Оценка: 89/100.** Как и в раунде 2 — два визуальных центра (крест + точка) слегка делят фокус на маленьком размере против I/J с одним лицом в центре.

### L «BLIND NOW» (чёрный фон)
- Лицо стикмена в беззвучном крике, рваная красная трещина через один глаз на чёрном фоне. Текст **BLIND NOW**, каждая буква рассечена трещиной.
- rawUrl: `https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_125042_a3dc5e36-b0f1-44f8-aaee-eaa47b68af8b.png`
- **Оценка: 88/100.** Самый драматичный, но текст всё ещё дублирует «blind» из заголовка (тот же минус, что и в раунде 2) — редкий кандидат в основные.

**Финал по всем 12 вариантам: I «NO SIGNAL» (чёрный фон, 94/100) — новый основной.** A/B-запас: H «NO SIGNAL» (бежевый, 92) — на случай если чёрный фон окажется слишком «мрачным» для органического охвата у нового канала; J «GONE» чёрный (91) — спокойный резерв.

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
- **Текст на превью — 2–3 слова, огромным**, отдельный крючок от заголовка (не дублируем «blind» дважды буквально — GONE, CAN'T SEE и NO SIGNAL работают как парадокс/метафора, а не повтор).
- **Первые 3 сек = текст-хук на экране** (караоке-сабы): «Right now, your eyes are jumping across this sentence.»
- **Вертикальные Shorts обязательны** (3–5, разные хуки): «you just went blind reading this», «find your blind spot in 10 seconds», «the 1668 coin trick that still works on you», «your brain is lying to you right now». Разные заголовки/описания у каждого!
- **Хэштеги под тренд:** + #fyp #shorts #didyouknow для Reels/TikTok-дублей.
- **Pinned-коммент сразу** + ответ на первые 10 комментариев с числом «сколько раз ты ослеп» — алгоритм 2026 сильно весит ранние ответы и числовые комменты (легко агрегировать в Community-пост позже).

## RU-вариант
Заголовок: `Ты слепнешь по несколько раз в секунду — и не замечаешь`
Закреп: `Так сколько раз ты, по-твоему, только что ослеп, читая это описание? Посчитай и напиши число ниже 👇 (Бонус: точка исчезла в тесте? На каком расстоянии?)`
