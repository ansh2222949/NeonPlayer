@echo off
title NeonPlayer Clean Builder
echo [1/4] Cleaning old build files...


if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist NeonPlayer.spec del /q NeonPlayer.spec

echo [2/4] Old files deleted successfully.
echo [3/4] Starting fresh build...


pyinstaller ^
 --noconsole ^
 --onefile ^
 --icon=app_icon.ico ^
 --add-data "web;web" ^
 --add-data "core;core" ^
 --name "NeonPlayer" ^
 main.py

echo [4/4] Build Complete! Check the 'dist' folder.
pause
