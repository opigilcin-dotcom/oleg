@echo off
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "$c=[IO.File]::ReadAllText('%~f0');$i=$c.LastIndexOf('#PSBODY#');iex $c.Substring($i+8)"
echo.
pause
exit /b
#PSBODY#
$ErrorActionPreference='Stop'
$folder = -join ([char]1089,[char]1090,[char]1080,[char]1082,[char]1084,[char]1101,[char]1085)
$desk = [Environment]::GetFolderPath('Desktop')
$dest = Join-Path $desk $folder
if(-not (Test-Path $dest)){ $dest = $desk }
Set-Location -LiteralPath $dest
Write-Host ('Output folder: '+$dest)
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
Write-Host 'Making avatar 800x800...'
& $ff -y -i 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260627_081759_d1b014aa-5b60-450c-8d64-65fc59ef755c.png' -vf scale=800:800 -update 1 'avatar-800.png'
Write-Host 'Making banner 2560x1440...'
& $ff -y -i 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260628_102359_a253b5c9-ac2b-4b38-ac7b-4c8b184c17b1.png' -vf scale=2560:1440 -update 1 'banner-2560x1440.png'
Write-Host 'Making thumbnail 1280x720...'
& $ff -y -i 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260628_054559_b309f963-340b-47c5-ab41-7159386d8dc8.png' -vf scale=1280:720 -update 1 'thumbnail-1280x720.png'
Write-Host 'ALL DONE. avatar-800.png, banner-2560x1440.png, thumbnail-1280x720.png are in the folder.'
