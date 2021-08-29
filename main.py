import time

from windowstheme import WindowsThemeInterface, Theme
import signal
import sys

ORIGINAL_THEME_PATH = '.tmp\\original_theme.json'

def onSigInt(sig, frame):
    theme = Theme.fromFile(ORIGINAL_THEME_PATH)
    WindowsThemeInterface().loadTheme(theme)
    print('Restored original theme')
    sys.exit(0)

def saveCurrentTheme(path: str):
    WindowsThemeInterface().currentTheme().toFile(path)

def main():
    # Save current theme
    saveCurrentTheme(ORIGINAL_THEME_PATH)
    print('Saved current theme')

    # Load A320 Theme
    theme = Theme.fromFile('themes\\a320\\theme.json')
    WindowsThemeInterface().loadTheme(theme)
    print('Loaded theme "A320"')

    signal.signal(signal.SIGINT, onSigInt)
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()