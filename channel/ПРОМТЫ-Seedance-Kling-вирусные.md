# 🎬 ПРОМТЫ для Seedance / Kling: форматы, которые сейчас залетают

> Собрано 2026-10-20 по выбросам TikTok и Reels (vidiq, последние ~30 дней, от 300K просмотров).
> «x» = во сколько раз ролик обогнал медиану своего автора. Это и есть «залёт», а не просто большой канал.
> Промты на английском (модели понимают его лучше всего). Пояснения на русском.

---

## 0. Как пользоваться (30 секунд)

| Что | Куда |
|---|---|
| **Модель №1** | **Seedance 2.0** (Higgsfield / Dreamina), mode `std`, 720p или 1080p. На нём сделан ролик на 28M |
| **Модель №2** | **Kling 3.0** (или Kling 3.0 Omni с `multi_shots`): лучше всего физика и POV-движение |
| Бюджетно / тест | Seedance 2.0 Mini или Kling 3.0 Turbo: сначала гоняем черновик, потом финал на std/pro |
| Формат | **9:16**, 10–15 сек, звук **ON** (нативный звук тоже часть залёта: эмбиент, гул, SFX) |
| Текст на экране | **НЕ просим модель писать текст**: она его коверкает. Хук-текст ставим в CapCut (дан к каждому промту) |
| Луп | Последний кадр ≈ первый: зритель пересматривает, и для алгоритма это x2 к удержанию |

**Структура любого промта (держи её, когда пишешь свои):**
`[Камера/ракурс] + [Субъект + действие] + [Окружение] + [Свет/время] + [Движение камеры] + [Стиль/плёнка] + [Звук]`
Для мульти-шота на Seedance пиши таймкоды: `Shot 1 (0–3s): … Shot 2 (3–7s): …`

**Негатив (дописывай в конец или в поле negative):**
`no text, no subtitles, no watermark, no logos, no extra fingers, no morphing faces, no cartoon look`

---

## 📊 Что залетает прямо сейчас (основа для промтов)

| # | Формат | Пример (просмотры, обгон медианы) | Подходит нашей нише? |
|---|---|---|---|
| A | **POV-падение в космический объект** + цифры глубины | «POV: you fall into Jupiter» **43.2M** (32x) · «What if you fell into a black hole» 1.2M | ✅✅ идеально (Space/Existential) |
| B | **Гипнотический космо-луп + 1 вопрос текстом** | Чёрная дыра, 10 сек: **6.1M** (745x) · «If gravity bends time, does the future already exist?» 1.6M (70x) | ✅✅ делается за час |
| C | **«What if» симуляция со счётчиком** | «What if a black hole was heading for Earth» **3.6M** (141x) · «What if a star exploded near Earth» 2.2M · «What if every woman disappeared» **15.6M** | ✅✅ |
| D | **POV: просыпаешься в другой эпохе / месте** | «Carboniferous swamp 314M years ago» **10.7M** (35x) · «Empire State ironworker 1930» 2.3M · «Medieval farmer» 796K (85x) | ✅ (время / экзистенция) |
| E | **Последний человек на Земле / все исчезли** | «Last human on Earth, year 10» 1.4M (32x) · «Everyone vanished but two» 697K | ✅✅ |
| F | **Невозможный масштаб / сюрреал** | Девушка ловит сетью айфоны из моря (Seedance 2.0) **28.1M** · Вертолёты несут бетономешалки **7.8M** (98x) | ⚠️ вирусно, но вне ниши. Для охвата и тестов |
| G | **Загадочная находка с дрона** | «Noah's Ark in the mountain» **5.9M** (18x) | ✅ (мистика) |
| H | **Исторический персонаж в современности (монтаж)** | «Cleo VOL.2» (Клеопатра в спорткарах, баскетбол) **4.7M** (246x) | ⚠️ для охвата, хорошо для Shorts-аккаунта |

**Вывод:** под наш канал в первую очередь берём **A, B, C, E**: они в нише, у них высокий RPM, и они легко режутся из длинных видео. **F/H** используем как «трафик-магниты» на отдельных Shorts.

---

## A. POV-падение (самый мощный формат: 43M)

