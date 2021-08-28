import winreg

class WindowsDwm:

    def __init__(self, rootHkey=winreg.HKEY_CURRENT_USER):
        self.__registryHkey = rootHkey
        self.__registrySubkey = 'SOFTWARE\Microsoft\Windows\DWM'
        self.__accentColorValue = 'AccentColor'
        self.__accentColorInactiveValue = 'AccentColorInactive'
        self.__colorPrevalenceValue = 'ColorPrevalence'

    def __getDwmValue(self, valueName: str) -> (int, int):
        keyh = winreg.OpenKey(self.__registryHkey, self.__registrySubkey)
        value, type = winreg.QueryValueEx(keyh, valueName)
        keyh.Close()
        return (value, type)

    def __setDwmValue(self, valueName: str, value: int):
        keyh = winreg.OpenKey(self.__registryHkey, self.__registrySubkey, access=winreg.KEY_SET_VALUE)
        winreg.SetValueEx(keyh, valueName, 0, winreg.REG_DWORD, value)
        keyh.Close()

    # Accent Color
    def getAccentColor(self) -> int:
        result, _ = self.__getDwmValue(self.__accentColorValue)
        return result

    def setAccentColor(self, value: int):
        self.__setDwmValue(self.__accentColorValue, value)

    # Accent Color Inactive
    def getAccentColorInactive(self) -> int:
        result, _ = self.__getDwmValue(self.__accentColorInactiveValue)
        return result

    def setAccentColorInactive(self, value: int):
        self.__setDwmValue(self.__accentColorInactiveValue, value)

    # Color Prevalence
    def getColorPrevalence(self) -> bool:
        result, _ = self.__getDwmValue(self.__colorPrevalenceValue)
        return bool(result)

    def setColorPrevalence(self, value: bool):
        self.__setDwmValue(self.__colorPrevalenceValue, int(value))
