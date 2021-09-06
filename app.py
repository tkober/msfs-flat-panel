import argparse
import os
import signal
import sys
import time

from flatpanel import FlatPanelConfig
from flightpatch import FlightPatchComposer, Callsign, SelCalCode
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

        if self.config.addCallsign and self.config.askForCallsign:
            self.askForCallsign()

        if self.config.addSelCalCode and self.config.askForSelCalCode:
            self.askForSelCalCode()

        if self.config.addRegistration and self.config.askForRegistration:
            self.askForRegistration()

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

    def askForUserInput(self, hint: str, fallbackOnEmpty=False, fallbackValue: str = None) -> str:

        if fallbackOnEmpty:
            promt = f'{hint} [{fallbackValue}]>'
        else:
            promt = f'{hint}>'

        answer = input(promt)

        if fallbackOnEmpty and len(answer) == 0:
            return fallbackValue
        else:
            return answer

    def askForCallsign(self):
        success = False

        while not success:
            callsignString = self.askForUserInput(
                "Callsign?",
                self.config.defaultCallsignOnEmpty,
                self.config.flightPatch.callsign.getFullValue()
            )
            try:
                self.config.flightPatch.callsign = Callsign(callsignString)
                success = True
                print(f'{self.config.flightPatch.callsign.getFullValue(" ")}\n')
            except ValueError as e:
                print(f'{e}\n', file=sys.stderr)

    def askForSelCalCode(self):
        success = False

        while not success:
            selCalCodeString = self.askForUserInput(
                "SelCal Code?",
                self.config.defaultSelCalCodeOnEmpty,
                self.config.flightPatch.selCalCode.getFullCode(' ')
            )
            try:
                self.config.flightPatch.selCalCode = SelCalCode(selCalCodeString)
                success = True
                print(f'{self.config.flightPatch.selCalCode.getFullCode(" ")}\n')
            except ValueError as e:
                print(f'{e}\n', file=sys.stderr)

    def askForRegistration(self):
        registration = self.askForUserInput(
            "Aircraft registration?",
            self.config.defaultRegistrationOnEmpty,
            self.config.flightPatch.aircraftRegistration
        )
        self.config.flightPatch.aircraftRegistration = registration
        print(f'{registration}\n')

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