**Механика:** вид от первого лица, медленное погружение, в CapCut сверху меняются цифры (глубина / температура / давление). Финал: «и тут…» → обрыв → луп.

### A1. Падение в Юпитер
```
First-person POV of an astronaut falling feet-first into Jupiter's atmosphere. Shot 1 (0–4s): the gloved hands of the astronaut visible at the bottom of the frame, Jupiter's banded orange and cream clouds filling the view below, the Great Red Spot on the horizon. Shot 2 (4–9s): plunging through thick ammonia clouds, violent lightning flashes inside the clouds lighting up the visor, the visor slowly fogging. Shot 3 (9–14s): total darkness, deep red glow from below, the visor glass starting to crack with a thin line. Slow continuous downward motion, slight camera shake, photorealistic, IMAX documentary look, volumetric clouds. Sound: deep rumbling wind, distant thunder, muffled breathing inside a helmet.
```
**Текст в CapCut:** `POV: you fall into Jupiter` → счётчик `0 km · -110°C` → `1,000 km · 2,000°C` → `there is no ground.`

### A2. Падение в чёрную дыру
```
First-person POV from inside an astronaut helmet drifting toward a supermassive black hole. A glowing accretion disk of orange and white light bends around the black sphere, gravitational lensing warps the stars behind it. The astronaut's gloved hand reaches toward it in the foreground. The camera slowly accelerates forward, stars stretching into streaks, light turning blue at the edges. Photorealistic, Interstellar-style, cinematic, ultra detailed, slow motion. Sound: low sub-bass drone rising in pitch, quiet breathing, a heartbeat slowing down.
```
**Текст:** `What if you fell into a black hole?` → `Time outside: 1 year` → `Time outside: 1,000 years` → `Earth is gone.`

### A3. Падение на Солнце
```
First-person POV of a small spacecraft cockpit approaching the Sun. Through the window, the solar surface boils with granules and huge arching solar flares. The window glass glows orange, metal panels on the dashboard begin to warp and smoke. The camera pushes slowly forward, intense lens flare, heat distortion waves across the image. Photorealistic, NASA SDO imagery look, cinematic. Sound: deep roaring plasma, metal creaking, alarm beeping faintly.
```

### A4. Погружение в Марианскую впадину (бонус: тоже «падение», огромные охваты)
```
First-person POV inside a tiny deep-sea submersible descending into the Mariana Trench. Shot 1 (0–4s): blue sunlight fading above, bubbles rising past the round porthole. Shot 2 (4–9s): pitch black, only the headlights cutting through floating marine snow, a strange translucent creature drifts past the glass. Shot 3 (9–14s): the porthole glass shows a tiny crack, a faint huge silhouette moves in the darkness beyond the light. Slow descent, slight vibration, photorealistic, documentary. Sound: hull creaking under pressure, sonar pings, muffled heartbeat.
```
**Текст:** `0 m` → `4,000 m` → `10,935 m · 1,086 atmospheres` → `something is down here.`

---

## B. Космо-луп + один вопрос (6.1M за 10 секунд, делается за час)

**Механика:** один красивый зацикленный кадр, никакой озвучки, только эмбиент + один экзистенциальный вопрос крупным текстом. Люди пишут ответы в комменты, а это сигнал алгоритму.

### B1. Чёрная дыра (луп)
```
A massive black hole slowly rotating in deep space, a thin glowing accretion disk of gold and white plasma, gravitational lensing bending the light of the stars around it into rings. Static camera, very slow rotation, perfectly seamless loop, the last frame matches the first. Photorealistic, ultra detailed, cinematic, dark background, high contrast. Sound: ethereal, low synth drone.
```
**Текст:** `If gravity bends time… does the future already exist somewhere?`

### B2. Земля ночью с орбиты
```
View from low Earth orbit at night, slowly drifting over a continent covered in city lights, thunderstorms flashing with lightning inside the clouds, a thin green aurora on the horizon, the Milky Way above. Very slow forward drift, seamless loop, photorealistic, ISS footage look, 4K. Sound: soft ambient pad, distant radio static.
```
**Текст:** `Everyone you've ever loved is down there.`

