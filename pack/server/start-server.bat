@echo off
setlocal
set "MINECRAFT_VERSION=1.20.1"
set "FORGE_VERSION=47.4.23"
set "FORGE_COORD=%MINECRAFT_VERSION%-%FORGE_VERSION%"
set "INSTALLER=forge-%FORGE_COORD%-installer.jar"
set "ARGS=libraries\net\minecraftforge\forge\%FORGE_COORD%\win_args.txt"

if not exist "%ARGS%" (
  echo Installing Forge %FORGE_COORD%...
  java -jar "%INSTALLER%" --installServer
  if errorlevel 1 exit /b %errorlevel%
)

java @user_jvm_args.txt @"%ARGS%" nogui
