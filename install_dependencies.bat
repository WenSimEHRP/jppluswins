@echo off

REM install python dependencies
pip install -r requirements.txt
if errorlevel 1 exit /b
echo Finished installing dependencies

echo Now cloning nml...
git clone https://github.com/openttd/nml
if errorlevel 1 exit /b
echo Finished cloning nml

echo Now merging...
cd nml
if errorlevel 1 exit /b
git config user.name "anonymous"
if errorlevel 1 exit /b
git config user.email "anonymous@example.com"
if errorlevel 1 exit /b
git remote add pr_source https://github.com/glx22/nml
if errorlevel 1 exit /b
git fetch pr_source layout_registers
if errorlevel 1 exit /b
git fetch pr_source var6B
if errorlevel 1 exit /b
git merge -X ours pr_source/layout_registers -m "Merge layout_registers"
if errorlevel 1 exit /b
git merge -X ours pr_source/var6B -m "Merge var6B"
if errorlevel 1 exit /b
echo Finished merging