### B3. Одинокий астронавт
```
A lone astronaut floating motionless in empty space, tethered to nothing, slowly spinning, the small blue Earth far behind, sunlight reflecting on the gold visor. Static camera, slow rotation, seamless loop, photorealistic, cinematic, minimalist composition, huge negative space. Sound: absolute silence broken by slow breathing.
```
**Текст:** `If you drifted away right now, you'd outlive every civilization on Earth.` (связка с видео №6 про тело в космосе)

### B4. Последняя звезда во Вселенной
```
The last dim red dwarf star in an empty, completely black universe, faint and flickering, no other stars around it. The camera slowly pulls away, the star getting smaller and smaller. Seamless loop, photorealistic, cosmic scale, melancholic, minimal. Sound: one low sustained note fading.
```
**Текст:** `In 100 trillion years, this will be the last light in the universe.`

### B5. Песочные часы с галактикой
```
A giant hourglass floating in space, instead of sand a spiral galaxy is slowly pouring through its narrow neck, stars falling like grains. Slow orbiting camera, seamless loop, surreal, photorealistic, cinematic lighting, deep blue and gold palette. Sound: soft ticking blended with an ambient drone.
```
**Текст:** `Why does time only go forward?` (тема из банка тем)

---

## C. «What if» симуляция со счётчиком (3.6M / 15.6M)

**Механика:** мирная сцена → в небе появляется угроза → в CapCut идёт обратный отсчёт расстояния / времени → эскалация → финальная фраза. Генерируем 3–4 клипа и склеиваем.

### C1. Чёрная дыра приближается к Земле (3 клипа)
```
Clip 1: A calm beach at sunset, people walking on the sand, a ferris wheel on the pier, a tiny black dot with a faint glowing ring appears in the sky above the horizon. Static wide shot, photorealistic, golden hour. Sound: waves, seagulls, then a faint low hum.

Clip 2: Same beach, now the black hole is huge in the sky, the ocean is pulled upward into a giant wave toward it, sand lifting off the ground, people looking up frozen. Slow push-in, photorealistic, dramatic. Sound: deep roaring, wind rising.

Clip 3: The horizon of the Earth bends and stretches into a glowing spiral, the beach, the ocean and the sky are pulled into the accretion disk in slow motion. Wide shot, cinematic, photorealistic. Sound: everything goes silent, one heartbeat.
```
**Текст:** `What if a black hole was heading for Earth?` → `1 light-year` → `1 AU` → `384,000 km` → `it wouldn't need to touch us.`

### C2. Звезда взрывается рядом (сверхновая)
```
A peaceful night landscape with a lake and mountains, the starry sky reflected in the water. One star in the sky slowly grows brighter and brighter until it is brighter than the Moon, casting sharp shadows, then it explodes into a blinding white flash that fills the whole sky. Static wide shot, photorealistic, cinematic. Sound: crickets, silence, then a deep pressure boom.
```
**Текст:** `What if a star exploded near Earth?` → `Day 1: night disappears` → `Year 1: …`

### C3. Все люди исчезли за секунду
```
Shot 1 (0–4s): A crowded Times Square at night, thousands of people, a countdown on the giant screens. Shot 2 (4–8s): in one frame all the people vanish, clothes and phones fall to the ground, cars keep rolling slowly with no drivers. Shot 3 (8–14s): aerial drone shot pulling up over the empty glowing city, a single dog walking in the middle of the street. Photorealistic, cinematic, night lights. Sound: crowd noise, then sudden total silence, a car horn in the distance.
```
**Текст:** `What if every human vanished at midnight?` → `Hour 1` → `Day 3: the lights go out` → `Year 50`

### C4. Земля перестала вращаться
```
A wide shot of a city at noon, then the sky suddenly freezes, clouds stop, a massive wall of wind and water sweeps horizontally across the city from left to right, trees and cars lifted sideways. Slow motion, photorealistic, disaster movie style, epic scale. Sound: a deafening roar of wind.
```
**Текст:** `What if Earth stopped spinning for one second?`

---

## D. POV: просыпаешься в другом времени (10.7M / 2.3M)

**Механика:** первое лицо, руки в кадре, «просыпание» → 4–6 сцен одного дня с таймстампами в CapCut. Формат: «таймлайн дня».

