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
# find first image (png/jpg/jpeg/webp), excluding our output and ffmpeg
$img = Get-ChildItem -File | Where-Object { $_.Extension -match '^\.(png|jpg|jpeg|webp)$' -and $_.Name -ne 'thumbnail-1280x720.png' -and $_.Name -ne 'ffmpeg.exe' } | Select-Object -First 1
if(-not $img){ Write-Host 'No image found. Put your thumbnail image (png/jpg) next to this .bat and run again.'; return }
Write-Host ('Input image: '+$img.Name)
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
# scale to fit 1280x720, pad to exact 16:9 with a soft cream background (matches reference)
& $ff -y -i $img.FullName -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0xF3E6CE" -update 1 'thumbnail-1280x720.png'
Write-Host 'ALL DONE. thumbnail-1280x720.png is ready to upload as your YouTube thumbnail.'
