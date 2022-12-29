Write-Host "Searching virtual environment..."
if (-not (Test-Path -Path './venv')){
	Write-Host "Environment not found, generating..."
	py -m venv venv
}

Write-Host "Installing dependencies..."
. venv/scripts/activate
[void](pip install -r requirements.txt)
deactivate

Write-Host "Building executable..."
pyinstaller --onefile --paths venv\Lib\site-packages --name "Xenia Patch Manager" --icon=assets/icon.ico --clean --noconsole main.py | Out-Null
[void](mkdir dist/assets)
[void](Copy-Item assets/icon.png dist/assets/)
[void](New-Item dist/path)

Write-Host "Creating .zip..."
. "C:\Program Files\7-Zip\7z.exe" a XeniaPatchManager.zip dist/*

Write-Host "Done :)"
