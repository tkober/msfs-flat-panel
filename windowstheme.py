import winreg
from dataclasses import dataclass


@dataclass
class Theme:
    dwmAccentColor: int
    dwmAccentColorInactive: int
    dwmColorPrevalence: bool
    explorerAccentColorMenu: int


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

    # Accent Color
    def getDwmAccentColor(self) -> int:
        result, _ = self.__getRegistryIntValue(self.__DwmRegistrySubkey, self.__dwmAccentColorValue)
        return result

    def setDwmAccentColor(self, value: int):
        self.__setRegistryIntValue(self.__DwmRegistrySubkey, self.__dwmAccentColorValue, value)

    # Accent Color Inactive
    def getDwmAccentColorInactive(self) -> int:
        result, _ = self.__getRegistryIntValue(self.__DwmRegistrySubkey, self.__dwmAccentColorInactiveValue)
        return result

    def setDwmAccentColorInactive(self, value: int):
        self.__setRegistryIntValue(self.__DwmRegistrySubkey, self.__dwmAccentColorInactiveValue, value)

    # Color Prevalence
    def getDwmColorPrevalence(self) -> bool:
        result, _ = self.__getRegistryIntValue(self.__DwmRegistrySubkey, self.__dwmColorPrevalenceValue)
        return bool(result)

    def setDwmColorPrevalence(self, value: bool):
        self.__setRegistryIntValue(self.__DwmRegistrySubkey, self.__dwmColorPrevalenceValue, int(value))

    # Accent Color Menu
    def getExplorerAccentColor(self) -> int:
        result, _ = self.__getRegistryIntValue(self.__WindowsExplorerAccentRegistrySubkey, self.__explorerAccentColorMenuValue)
        return result

    def setExplorerAccentColor(self, value: int):
        self.__setRegistryIntValue(self.__WindowsExplorerAccentRegistrySubkey, self.__explorerAccentColorMenuValue, value)
