@echo off
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "$c=[IO.File]::ReadAllText('%~f0');$i=$c.LastIndexOf('#PSBODY#');iex $c.Substring($i+8)"
echo.
pause
exit /b
#PSBODY#
$ErrorActionPreference='Stop'
$folder = -join ([char]1089,[char]1090,[char]1080,[char]1082,[char]1084,[char]1077,[char]1085,[char]40,[char]1089,[char]1086,[char]1085,[char]41)
$dest = Join-Path ([Environment]::GetFolderPath('Desktop')) $folder
if(-not (Test-Path $dest)){ Write-Host ('Folder not found: '+$dest); return }
Set-Location -LiteralPath $dest
Write-Host ('Folder: '+$dest)
$ff=$null
try{ ffmpeg -version *>$null; $ff='ffmpeg' }catch{}
if(-not $ff){
  if(Test-Path '.\ffmpeg.exe'){ $ff='.\ffmpeg.exe' }
  elseif(Test-Path '.\ffmpeg\bin\ffmpeg.exe'){ $ff='.\ffmpeg\bin\ffmpeg.exe' }
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
$parts=@('01.mp3','02.mp3','03.mp3','04.mp3','05.mp3','06.mp3','07.mp3','08.mp3','09.mp3')
($parts | ForEach-Object { "file '$_'" }) | Set-Content 'audio.txt' -Encoding ASCII
& $ff -y -f concat -safe 0 -i 'audio.txt' -c copy 'full.mp3'
$frames=@('0-00.png','0-03.png','0-06.png','0-09.png','0-12.png','0-15.png','0-18.png','0-21.png','0-24.png','0-27.png','0-30.png','0-33.png','0-37.png','0-40.png','0-43.png','0-46.png','0-49.png','0-52.png','0-55.png','0-58.png','1-01.png','1-04.png','1-07.png','1-10.png','1-13.png','1-16.png','1-19.png','1-22.png','1-25.png','1-28.png','1-31.png','1-36.png','1-39.png','1-42.png','1-45.png','1-48.png','1-51.png','1-54.png','1-57.png','2-00.png','2-03.png','2-06.png','2-09.png','2-12.png','2-15.png','2-18.png','2-21.png','2-24.png','2-28.png','2-32.png','2-35.png','2-38.png','2-41.png','2-44.png','2-47.png','2-50.png','2-53.png','2-56.png','2-59.png','3-02.png','3-05.png','3-08.png','3-11.png','3-14.png','3-17.png','3-20.png','3-23.png','3-26.png','3-29.png','3-32.png','3-36.png','3-39.png','3-42.png','3-45.png','3-48.png','3-51.png','3-54.png','3-57.png','4-00.png','4-03.png','4-06.png','4-09.png','4-12.png','4-15.png','4-18.png','4-22.png','4-26.png','4-29.png','4-32.png','4-35.png','4-38.png','4-41.png','4-44.png','4-47.png','4-50.png','4-53.png','4-56.png','4-59.png','5-02.png','5-05.png','5-08.png','5-11.png','5-14.png','5-17.png','5-20.png','5-23.png','5-26.png','5-29.png','5-32.png','5-35.png','5-38.png','5-41.png','5-44.png','5-47.png','5-50.png','5-53.png','5-56.png','5-59.png','6-02.png','6-05.png','6-08.png','6-11.png','6-14.png','6-17.png','6-20.png','6-23.png','6-26.png','6-28.png','6-31.png','6-34.png','6-37.png','6-40.png','6-43.png','6-46.png','6-50.png','6-54.png','6-57.png','7-00.png','7-03.png','7-06.png','7-09.png','7-12.png','7-15.png','7-18.png','7-21.png')
$raw=@(3,3,3,3,3,3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,5,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3,4,4,3,3,3,3,3,3,3,3,3,3)
$adur=445.44
$rawsum=444
$scale=$adur/$rawsum
$lines=New-Object System.Collections.Generic.List[string]
for($i=0;$i -lt $frames.Count;$i++){ $d=[math]::Round($raw[$i]*$scale,3); $lines.Add("file '$($frames[$i])'"); $lines.Add('duration '+$d) }
$lines.Add("file '$($frames[$frames.Count-1])'")
$lines | Set-Content 'images.txt' -Encoding ASCII
& $ff -y -f concat -safe 0 -i 'images.txt' -i 'full.mp3' -vf 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:white,fps=25,format=yuv420p' -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest 'sleep.mp4'
Write-Host 'ALL DONE. sleep.mp4 is in the folder.'