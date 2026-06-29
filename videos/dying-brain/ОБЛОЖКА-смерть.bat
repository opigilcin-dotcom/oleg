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
$src = 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_101028_ab41d349-25bb-463b-a47d-f42372fb417c.png'
Write-Host 'Downloading thumbnail (A - THE LAST 7 MINUTES)...'
& curl.exe -L -o 'cover-src.png' $src
if(-not (Test-Path '.\cover-src.png')){ Write-Host 'Download failed. Check internet and run again.'; return }
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
& $ff -y -i 'cover-src.png' -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0xEFE7D6" -update 1 'thumbnail-1280x720.png'
Remove-Item 'cover-src.png' -Force -ErrorAction SilentlyContinue
Write-Host 'ALL DONE. thumbnail-1280x720.png is ready to upload as your YouTube thumbnail.'