### D1. Каменноугольное болото, 314 млн лет назад (10.7M)
```
First-person POV gliding slowly at eye level through a misty prehistoric Carboniferous swamp, giant tree ferns and towering lycopsid trees, dark still water, a dragonfly with a one-meter wingspan flies past the camera, thick humid fog, green filtered light. Slow continuous forward motion, seamless loop, photorealistic, BBC documentary look. Sound: water sloshing, buzzing insects, distant strange calls.
```
**Текст:** `POV: you're trapped in a swamp 314 million years ago.` → `The air has 35% oxygen.`

### D2. Ты на Земле, когда упал астероид (66 млн лет назад)
```
First-person POV standing in a Cretaceous forest at dawn, the hands of the viewer pushing aside giant ferns, a herd of dinosaurs drinking at a river. A bright streak of fire appears in the sky and grows larger, the animals raise their heads, the light turns orange, a flash on the horizon. Photorealistic, cinematic, documentary. Sound: birdsong and insects, then a rising whistle, then a muffled boom.
```
**Текст:** `POV: it's the last morning of the dinosaurs.`

### D3. Первые часы на Марсе (колония)
```
First-person POV waking up inside a small Mars habitat, the gloved hands pull open a window shade revealing a red dusty landscape, a pale blue sunset, a rover parked outside. Shot 2: walking outside in a spacesuit, footprints in red dust, Earth visible as a tiny bright dot in the sky. Photorealistic, cinematic, The Martian look. Sound: suit breathing, wind, radio beeps.
```
**Текст:** `POV: you wake up on Mars in 2061.` → `06:00` → `09:30` → `Earth is 22 light-minutes away.`

### D4. Последний житель Помпей
```
First-person POV on a stone balcony in ancient Pompeii, the viewer's hands holding a clay cup, a busy Roman street below, Mount Vesuvius in the distance releasing a tall dark column of smoke that spreads into the sky like a pine tree. People in the street stop and look up. Photorealistic, cinematic, warm afternoon light. Sound: market chatter, a dog barking, then a deep distant rumble.
```
**Текст:** `POV: Pompeii, 24 August, 79 AD, 1:00 PM.`

---

## E. Последний человек на Земле (экзистенциальный хит)

### E1. Год 10 в одиночестве
```
A lone man walking through an overgrown empty city, Times Square covered with vines and moss, deer grazing between rusted cars, faded billboards, a soft morning fog. He carries a backpack and stops to look at a cracked screen. Slow tracking shot from behind, photorealistic, melancholic, The Last of Us look, soft natural light. Sound: birds, wind, quiet piano.
```
**Текст:** `What if you were the last human on Earth?` → `Year 10.`

### E2. Последний сигнал
```
A dark abandoned radio station on a mountain at night, a single person sitting in front of glowing old radio equipment, speaking into a microphone, the stars outside the window, a small red light blinking. Slow push-in from behind, photorealistic, cinematic, lonely, cold blue light with one warm lamp. Sound: radio static, a quiet voice, no answer.
```
**Текст:** `Day 4,380. Still no answer.`

### E3. Земля через 1000 лет без людей
```
Aerial drone shot slowly flying over the ruins of a megacity a thousand years after humans disappeared, skyscrapers broken and covered in forest, a river running through the streets, a bridge collapsed into the water, flocks of birds. Slow cinematic flyover, photorealistic, golden hour, epic scale. Sound: wind, birds, distant waterfall.
```
**Текст:** `How long until Earth forgets us?`

---

## F. Невозможный масштаб / сюрреал (28M: трафик-магнит, вне ниши)

### F1. Море из предметов (формат ролика Seedance 2.0 на 28M)
```
A woman standing on a wooden dock at a tropical beach scoops shiny new smartphones out of the turquoise water with a large fishing net, the whole sea is made of thousands of floating phones glittering in the sun. Then she rides a jet ski across the sea of phones, phones splashing like water. Bright daylight, photorealistic, fun, high energy, smooth camera tracking. Sound: upbeat music, splashing.
```
*Меняй предмет: золотые монеты, кроссовки, LEGO, конфеты. Механика: «знакомое действие + невозможное количество предмета».*

