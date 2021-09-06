import argparse
import os
import signal
import sys
import time

from flatpanel import FlatPanelConfig
from flightpatch import FlightPatchComposer
from windowstheme import Theme, WindowsThemeInterface


class App:

    def __init__(self):
        self.ORIGINAL_THEME_PATH = '.tmp/original_theme.json'
        self.PANEL_BACKGROUND_PATH = '.tmp/panel_background.png'

        self.themeInterface = WindowsThemeInterface()
        self.flightPatchComposer = None

    def parseArgs(self):
        argparser = argparse.ArgumentParser(
            prog='msfs-flat-panel',
            description='Sets up your monitor for a flat panel flight sim.'
        )

        argparser.add_argument(
            '-l',
            '--load',
            help="Loads a flat panel simulator from a .json config file.",
            metavar='CONFIG')

        argparser.add_argument(
            '-r',
            '--restore',
            help="Restores last stored original Windows theme.",
            action="store_true"
        )

        return argparser.parse_args()

    def run(self):
        args = self.parseArgs()

        if args.restore:
            self.restoreOriginalTheme()

        elif args.load:
            self.runConfig(args.load)

    def restoreOriginalTheme(self):
        theme = Theme.fromFile(self.ORIGINAL_THEME_PATH)
        WindowsThemeInterface().loadTheme(theme)
        print('Restored original theme')

    def saveCurrentTheme(self, path: str):
        self.themeInterface.currentTheme().toFile(path)
        print('Saved current theme')

    def addFlightPatchToWallpaper(self):
        path = self.PANEL_BACKGROUND_PATH
        self.flightPatchComposer = FlightPatchComposer(self.config.backgroundImage)
        image = self.flightPatchComposer.composePatch(
            patch=self.config.flightPatch,
            registration=self.config.addRegistration,
            selCalCode=self.config.addSelCalCode,
            callsign=self.config.addCallsign,
            descriptions=self.config.addDescriptions
        )
        image.save(path, 'PNG')
        print('Generated panel background')

        return path

    def activate(self):
        print(f'Loading: {self.config.manufacturer} '
              f'{self.config.aircraftType} '
              f'({self.config.typeDesignatorIcao})')

        # Save current theme
        self.saveCurrentTheme(self.ORIGINAL_THEME_PATH)

        # Generate complete panel background
        wallpaper = self.config.backgroundImage
        if self.config.addFlightPatch:
            wallpaper = self.addFlightPatchToWallpaper()

        # Activate theme
        self.config.theme.wallpaper = os.path.abspath(wallpaper)
        self.themeInterface.loadTheme(self.config.theme)
        print('Activated theme')

    def runConfig(self, configFile):
        self.config = FlatPanelConfig.fromFile(configFile)
        self.activate()

        def onSigInt(sig, frame):
            print('Shutdown signal received')
            self.restoreOriginalTheme()
            sys.exit(0)

        signal.signal(signal.SIGINT, onSigInt)
        while True:
            time.sleep(1)


if __name__ == '__main__':
    App().run()