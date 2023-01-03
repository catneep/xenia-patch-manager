# Xenia Patch Manager

<p align="center">
  <img src="assets/icon.png" />
</p>

A GUI utility that deals with [Xenia Canary's](https://xenia.jp/) cumbersome patch solution

## Features
- Display all the available patches for a game in an intuitive interface
- Easily backup a configuration file

### Patch compatibility
This utility was built using the patches in [this repository](https://github.com/xenia-canary/game-patches) as a template, as such, it may not work properly (if at all) with other files.

## Requirements
In order to use this utility, you'll need:
- [Xenia Canary](https://github.com/xenia-canary/xenia-canary)
- A couple of [compatible patch files](https://github.com/xenia-canary/game-patches)

If you're building the executable as stated in the [Build manually](#build-manually) section, you'll also need:
- [7-Zip](https://www.7-zip.org/)
- [Dart Sass](https://sass-lang.com/dart-sass)
- [Python](https://www.python.org/) 3.8 or later
- [PyInstaller](https://pyinstaller.org/en/stable/) for Windows

## Installation
You can easily get an executable for Windows from this repo's [***Releases***](https://github.com/catneep/xenia-patch-manager/releases) page, or if you want to get your hands dirty, you may follow one of the following sections:

### For development
You can run this utility by using the following commands:

    git clone https://github.com/catneep/xenia-patch-manager
    cd xenia-patch-manager
    py -m venv venv
    . venv/scripts/activate
    pip install -r requirements

### Build manually
Alternatively, you can build an .exe file by running the included ***"build.ps1"*** script from PowerShell (5.1 or later):

    git clone https://github.com/catneep/xenia-patch-manager
    cd xenia-patch-manager
    ./build.ps1

This will generate a new directory named ***"output"***, where you'll find the executable.

## How to use
### For development
After cloning the repository and activating the virtual environment, you can simply run the utility with:

    py main.py path/to/patch_directory

Likewise, you can edit the route to your local patch directory in the file ***"path.txt"*** and run the following command:

    py main.py

### General use
You'll see the following window on startup:

![Main window](assets/main-view.png)

You may select a new root directory by using the ***"Browse"*** button.

You can then select a file from your locally stored patches in order to display all available options:

![Game selection](assets/game-select.png)
![Game options](assets/game-view.png)

You can then save all the changes you've made or backup the current configuration in a *".bak"* file within the same directory.

That's about it, you no longer have to deal with .toml files on your own, enjoy!

## The future
A list of features that I have in mind can be found inside the repo's ***".todo"*** file, so keep an eye out for any new features or bug fixes!
