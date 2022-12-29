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
pyinstaller --onefile --paths venv\Lib\site-packages --name "Xenia Patch Manager" --icon=assets/icon.ico --clean --noconsole main.py
[void](mkdir dist/assets)
[void](Copy-Item assets/icon.png dist/assets/)
[void](New-Item dist/path)
[void](Write-Output $env:userprofile | Set-Content dist/path)

Write-Host "Creating .zip..."
[void](Move-Item dist xenia-patch-manager)
. "C:\Program Files\7-Zip\7z.exe" a XeniaPatchManager.zip xenia-patch-manager/*
[void](Move-Item xenia-patch-manager dist)

Write-Host "Cleaning stuff up..."
[void](mkdir output)
[void](Move-Item dist/ output/)
[void](Move-Item build/ output/)
[void](Move-Item "Xenia Patch Manager.spec" output/)
[void](Move-Item XeniaPatchManager.zip output/)

Write-Host "Done :)"
