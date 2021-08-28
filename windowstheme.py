import winreg

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
