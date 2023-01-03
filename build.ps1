param (
	[switch] $Open
)

$OUTPUT_DIR = 'output/'

if (Test-Path -Path $OUTPUT_DIR){
	Write-Host "Removing past builds..."
	[void](Remove-Item -Path $OUTPUT_DIR -Recurse -Force)
}

Write-Host "Searching virtual environment..."
if (-not (Test-Path -Path './venv')){
	Write-Host "Environment not found, generating..."
	py -m venv venv
}

Write-Host "Installing dependencies..."
. venv/scripts/activate
[void](pip install -r requirements.txt)
deactivate

# Assumes PyInstaller is installed
Write-Host "Building executable..."
try {
	pyinstaller --onefile --paths venv\Lib\site-packages --name "Xenia Patch Manager" --icon=assets/icon.ico --clean --noconsole main.py
} catch {
	Write-Host "Failed to build executable!" -Foregroundcolor Red
	Break Script
}
[void](mkdir dist/assets)
[void](Copy-Item assets/icon.png dist/assets/)
[void](Copy-Item assets/styles.css dist/assets/)
[void](New-Item dist/path.txt)

# Adds Users/Public as default path
[void](Write-Output $env:public | Set-Content dist/path.txt)

# Minimize CSS with dart-sass
Write-Host "Minimizing stylesheet..."
try {
	sass ./assets/styles.css ./dist/assets/styles.css --style compressed --no-source-map
} catch {
	Write-Host "Failed to minimize stylesheet, copying source as fallback..." -ForegroundColor DarkYellow
	[void](Copy-Item assets/styles.css dist/assets/)
}

Write-Host "Creating .zip..."
[void](Move-Item dist xenia-patch-manager)
. "C:\Program Files\7-Zip\7z.exe" a XeniaPatchManager.zip xenia-patch-manager/*
[void](Move-Item xenia-patch-manager dist)

Write-Host "Cleaning stuff up..."
[void](mkdir output)
[void](Move-Item dist/ $OUTPUT_DIR)
[void](Move-Item build/ $OUTPUT_DIR)
[void](Move-Item "Xenia Patch Manager.spec" $OUTPUT_DIR)
[void](Move-Item XeniaPatchManager.zip $OUTPUT_DIR)

if ($Open){
	Set-Location $OUTPUT_DIR
	explorer .
	Set-Location ..
}

Write-Host "Done :)" -Foregroundcolor DarkCyan
