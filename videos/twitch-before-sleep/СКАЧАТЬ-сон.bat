@echo off
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "$c=[IO.File]::ReadAllText('%~f0');$i=$c.LastIndexOf('#PSBODY#');iex $c.Substring($i+8)"
echo.
pause
exit /b
#PSBODY#
$ErrorActionPreference='Stop'
$folder = -join ([char]1089,[char]1090,[char]1080,[char]1082,[char]1084,[char]1077,[char]1085,[char]40,[char]1089,[char]1086,[char]1085,[char]41)
$desk = [Environment]::GetFolderPath('Desktop')
$dest = Join-Path $desk $folder
if(-not (Test-Path $dest)){ New-Item -ItemType Directory -Force $dest | Out-Null }
Write-Host ('Folder: '+$dest)
$base='https://d8j0ntlcm91z4.cloudfront.net/user_3FcaNpN5kYVpXp4PHFWx6FQ3hg7/'
$files=@(@('01.mp3','hf_20260628_060347_ba64cd3e-6eb5-4ba5-9f60-69c7a2eaf1c3.mp3');@('02.mp3','hf_20260628_060351_c0460187-e804-4bf7-a346-d48f7ffc994d.mp3');@('03.mp3','hf_20260628_060421_b9ac8c23-6df8-4429-bdef-aff154a417eb.mp3');@('04.mp3','hf_20260628_061034_a23bd93e-afa8-4e55-82ac-e7be37a62c09.mp3');@('05.mp3','hf_20260628_060425_a48c5da3-66ae-4279-abc9-0728f4844af4.mp3');@('06.mp3','hf_20260628_061037_47598028-afb3-41e4-8411-ba30b98da2ff.mp3');@('07.mp3','hf_20260628_060451_91f8506a-9601-4c8d-9c2e-d9e58e6e76ba.mp3');@('08.mp3','hf_20260628_061056_75d18113-0b89-4d1e-af6c-d10f838158f4.mp3');@('09.mp3','hf_20260628_060454_63c0eb7e-34e5-4983-8f22-6698ce4936f9.mp3'))
$i=0
foreach($f in $files){ $i++; Write-Host ('['+$i+'/'+$files.Count+'] '+$f[0]); Invoke-WebRequest ($base+$f[1]) -OutFile (Join-Path $dest $f[0]) }
Write-Host 'ALL DONE. 9 mp3 files (01-09) downloaded to the folder on your Desktop.'