import winreg

from windowstheme import WindowsTheme

if __name__ == '__main__':
    theme = WindowsTheme()

    theme.setDwmAccentColor(4288052579)
    theme.setDwmAccentColorInactive(4288052579)
    theme.setDwmColorPrevalence(1)
    theme.setExplorerAccentColor(4288052579)

    print(theme.getDwmAccentColor())
    print(theme.getDwmAccentColorInactive())
    print(theme.getDwmColorPrevalence())
    print(theme.getExplorerAccentColor())

    # A320
    #4288052579
    #4288052579
    #True

    # Normal
    #4279654135
    #4288052579
    #False
    #4279654135