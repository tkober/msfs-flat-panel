from windowstheme import WindowsTheme, Theme, ThemeColor

if __name__ == '__main__':
    orange = ThemeColor(r=247, g=86, b=22)
    blue = ThemeColor(r=99, g=125, b=150)

    a320Theme = Theme(
        dwmAccentColor=blue,
        dwmAccentColorInactive=blue,
        dwmColorPrevalence=True,
        explorerAccentColorMenu=blue,
        wallpaper='C:\\Users\\thors\\Desktop\\msfs_2020_flat_panel_background_airbus_a320.png'
    )

    original = Theme(
        dwmAccentColor=orange,
        dwmAccentColorInactive=orange,
        dwmColorPrevalence=False,
        explorerAccentColorMenu=orange,
        wallpaper='c:\\windows\\web\\wallpaper\\windows\\img0.jpg'
    )

    WindowsTheme().loadTheme(original)
    print(WindowsTheme().currentTheme().toJson())