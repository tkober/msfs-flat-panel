from windowstheme import WindowsTheme, Theme, ThemeColor

if __name__ == '__main__':
    orange = ThemeColor(r=247, g=86, b=22)
    blue = ThemeColor(r=99, g=125, b=150)

    a320Theme = Theme(
        dwmAccentColor=blue,
        dwmAccentColorInactive=blue,
        dwmColorPrevalence=True,
        explorerAccentColorMenu=blue
    )

    original = Theme(
        dwmAccentColor=orange,
        dwmAccentColorInactive=orange,
        dwmColorPrevalence=False,
        explorerAccentColorMenu=orange
    )

    print(WindowsTheme().currentTheme().toJson())