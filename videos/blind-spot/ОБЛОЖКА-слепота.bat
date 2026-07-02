@echo off
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "$c=[IO.File]::ReadAllText('%~f0');$i=$c.LastIndexOf('#PSBODY#');iex $c.Substring($i+8)"
echo.
pause
exit /b
#PSBODY#
try {
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls11 -bor [Net.SecurityProtocolType]::Tls
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
if(-not $dir){ $dir = (Get-Location).Path }
Set-Location -LiteralPath $dir
Write-Host ('Folder: '+$dir)
$src = 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260702_125033_fd4244d1-7da1-4be0-947c-c463aeeea85d.png'
Write-Host 'Downloading thumbnail (I - NO SIGNAL, black background, TV-static across the eyes)...'
Remove-Item '.\cover-src.png' -Force -ErrorAction SilentlyContinue
try {
  Invoke-WebRequest -Uri $src -OutFile 'cover-src.png' -UseBasicParsing
} catch {
  Write-Host ('Invoke-WebRequest failed: '+$_.Exception.Message)
  Write-Host 'Trying curl.exe as a fallback...'
  & curl.exe -L -o 'cover-src.png' $src
}
if(-not (Test-Path '.\cover-src.png') -or (Get-Item '.\cover-src.png').Length -lt 1000){
  Write-Host 'DOWNLOAD FAILED. The image did not save correctly.'
  Write-Host 'Possible causes: no internet, a firewall/antivirus blocking the connection, or a corporate network blocking cloudfront.net.'
  Write-Host 'Try opening this link directly in your browser to test it:'
  Write-Host $src
  return
}
Write-Host 'Thumbnail source downloaded OK.'
$ff=$null
try{ ffmpeg -version *>$null; $ff='ffmpeg' }catch{}
if(-not $ff){
  if(Test-Path '.\ffmpeg.exe'){ $ff='.\ffmpeg.exe' }
  else{
    try{
      Write-Host 'Downloading ffmpeg from GitHub (~167 MB, one time, needed only to resize to exactly 1280x720)...'
      Invoke-WebRequest 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip' -UseBasicParsing
      Expand-Archive 'ffmpeg.zip' -DestinationPath 'ffmpeg_tmp' -Force
      $exe=Get-ChildItem 'ffmpeg_tmp' -Recurse -Filter 'ffmpeg.exe' | Select-Object -First 1
      Copy-Item $exe.FullName '.\ffmpeg.exe' -Force
      Remove-Item 'ffmpeg.zip','ffmpeg_tmp' -Recurse -Force -ErrorAction SilentlyContinue
      $ff='.\ffmpeg.exe'
    } catch {
      Write-Host ('ffmpeg download failed: '+$_.Exception.Message)
    }
  }
}
if(-not $ff){
  Write-Host 'ffmpeg is not available, so the image cannot be auto-resized to 1280x720.'
  Copy-Item '.\cover-src.png' '.\thumbnail-1280x720.png' -Force
  Write-Host 'Saved the original image as thumbnail-1280x720.png instead (resize it manually before uploading, e.g. at https://www.iloveimg.com/resize-image).'
  return
}
Write-Host ('ffmpeg: '+$ff)
& $ff -y -i 'cover-src.png' -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x111111" -update 1 'thumbnail-1280x720.png'
Remove-Item 'cover-src.png' -Force -ErrorAction SilentlyContinue
Write-Host 'ALL DONE. thumbnail-1280x720.png is ready to upload as your YouTube thumbnail.'
} catch {
  Write-Host '=== SCRIPT ERROR ==='
  Write-Host $_.Exception.Message
  Write-Host $_.InvocationInfo.PositionMessage
}
