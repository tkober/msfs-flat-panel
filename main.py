import winreg

from windowstheme import WindowsTheme, Theme, ThemeColor

if __name__ == '__main__':
    a320Theme = Theme(
        dwmAccentColor=4288052579,
        dwmAccentColorInactive=4288052579,
        dwmColorPrevalence=True,
        explorerAccentColorMenu=4288052579
    )

    original = Theme(
        dwmAccentColor=4279654135,
        dwmAccentColorInactive=4288052579,
        dwmColorPrevalence=False,
        explorerAccentColorMenu=4279654135
    )

    #WindowsTheme().loadTheme(original)
    color = ThemeColor.fromRegDword(original.dwmAccentColor)
    print(color)
    print(color.toRegDword())



    # A320
    #4288052579
    #4288052579
    #True

    # Normal
    #4279654135
    #4288052579
    #False
    #4279654135