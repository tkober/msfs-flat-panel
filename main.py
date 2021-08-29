import json

from windowstheme import WindowsTheme, Theme, ThemeColor
from dataclasses import asdict

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

    WindowsTheme().loadTheme(original)

    theme = WindowsTheme().currentTheme()
    print(json.dumps(asdict(theme), indent=4))