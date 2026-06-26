# build-video.ps1 — собирает ru.mp4 и en.mp4 из кадров + озвучки
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$dest = Join-Path $env:USERPROFILE 'Desktop\стикмэн'
if (-not (Test-Path $dest)) { Write-Host "Папка $dest не найдена. Сначала запусти скачивалку."; Read-Host; exit }
Set-Location $dest
Write-Host "Рабочая папка: $dest"

# --- 1. Найти или скачать ffmpeg ---
$ff = $null
try { ffmpeg -version *> $null; $ff = 'ffmpeg' } catch { }
if (-not $ff) {
  if     (Test-Path '.\ffmpeg.exe')          { $ff = '.\ffmpeg.exe' }
  elseif (Test-Path '.\ffmpeg\bin\ffmpeg.exe') { $ff = '.\ffmpeg\bin\ffmpeg.exe' }
  else {
    Write-Host "ffmpeg не найден — скачиваю (~80 МБ, один раз)..."
    Invoke-WebRequest 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg.zip'
    Expand-Archive 'ffmpeg.zip' -DestinationPath 'ffmpeg_tmp' -Force
    $exe = Get-ChildItem 'ffmpeg_tmp' -Recurse -Filter 'ffmpeg.exe' | Select-Object -First 1
    New-Item -ItemType Directory -Force '.\ffmpeg\bin' | Out-Null
    Copy-Item $exe.FullName '.\ffmpeg\bin\ffmpeg.exe' -Force
    Remove-Item 'ffmpeg.zip','ffmpeg_tmp' -Recurse -Force
    $ff = '.\ffmpeg\bin\ffmpeg.exe'
  }
}
Write-Host "ffmpeg: $ff"

# --- 2. Данные кадров и таймкодов ---
$frames = @('0-00.png','0-03.png','0-06.png','0-08.png','0-11.png','0-14.png','0-16.png','0-19.png','0-22.png','0-25.png','0-27.png','0-31.png','0-34.png','0-39.png','0-42.png','0-46.png','0-49.png','0-52.png','0-55.png','0-58.png','1-01.png','1-04.png','1-08.png','1-11.png','1-14.png','1-18.png','1-21.png','1-25.png','1-28.png','1-32.png','1-36.png','1-39.png','1-41.png','1-44.png','1-48.png','1-51.png','1-54.png','1-57.png','2-00.png','2-03.png','2-06.png','2-09.png','2-12.png','2-14.png','2-17.png','2-20.png','2-23.png','2-27.png','2-31.png','2-34.png','2-37.png','2-41.png','2-43.png','2-46.png','2-50.png','2-53.png','2-56.png','2-58.png','3-00.png','3-02.png','3-05.png','3-08.png','3-11.png','3-14.png','3-16.png','3-18.png','3-22.png','3-25.png','3-28.png','3-31.png','3-34.png','3-36.png','3-40.png','3-43.png','3-46.png','3-50.png','3-53.png','3-56.png','3-58.png','4-01.png','4-04.png','4-08.png','4-11.png','4-14.png','4-18.png','4-21.png','4-25.png','4-28.png','4-31.png','4-33.png','4-36.png','4-40.png','4-43.png','4-46.png','4-50.png','4-53.png','4-57.png','5-00.png','5-03.png','5-07.png','5-10.png','5-14.png','5-16.png','5-19.png','5-23.png','5-27.png','5-30.png','5-33.png','5-36.png','5-40.png','5-43.png','5-47.png','5-50.png','5-53.png','5-57.png','6-00.png')
$raw    = @(3,3,2,3,3,2,3,3,3,2,4,3,5,3,4,3,3,3,3,3,3,4,3,3,4,3,4,3,4,4,3,2,3,4,3,3,3,3,3,3,3,3,2,3,3,3,4,4,3,3,4,2,3,4,3,3,2,2,2,3,3,3,3,2,2,4,3,3,3,3,2,4,3,3,4,3,3,2,3,3,4,3,3,4,3,4,3,3,2,3,4,3,3,4,3,4,3,3,4,3,4,2,3,4,4,3,3,3,4,3,4,3,3,4,3,3)
$rawsum = 363

# --- 3. Длины озвучки (секунды) ---
$audio = @{
  ru = @{ parts = @('ru-1.mp3','ru-2.mp3','ru-3.mp3','ru-4.mp3','ru-5.mp3','ru-6.mp3'); dur = 462.08 }
  en = @{ parts = @('en-1.mp3','en-2.mp3','en-3.mp3','en-4.mp3','en-5.mp3');            dur = 412.08 }
}

foreach ($lang in @('ru','en')) {
  $parts = $audio[$lang].parts
  $adur  = $audio[$lang].dur

  # пропустить язык, если файлов нет
  $missing = $parts | Where-Object { -not (Test-Path $_) }
  if ($missing) { Write-Host "[$lang] пропускаю — нет файлов: $($missing -join ', ')"; continue }

  Write-Host "`n=== Сборка [$lang] ==="

  # 3a. склейка аудио
  $alist = "audio_$lang.txt"
  ($parts | ForEach-Object { "file '$_'" }) | Set-Content $alist -Encoding ASCII
  $full = "$lang-full.mp3"
  & $ff -y -f concat -safe 0 -i $alist -c copy $full

  # 3b. список кадров с растянутой длительностью
  $scale = $adur / $rawsum
  $ilist = "images_$lang.txt"
  $lines = New-Object System.Collections.Generic.List[string]
  for ($i=0; $i -lt $frames.Count; $i++) {
    $d = [math]::Round($raw[$i] * $scale, 3)
    $lines.Add("file '$($frames[$i])'")
    $lines.Add("duration $d")
  }
  $lines.Add("file '$($frames[$frames.Count-1])'")   # повтор последнего кадра
  $lines | Set-Content $ilist -Encoding ASCII

  # 3c. рендер
  $out = "$lang.mp4"
  & $ff -y -f concat -safe 0 -i $ilist -i $full `
    -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:white,fps=25,format=yuv420p" `
    -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest $out
  Write-Host "[$lang] готово -> $out"
}

Write-Host "`nВсё собрано. Файлы ru.mp4 и en.mp4 в папке стикмэн."
Read-Host "Нажми Enter чтобы закрыть"
