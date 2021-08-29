import ctypes
import json
import winreg
from dataclasses import dataclass, asdict


@dataclass()
class ThemeColor:
    r: int
    g: int
    b: int

    def toRegDword(self) -> int:
        return (0xff<<24) + (self.b<<16) + (self.g<<8) + self.r

    def fromRegDword(value: int):
        bytes = value.to_bytes(4, byteorder='little')
        r = bytes[0]
        g = bytes[1]
        b = bytes[2]

        return ThemeColor(r=r, g=g, b=b)

    def fromJsonObject(jsonObject: dict):
        return ThemeColor(
            r=jsonObject['r'],
            g=jsonObject['g'],
            b=jsonObject['b']
        )


@dataclass
class Theme:
    dwmAccentColor: ThemeColor
    dwmAccentColorInactive: ThemeColor
    dwmColorPrevalence: bool
    explorerAccentColorMenu: ThemeColor
    wallpaper: str

    def toJson(self, indent=4) -> str:
        return json.dumps(asdict(self), indent=indent)

    def fromFile(path: str):
        file = open(path)
        jsonObject = json.load(file)
        file.close()

        dwmAccentColor = ThemeColor.fromJsonObject(jsonObject['dwmAccentColor'])
        dwmAccentColorInactive = ThemeColor.fromJsonObject(jsonObject['dwmAccentColorInactive'])
        explorerAccentColorMenu = ThemeColor.fromJsonObject(jsonObject['explorerAccentColorMenu'])
        dwmColorPrevalence = jsonObject['dwmColorPrevalence']
        wallpaper = jsonObject['wallpaper']

        return Theme(
            dwmAccentColor=dwmAccentColor,
            dwmAccentColorInactive=dwmAccentColorInactive,
            explorerAccentColorMenu=explorerAccentColorMenu,
            dwmColorPrevalence=dwmColorPrevalence,
            wallpaper=wallpaper
        )

    def toFile(self, path: str, indent=4):
        file = open(path, 'w')
        file.write(self.toJson(indent=indent))
        file.close()


class WindowsThemeInterface:

    def __init__(self, rootHkey=winreg.HKEY_CURRENT_USER):
        self.__registryHkey = rootHkey
        self.__DwmRegistrySubkey = 'SOFTWARE\Microsoft\Windows\DWM'
        self.__WindowsExplorerAccentRegistrySubkey = 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Accent'

        self.__dwmAccentColorValue = 'AccentColor'
        self.__dwmAccentColorInactiveValue = 'AccentColorInactive'
        self.__dwmColorPrevalenceValue = 'ColorPrevalence'

        self.__explorerAccentColorMenuValue = 'AccentColorMenu'

    def __getRegistryIntValue(self, hSubKey: str, valueName: str) -> (int, int):
        keyh = winreg.OpenKey(self.__registryHkey, hSubKey)
        value, type = winreg.QueryValueEx(keyh, valueName)
        keyh.Close()
        return (value, type)

    def __setRegistryIntValue(self, hSubKey: str, valueName: str, value: int):
        keyh = winreg.OpenKey(self.__registryHkey, hSubKey, access=winreg.KEY_SET_VALUE)
        winreg.SetValueEx(keyh, valueName, 0, winreg.REG_DWORD, value)
        keyh.Close()

    def loadTheme(self, theme: Theme):
        self.setDwmAccentColor(theme.dwmAccentColor)
        self.setDwmAccentColorInactive(theme.dwmAccentColorInactive)
        self.setDwmColorPrevalence(theme.dwmColorPrevalence)
        self.setExplorerAccentColor(theme.explorerAccentColorMenu)
        self.setWallpaper(theme.wallpaper)

    def currentTheme(self) -> Theme:
        return Theme(
            dwmAccentColor=self.getDwmAccentColor(),
            dwmAccentColorInactive=self.getDwmAccentColorInactive(),
            dwmColorPrevalence=self.getDwmColorPrevalence(),
            explorerAccentColorMenu=self.getExplorerAccentColor(),
            wallpaper=self.getWallpaper()[1]
        )

    # Accent Color
    def getDwmAccentColor(self) -> ThemeColor:
        result, _ = self.__getRegistryIntValue(self.__DwmRegistrySubkey, self.__dwmAccentColorValue)
        return ThemeColor.fromRegDword(result)

    def setDwmAccentColor(self, value: ThemeColor):
        regDwordValue = value.toRegDword()
        self.__setRegistryIntValue(self.__DwmRegistrySubkey, self.__dwmAccentColorValue, regDwordValue)

    # Accent Color Inactive
    def getDwmAccentColorInactive(self) -> ThemeColor:
        result, _ = self.__getRegistryIntValue(self.__DwmRegistrySubkey, self.__dwmAccentColorInactiveValue)
        return ThemeColor.fromRegDword(result)

    def setDwmAccentColorInactive(self, value: ThemeColor):
        regDwordValue = value.toRegDword()
        self.__setRegistryIntValue(self.__DwmRegistrySubkey, self.__dwmAccentColorInactiveValue, regDwordValue)

    # Color Prevalence
    def getDwmColorPrevalence(self) -> bool:
        result, _ = self.__getRegistryIntValue(self.__DwmRegistrySubkey, self.__dwmColorPrevalenceValue)
        return bool(result)

    def setDwmColorPrevalence(self, value: bool):
        self.__setRegistryIntValue(self.__DwmRegistrySubkey, self.__dwmColorPrevalenceValue, int(value))

    # Accent Color Menu
    def getExplorerAccentColor(self) -> ThemeColor:
        result, _ = self.__getRegistryIntValue(self.__WindowsExplorerAccentRegistrySubkey, self.__explorerAccentColorMenuValue)
        return ThemeColor.fromRegDword(result)

    def setExplorerAccentColor(self, value: ThemeColor):
        regDwordValue = value.toRegDword()
        self.__setRegistryIntValue(self.__WindowsExplorerAccentRegistrySubkey, self.__explorerAccentColorMenuValue, regDwordValue)

    # Wallpaper
    def getWallpaper(self) -> (int, str):
        SPI_GETDESKWALLPAPER = 0x0073
        bufferSize = 200
        buffer = ctypes.create_unicode_buffer(bufferSize)

        success = ctypes.windll.user32.SystemParametersInfoW(
            SPI_GETDESKWALLPAPER,
            bufferSize,
            buffer,
            0
        )
        return success, str(buffer.value)

    def setWallpaper(self, absolutePath: str) -> int:
        SPI_SETDESKWALLPAPER = 0x0014
        success = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            absolutePath,
            0
        )
        return success