### F2. Невозможная стройка (7.8M)
```
Three heavy helicopters lower concrete mixer trucks on cables over a giant bridge pier under construction high above a canyon, the trucks pour concrete in mid-air into the pier, workers in orange vests watching below. Wide establishing shot, then a closer detail shot of the concrete pouring. Photorealistic, documentary drone footage, daylight. Sound: helicopter rotors, construction noise.
```

### F3. Космический вариант сюрреала (наша ниша + механика F)
```
An astronaut standing on the surface of the Moon casts a fishing line into a pool of liquid stars, slowly pulling out a tiny glowing planet on the hook, Earth rising in the black sky behind him. Slow cinematic push-in, photorealistic, surreal, soft blue light. Sound: quiet ambient hum, a soft splash.
```

---

## G. Загадочная находка с дрона (5.9M)

### G1. Корабль в горах
```
Slow aerial drone shot over a snowy mountain ridge in thick fog revealing a gigantic ancient wooden ship wedged into the rocks, half covered in ice and snow, its hull cracked, much larger than any modern ship. The camera slowly descends toward it. Photorealistic, cinematic, mysterious, overcast light. Sound: wind, low eerie drone.
```

### G2. Объект на дне океана
```
Slow underwater drone shot gliding over the dark ocean floor, the flashlight beam reveals a gigantic perfectly smooth black monolith standing upright in the sand, covered in strange geometric engravings, much taller than the camera can see. Photorealistic, cinematic, mysterious, deep blue. Sound: deep sonar ping, low hum.
```

### G3. Сигнал на Луне
```
Slow aerial shot gliding over the grey cratered surface of the Moon, revealing an ancient metallic structure half buried in moon dust, a faint light blinking on it, Earth hanging in the black sky. Photorealistic, NASA footage look, cinematic. Sound: radio static, a repeating faint beep.
```
**Текст:** `This has been blinking for 3 billion years.`

---

## H. Исторический персонаж в современности («Cleo VOL.2»: 4.7M, 246x)

**Механика:** один узнаваемый персонаж (Клеопатра / фараон / викинг / римский легионер) в 6–10 быстрых сценах современной жизни под ритмичный бит. Монтаж каждые 1–1.5 сек. Для узнаваемости персонажа во всех клипах используй **один референс-кадр** (Seedance 2.0 `image_references` / Kling Omni).

**Шаг 1: референс персонажа (картинка):**
```
Full-body portrait of Cleopatra, Egyptian queen, black bob hair with gold beads, heavy winged eyeliner, golden collar necklace, white linen dress, confident expression, standing in a neutral studio, photorealistic, cinematic lighting, 9:16.
```

**Шаг 2: сцены (каждая отдельной генерацией по 4–5 сек с референсом):**
```
1. Cleopatra slowly turns away from the camera in a luxury garage full of supercars, golden light, slow motion.
2. Cleopatra drives a gold sports car through a desert highway at sunset, pyramids in the background, tracking shot.
3. Cleopatra dunks a basketball in an empty arena, crowd gasping, slow motion, dramatic lighting.
4. Cleopatra orders coffee in a modern café, holding a stone tablet instead of a phone, barista confused.
5. Cleopatra walks a red carpet with paparazzi flashes, wearing sunglasses, confident walk.
6. Cleopatra sitting on a throne in a modern skyscraper office, city skyline behind her, looking at the camera.
```
*Стиль для всех: `photorealistic, cinematic, high-end commercial look, shallow depth of field, 9:16`. Звук OFF, музыку кладём в CapCut.*

---

## 🔁 Как из этого сделать конвейер

1. **Каждый длинный ролик → 3–5 Shorts в форматах A/B/C** по той же теме (например, видео №6 «тело в космосе» → A2 + B3 + C-вариант).
2. **Тест:** одна тема в 2 форматах (например, A и B) → через 48 ч смотрим удержание → масштабируем победителя.
3. **Свои промты по шаблону:** `What if / POV + [космический объект или эпоха] + [первое лицо или луп] + [один пугающий факт текстом]`.
4. Генерация: черновик на Mini/Turbo (дёшево) → лучший вариант перегенерить на Seedance 2.0 std / Kling 3.0 pro 1080p.

> Хочешь, сгенерирую первые 3–5 клипов прямо в Higgsfield (A2, B3, C1)? Просто скажи, какие номера.
