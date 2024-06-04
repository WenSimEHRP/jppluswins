@echo off

REM get current time
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /format:list') do set datetime=%%I
set datetime=%datetime:~0,4%/%datetime:~4,2%/%datetime:~6,2% %datetime:~8,2%:%datetime:~10,2%:%datetime:~12,2%

REM preprocess tags.txt with gcc
gcc -E -x c -DCURRENT_TIME="%datetime% PT" -o custom_tags.txt tags.txt
if errorlevel 1 exit /b
echo Finished preprocessing tags.txt

echo Now preprocessing...
gcc -E -x c -o wins.nml wins.pnml
if errorlevel 1 exit /b
echo Finished preprocessing

echo Now compiling...
py nml/nmlc wins.nml -o wins.grf --nml="wins_parsed.nml"
if errorlevel 1 exit /b
echo Finished compiling!
