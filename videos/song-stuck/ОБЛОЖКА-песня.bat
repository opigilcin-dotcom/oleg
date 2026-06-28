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
if(-not (Test-Path $dest)){ New-Item -ItemType Directory -Force $dest | Out-Null }
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
Write-Host 'Making thumbnail 1280x720 (G1)...'
& $ff -y -i 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260628_163225_3a3fec89-3b2f-4949-8110-ae360d6df3d3.png' -vf scale=1280:720 -update 1 'thumbnail-1280x720.png'
Write-Host 'ALL DONE. thumbnail-1280x720.png is in the folder.'
