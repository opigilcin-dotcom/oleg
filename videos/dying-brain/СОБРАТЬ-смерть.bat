@echo off
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "$c=[IO.File]::ReadAllText('%~f0');$i=$c.LastIndexOf('#PSBODY#');iex $c.Substring($i+8)"
echo.
pause
exit /b
#PSBODY#
$ErrorActionPreference='Stop'
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
if(-not $dir){ $dir = (Get-Location).Path }
Set-Location -LiteralPath $dir
Write-Host ('Folder: '+$dir)

$framesDir = Join-Path $dir 'frames-death'
$audioDir  = Join-Path $dir 'audio-death'
if(-not (Test-Path $framesDir)){ Write-Host 'NO frames-death folder. Run СКАЧАТЬ-ВСЁ-смерть.bat first.'; return }
if(-not (Test-Path $audioDir)){ Write-Host 'NO audio-death folder. Run СКАЧАТЬ-аудио-смерть.bat first.'; return }

# find or download ffmpeg
$ff=$null
try{ ffmpeg -version *>$null; $ff='ffmpeg' }catch{}
if(-not $ff){
  if(Test-Path '.\ffmpeg.exe'){ $ff='.\ffmpeg.exe' }
  else{
    Write-Host 'Downloading ffmpeg from GitHub (~167 MB, one time)...'
    Invoke-WebRequest 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'
    Expand-Archive 'ffmpeg.zip' -DestinationPath 'ffmpeg_tmp' -Force
    $exe=Get-ChildItem 'ffmpeg_tmp' -Recurse -Filter 'ffmpeg.exe' | Select-Object -First 1
    Copy-Item $exe.FullName '.\ffmpeg.exe' -Force
    Remove-Item 'ffmpeg.zip','ffmpeg_tmp' -Recurse -Force
    $ff='.\ffmpeg.exe'
  }
}
Write-Host ('ffmpeg: '+$ff)

# frame start timecodes (seconds), 77 frames, in script order
$tc = @(0,6,12,19,26,33,40,42,50,57,61,68,74,83,88,91,98,100,106,114,120,128,137,143,151,161,167,175,181,185,190,195,203,211,217,226,235,243,248,255,260,264,272,279,287,296,304,312,320,330,334,339,348,356,363,370,377,384,391,395,400,408,416,423,427,434,442,450,456,462,468,477,482,490,496,504,508)
$tailSec = 4.0
# raw per-frame durations
$raw = @()
for($i=0;$i -lt ($tc.Count-1);$i++){ $raw += ($tc[$i+1]-$tc[$i]) }
$raw += $tailSec
$rawTotal = 0.0; foreach($r in $raw){ $rawTotal += $r }

# actual audio total (sum of the 8 Cillian chunks)
$audioTotal = 504.96
$scale = $audioTotal / $rawTotal
Write-Host ('Frames: '+$raw.Count+'  rawTotal: '+$rawTotal+'  audio: '+$audioTotal+'  scale: '+([math]::Round($scale,4)))

# build audio concat list (8 mp3 in order)
$alist = Join-Path $dir 'audio.txt'
$sb = New-Object System.Text.StringBuilder
for($n=1;$n -le 8;$n++){
  $name = ('{0:D2}.mp3' -f $n)
  $p = Join-Path $audioDir $name
  if(-not (Test-Path $p)){ Write-Host ('Missing audio '+$name+' — run the audio download bat.'); return }
  [void]$sb.AppendLine("file '"+($p -replace '\\','/')+"'")
}
[IO.File]::WriteAllText($alist, $sb.ToString(), (New-Object System.Text.ASCIIEncoding))
& $ff -y -f concat -safe 0 -i $alist -c copy 'full-narration.mp3'

# build frames concat list with scaled durations
$flist = Join-Path $dir 'frames.txt'
$fb = New-Object System.Text.StringBuilder
for($i=0;$i -lt 77;$i++){
  $name = ('frame-{0:D2}.png' -f ($i+1))
  $p = Join-Path $framesDir $name
  if(-not (Test-Path $p)){ Write-Host ('Missing '+$name+' — run СКАЧАТЬ-ВСЁ-смерть.bat'); return }
  $d = [math]::Round($raw[$i]*$scale,3)
  [void]$fb.AppendLine("file '"+($p -replace '\\','/')+"'")
  [void]$fb.AppendLine("duration $d")
}
# concat demuxer needs the last file repeated with no duration
$lastp = Join-Path $framesDir 'frame-77.png'
[void]$fb.AppendLine("file '"+($lastp -replace '\\','/')+"'")
[IO.File]::WriteAllText($flist, $fb.ToString(), (New-Object System.Text.ASCIIEncoding))

Write-Host 'Encoding dying-brain.mp4 (1920x1080, 25fps)...'
& $ff -y -f concat -safe 0 -i $flist -i 'full-narration.mp3' -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0xEFE7D6,setsar=1,format=yuv420p" -r 25 -c:v libx264 -preset medium -crf 19 -c:a aac -b:a 192k -shortest 'dying-brain.mp4'

Remove-Item 'audio.txt','frames.txt' -Force -ErrorAction SilentlyContinue
Write-Host ''
Write-Host 'ALL DONE. dying-brain.mp4 is ready (~8:25). Add text overlays + the real 2022 EEG insert in CapCut per МОНТАЖ-реальные-вставки.md.'
