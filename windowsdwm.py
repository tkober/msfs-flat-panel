import winreg

class WindowsDwm:

    def __init__(self, rootHkey=winreg.HKEY_CURRENT_USER):
        self.__registryHkey = rootHkey
        self.__registrySubkey = 'SOFTWARE\Microsoft\Windows\DWM'
        self.__accentColorValue = 'AccentColor'
        self.__accentColorInactive = 'AccentColorInactive'
        self.__colorPrevalence = 'ColorPrevalence'

    def __getDwmValue(self, valueName: str) -> (int, int):
        keyh = winreg.OpenKey(self.__registryHkey, self.__registrySubkey)
        value, type = winreg.QueryValueEx(keyh, valueName)
        return (value, type)

    def getAccentColor(self) -> int:
        result, _ = self.__getDwmValue(self.__accentColorValue)
        return result

    def getAccentColorInactive(self) -> int:
        result, _ = self.__getDwmValue(self.__accentColorInactive)
        return result

    def getColorPrevalence(self) -> bool:
        result, _ = self.__getDwmValue(self.__colorPrevalence)
        return bool(result)
