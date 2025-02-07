# Tidy Textbooks Automation

## Description

This is a quick and dirty Python script that plays Royale High's Tidy Textbooks minigame reliably up until ~75 books.

## Usage

- This script only runs on Windows with Python 3. Tested on Python 3.12.
- Make sure you have Python 3 installed. On Windows, download it from [python.org](https://www.python.org/downloads/) or the Microsoft Store.
- Make a venv with `python3 -m venv venv`
- Activate the venv with `venv\Scripts\Activate.ps1` on Windows.
- Install dependencies with `pip install -r requirements.txt`
- Open Roblox, join Royale High, and start the Tidy Textbooks Minigame.
- Run the script with `python3 tidy_textbooks.py`
- Exit the script by pressing Ctrl + C or you may experience unwanted clicking...

## Modifying the script

This script was developed for a screen resolution of `2560x1600` on an Asus ROG Zephyrus G14 14 inch screen. You may need to tweak the `startXCoord` and `gameWidth` variables to fit your screen.

## Requirements

- Python 3
- pyautogui
- numpy
- pywin32
- opencv-python
