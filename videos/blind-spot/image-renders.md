# Image Renders — Video #7 "You Go Blind Several Times a Second — And Never Notice"

## ⚠️ ЭТО ЧЕРНОВОЙ ТЕСТ, НЕ ПОЛНЫЙ НАБОР КАДРОВ

Только 5 кадров из БЛОКА 1 (0:00, 0:06, 0:12, 0:18, 0:24) для проверки консистентности стиля Clinical v2 перед рендером всех ~95 кадров сценария. Остальные (~90) кадров ещё НЕ отрендерены — ждут approve стиля.

Model: `z_image` | aspect_ratio: `16:9` | count: 1 per frame

---

### [0:00] — стикмен читает текст, скачки-траектории от глаз к словам
- Job ID: `81aa88d6-9ffb-4c96-ad4e-3a0973c2cd6e`
- Raw: https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_052310_81aa88d6-9ffb-4c96-ad4e-3a0973c2cd6e.png
- Status: completed

### [0:06] — та же сцена, красная вспышка-обрыв на траектории
- Job ID: `27ffd2f7-68f0-4e49-85cb-b5a96b6e3af2`
- Raw: https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_052312_27ffd2f7-68f0-4e49-85cb-b5a96b6e3af2.png
- Status: completed

### [0:12] — лента кадров, скачки закрашены красным и убраны
- Job ID: `65607deb-9753-49c5-ac53-31ff5d73434d`
- Raw: https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_052314_65607deb-9753-49c5-ac53-31ff5d73434d.png
- Status: completed

### [0:18] — календарная лента от ребёнка до взрослого, мелкие красные метки
- Job ID: `9feb1ec4-ed62-45d0-805f-d98401761af4`
- Raw: https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_052318_9feb1ec4-ed62-45d0-805f-d98401761af4.png
- Status: completed

### [0:24] — стикмен пожимает плечами, ни одной красной метки
- Job ID: `8193ba5f-f108-45ee-ab05-9392547afbd9`
- Raw: https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_052326_8193ba5f-f108-45ee-ab05-9392547afbd9.png
- Status: completed
- Note: this frame's first attempt hit a `429 rate_limit_reached` from the z_image backend and was retried; the retry succeeded.

---

## Что дальше
Посмотри на эти 5 кадров — проверь:
1. Персонаж (стикмен, круглая голова, точки-глаза) визуально одинаковый во всех 5.
2. Палитра держится (бежевый/серый/коричневый/кость), без лишних цветов.
3. Красный акцент читается там, где он есть (0:06, 0:12, 0:18), и отсутствует там, где его не должно быть (0:00, 0:24).
4. Фон детальный и разный в каждом кадре, но не отвлекает от персонажа.

Если стиль устраивает — можно запускать рендер оставшихся ~90 кадров из `image-prompts.md` (блоки 1 (остаток) - 10) тем же способом (`z_image`, `16:9`).
