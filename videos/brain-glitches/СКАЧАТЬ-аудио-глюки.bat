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
$out = Join-Path $dir 'audio-glitches'
New-Item -ItemType Directory -Force -Path $out | Out-Null
Write-Host ('Saving into: '+$out)
$urls = @(
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_084621_85ccdfaf-cc18-4514-9e42-07975dfd7785.mp3',
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_084629_bfc099f9-026a-43aa-8232-06386536e75e.mp3',
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_084636_5df4b59d-ef13-4c64-8858-853ffcdfc7a9.mp3',
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_084644_07eea18f-668b-48d2-9243-c24375df357f.mp3',
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_084652_f07245ce-8cb1-45c7-bec0-9743d4bf4162.mp3',
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_084704_def12a7d-df9a-4b12-a8a8-77719eabe6f6.mp3',
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_084712_2a1141e9-e1c6-4ff7-9d09-3937c59e73f5.mp3',
 'https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/hf_20260629_084722_8bc4c5f8-5b70-4735-a8ae-3a7d1fc28dbb.mp3'
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
Write-Host 'ALL DONE. 8 mp3 files (01..08) are in the audio-glitches folder, in script order.'
