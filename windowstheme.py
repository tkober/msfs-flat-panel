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


@dataclass
class Theme:
    dwmAccentColor: ThemeColor
    dwmAccentColorInactive: ThemeColor
    dwmColorPrevalence: bool
    explorerAccentColorMenu: ThemeColor

    def toJson(self, indent=4) -> str:
        return json.dumps(asdict(self), indent=indent)


class WindowsTheme:

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

    def currentTheme(self) -> Theme:
        return Theme(
            dwmAccentColor=self.getDwmAccentColor(),
            dwmAccentColorInactive=self.getDwmAccentColorInactive(),
            dwmColorPrevalence=self.getDwmColorPrevalence(),
            explorerAccentColorMenu=self.getExplorerAccentColor()
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
