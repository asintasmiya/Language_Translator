# Language Translation Tool

A modern, user-friendly desktop application for translating text between many languages, built with Python and Tkinter. Supports copy, paste, clear, and text-to-speech features, with a beautiful light blue theme.

---

## What I've done so far:
- ◆ Designed and implemented a user-friendly **Language Translator** using Python and Tkinter for a graphical interface
- ◆ Integrated the [deep-translator](https://pypi.org/project/deep-translator/) library to support translation between many languages
- ◆ Enabled users to select source and target languages from dropdown menus
- ◆ Added features like **copy**, **paste**, **clear**, and **text-to-speech** for better usability
- ◆ Provided a modern, visually appealing color scheme for a pleasant user experience
- ◆ Implemented robust error handling for missing dependencies and translation issues

---

## This task helped me:
- Strengthen my Python programming skills
- Learn about GUI application development with Tkinter
- Explore integration with third-party APIs and libraries
- Improve user experience design and usability in Python apps

---

## Features
- Translate text from Different languages to dozens of languages (and vice versa)
- Auto language detection
- Copy, paste, and clear text with one click
- Text-to-speech for translated text
- Modern, clean GUI with color theme
- Fallback language list if translation engine is unavailable

## Requirements
- Python 3.7+
- Packages: `tkinter` (comes with Python), `deep-translator`, `pyttsx3`, `pyperclip`

## Installation
1. **Clone or download this repository.**
2. **(Recommended) Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```powershell
   python translator.py
   ```
2. Enter text, select source and target languages, and click "Translate".
3. Use the Copy, Paste, Clear, and Speak buttons as needed.

## Notes
- If you see a warning about the translation engine, check your internet connection or ensure `deep-translator` is installed.
- The app uses Google Translate via `deep-translator` for reliable translations.
- All features except translation (copy, paste, clear, speak) work even if translation is unavailable.

## Screenshots
![screenshot](screenshot.png)

## License
This project is for educational and personal use.

## Author

**ASIN TASMIYA K B**

---

**Made using Python and Tkinter.**
