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
$out = Join-Path $dir 'audio-death'
New-Item -ItemType Directory -Force -Path $out | Out-Null
Write-Host ('Saving into: '+$out)
$urls = @(
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_093730_500d9dcb-5513-40ee-90fa-9c2e232d18fc.mp3',
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_093740_89c64653-d67e-4334-b33c-c62e004c5148.mp3',
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_093749_bf47db33-41f6-42a4-898d-92d02021dd8a.mp3',
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_093759_8b072c63-a04e-4dda-ae29-69745bb25756.mp3',
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_093813_c9d9da87-8699-4161-84a6-a59419a376dd.mp3',
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_093822_3cf035ee-ba43-4ab8-b6a1-e9904304940b.mp3',
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_093828_c65a60cb-04b0-450d-9456-caf56b1767c7.mp3',
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_093834_3239a9c3-ac62-4904-8dca-d1d0ec0a66a1.mp3'
)
$n=0
foreach($u in $urls){
  $n++
  $name = ('{0:D2}.mp3' -f $n)
  $dest = Join-Path $out $name
  Write-Host ('Downloading '+$name)
  & curl.exe -L -o $dest $u
}
Write-Host ''
Write-Host 'ALL DONE. 8 mp3 files (01..08) are in the audio-death folder, in script order.'
