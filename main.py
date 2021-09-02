import time

from windowstheme import WindowsThemeInterface, Theme
import signal
import sys
import argparse

ORIGINAL_THEME_PATH = '.tmp\\original_theme.json'

def onSigInt(sig, frame):
    restoreOriginalTheme()
    sys.exit(0)

def saveCurrentTheme(path: str):
    WindowsThemeInterface().currentTheme().toFile(path)

def loadA320():
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


def parseArgs():
    argparser = argparse.ArgumentParser(
        prog='msfs-flat-panel',
        description='Sets up your monitor for a flat panel flight sim.'
    )

    argparser.add_argument(
        '-r',
        '--restore',
        help = "Restores last stored original Windows theme.",
        action = "store_true"
    )

    return argparser.parse_args()


def restoreOriginalTheme():
    theme = Theme.fromFile(ORIGINAL_THEME_PATH)
    WindowsThemeInterface().loadTheme(theme)
    print('Restored original theme')


if __name__ == '__main__':
    args = parseArgs()

    if args.restore:
        restoreOriginalTheme()

    else:
        loadA320()