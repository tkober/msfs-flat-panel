import json
from dataclasses import dataclass, asdict
from enum import Enum

from flightpatch import FlightPatch
from windowstheme import Theme, WindowsThemeInterface


@dataclass()
class FlatPanelConfig:
    manufacturer: str
    aircraftType: str
    typeDesignatorIcao: str
    addFlightPatch: bool

    addRegistration: bool
    askForRegistration: bool
    defaultRegistrationOnEmpty: bool

    addSelCalCode: bool
    askForSelCalCode: bool
    defaultSelCalCodeOnEmpty: bool

    addCallsign: bool
    askForCallsign: bool
    defaultCallsignOnEmpty: bool

    addDescriptions: bool

    theme: Theme
    flightPatch: FlightPatch
    backgroundImage: str

    def toJson(self, indent=4) -> str:

        def custom_asdict_factory(data):
            def convert_value(obj):
                if isinstance(obj, Enum):
                    return obj.name
                return obj

            return dict((k, convert_value(v)) for k, v in data)

        return json.dumps(asdict(self, dict_factory=custom_asdict_factory), indent=indent)

    def fromJsonObject(jsonObject: dict):
        return FlatPanelConfig(
            manufacturer=jsonObject['manufacturer'],
            aircraftType=jsonObject['aircraftType'],
            typeDesignatorIcao=jsonObject['typeDesignatorIcao'],
            addFlightPatch=jsonObject['addFlightPatch'],
            addRegistration=jsonObject['addRegistration'],
            askForRegistration=jsonObject['askForRegistration'],
            defaultRegistrationOnEmpty=jsonObject['defaultRegistrationOnEmpty'],
            addSelCalCode=jsonObject['addSelCalCode'],
            askForSelCalCode=jsonObject['askForSelCalCode'],
            defaultSelCalCodeOnEmpty=jsonObject['defaultSelCalCodeOnEmpty'],
            addCallsign=jsonObject['addCallsign'],
            askForCallsign=jsonObject['askForCallsign'],
            defaultCallsignOnEmpty=jsonObject['defaultCallsignOnEmpty'],
            addDescriptions=jsonObject['addDescriptions'],
            theme=Theme.fromJsonObject(jsonObject['theme']),
            flightPatch=FlightPatch.fromJsonObject(jsonObject['flightPatch']),
            backgroundImage=jsonObject['backgroundImage']
        )

    def fromFile(path: str):
        file = open(path)
        jsonObject = json.load(file)
        file.close()

        return FlatPanelConfig.fromJsonObject(jsonObject)

    def toFile(self, path: str, indent=4):
        file = open(path, 'w')
        file.write(self.toJson(indent=indent))
        file.close()