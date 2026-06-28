@echo off
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "$c=[IO.File]::ReadAllText('%~f0');$i=$c.LastIndexOf('#PSBODY#');iex $c.Substring($i+8)"
echo.
pause
exit /b
#PSBODY#
$ErrorActionPreference='Stop'
$folder = -join ([char]1076,[char]1086,[char]1089,[char]1082,[char]1072,[char]40,[char]1087,[char]1077,[char]1089,[char]1085,[char]1103,[char]41)
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
$parts=@('01.mp3','02.mp3','03.mp3','04.mp3','05.mp3','06.mp3','07.mp3','08.mp3','09.mp3','10.mp3')
($parts | ForEach-Object { "file '$_'" }) | Set-Content 'audio.txt' -Encoding ASCII
& $ff -y -f concat -safe 0 -i 'audio.txt' -c copy 'full.mp3'
$frames=@('0-00.png','0-03.png','0-07.png','0-11.png','0-15.png','0-20.png','0-24.png','0-29.png','0-33.png','0-37.png','0-42.png','0-46.png','0-49.png','0-54.png','0-59.png','1-04.png','1-09.png','1-12.png','1-15.png','1-21.png','1-25.png','1-28.png','1-33.png','1-37.png','1-41.png','1-46.png','1-50.png','1-54.png','1-59.png','2-03.png','2-06.png','2-11.png','2-14.png','2-18.png','2-21.png','2-24.png','2-29.png','2-35.png','2-38.png','2-43.png','2-48.png','2-52.png','2-57.png','3-01.png','3-05.png','3-10.png','3-14.png','3-18.png','3-22.png','3-27.png','3-32.png','3-35.png','3-40.png','3-45.png','3-49.png','3-54.png','3-59.png','4-04.png','4-07.png','4-12.png','4-18.png','4-22.png','4-27.png','4-31.png','4-35.png','4-38.png','4-42.png','4-48.png','4-54.png','4-57.png','5-01.png','5-06.png','5-10.png','5-16.png','5-22.png','5-28.png','5-33.png','5-37.png','5-41.png','5-45.png','5-50.png','5-56.png','6-02.png','6-05.png','6-10.png','6-15.png','6-20.png','6-26.png','6-29.png','6-34.png','6-37.png','6-40.png','6-44.png','6-48.png','6-52.png','6-58.png','7-03.png','7-06.png','7-10.png','7-15.png','7-20.png','7-24.png','7-28.png','7-34.png','7-40.png','7-43.png','7-48.png','7-53.png','7-55.png','8-00.png','8-06.png','8-09.png','8-15.png','8-20.png')
$raw=@(3,4,4,4,5,4,5,4,4,5,4,3,5,5,5,5,3,3,6,4,3,5,4,4,5,4,4,5,4,3,5,3,4,3,3,5,6,3,5,5,4,5,4,4,5,4,4,4,5,5,3,5,5,4,5,5,5,3,5,6,4,5,4,4,3,4,6,6,3,4,5,4,6,6,6,5,4,4,4,5,6,6,3,5,5,5,6,3,5,3,3,4,4,4,6,5,3,4,5,5,4,4,6,6,3,5,5,2,5,6,3,6,5,4)
$adur=510.4
$rawsum=504
$scale=$adur/$rawsum
$lines=New-Object System.Collections.Generic.List[string]
for($i=0;$i -lt $frames.Count;$i++){ $d=[math]::Round($raw[$i]*$scale,3); $lines.Add("file '$($frames[$i])'"); $lines.Add('duration '+$d) }
$lines.Add("file '$($frames[$frames.Count-1])'")
$lines | Set-Content 'images.txt' -Encoding ASCII
& $ff -y -f concat -safe 0 -i 'images.txt' -i 'full.mp3' -vf 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:white,fps=25,format=yuv420p' -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest 'song.mp4'
Write-Host 'ALL DONE. song.mp4 is in the folder.'