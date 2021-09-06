import json
import re
import sys
from dataclasses import dataclass, asdict
from enum import Enum

from PIL import Image, ImageDraw, ImageFont


class VerticalReference(Enum):
    Top = 'Top',
    Bottom = 'Bottom'


class HorizontalReference(Enum):
    Left = 'Left',
    Right = 'Right'


@dataclass()
class Position:
    verticalReference: VerticalReference
    verticalOffset: int

    horizontalReference: HorizontalReference
    horizontalOffset: int

    def fromJsonObject(jsonObject: dict):
        return Position(
            verticalReference=VerticalReference[jsonObject['verticalReference']],
            verticalOffset=jsonObject['verticalOffset'],
            horizontalReference=HorizontalReference[jsonObject['horizontalReference']],
            horizontalOffset=jsonObject['horizontalOffset']
        )


@dataclass()
class Rectangle:
    x: int
    y: int
    width: int
    height: int

    def fromJsonObject(jsonObject: dict):
        return Rectangle(
            x=jsonObject['x'],
            y=jsonObject['y'],
            width=jsonObject['width'],
            height=jsonObject['height']
        )


@dataclass(init=False)
class SelCalCode:
    digit1: str
    digit2: str
    digit3: str
    digit4: str

    def __init__(self, text: str):
        ALLOWED_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'P', 'Q', 'R', 'S']
        transformedText = text.upper().strip().replace(' ', '')

        # Check sufficient length
        if len(transformedText) != 4:
            raise ValueError(f'SelCal squence "{transformedText}" is expected to be exactly 4 digits long.')

        # Iterate the first 4 characters
        occurrenceesList = []
        for i in range(4):
            digit = transformedText[i]

            # Check character is valid
            if digit not in ALLOWED_CHARACTERS:
                raise ValueError(f'Character "{digit}" is not valid as a SelCal digit.')

            # Check character has not been used already
            if digit in occurrenceesList:
                raise ValueError(f'Character "{digit}" already occurred in your SelCal code. Digits must be unique.')

            occurrenceesList.append(digit)

        def assertOrderInPart(firstDigit: str, secondDigit: str):
            if firstDigit > secondDigit:
                raise ValueError(f'Sequence "{firstDigit}{secondDigit}" is not allowed. Digits musst follow alphabetic order within their part.')

        # Check characters are alphabetically orderd within their part
        assertOrderInPart(transformedText[0], transformedText[1])
        assertOrderInPart(transformedText[2], transformedText[3])

        self.digit1 = transformedText[0]
        self.digit2 = transformedText[1]
        self.digit3 = transformedText[2]
        self.digit4 = transformedText[3]

    def getFirstPart(self) -> str:
        return f'{self.digit1}{self.digit2}'

    def getSecondPart(self) -> str:
        return f'{self.digit3}{self.digit4}'

    def getFullCode(self, delimiter: str = '-') -> str:
        return f'{self.getFirstPart()}{delimiter}{self.getSecondPart()}'

    def fromJsonObject(jsonObject: dict):
        return SelCalCode(
            text=f"{jsonObject['digit1']}{jsonObject['digit2']}{jsonObject['digit3']}{jsonObject['digit4']}"
        )


@dataclass(init=False)
class Callsign:

    airlineIcaoCode: str
    flightNumber: str

    def __init__(self, text: str):
        transformedText = text.upper().strip().replace(' ', '')

        # Check for minimum length
        if len(transformedText) < 4:
            raise ValueError(f'Callsign squence "{transformedText}" is too short.')

        # Check for maximum length
        if len(transformedText) > 7:
            raise ValueError(f'Callsign squence "{transformedText}" is too long.')

        # Check airline code
        airlineIcaoCode = transformedText[0:3]
        ICAO_AIRLINE_CODE_REGEX = r"^[A-Z]{3}$"
        if not re.match(ICAO_AIRLINE_CODE_REGEX, airlineIcaoCode):
            raise ValueError(f'Sequence "{airlineIcaoCode}" is not a valid ICAO airline code.')

        # Check flight number
        flightNumber = transformedText[3:]
        FLIGHT_NUMBER_REGEX = r"^[1-9]+[0-9]*[A-Z]*$"
        if not re.match(FLIGHT_NUMBER_REGEX, flightNumber):
            raise ValueError(f'Sequence "{flightNumber}" is not a valid flight number.')

        self.airlineIcaoCode = airlineIcaoCode
        self.flightNumber = flightNumber

    def getFullValue(self, delimiter: str =' ') -> str:
        return f'{self.airlineIcaoCode}{delimiter}{self.flightNumber}'

    def fromJsonObject(jsonObject: dict):
        return Callsign(
            text=f"{jsonObject['airlineIcaoCode']}{jsonObject['flightNumber']}"
        )


@dataclass()
class RgbColor:
    r: int
    g: int
    b: int

    def asTuple(self) -> (int, int, int):
        return (self.r, self.g, self.b)

    def fromJsonObject(jsonObject: dict):
        return RgbColor(
            r=jsonObject['r'],
            g=jsonObject['g'],
            b=jsonObject['b']
        )


@dataclass()
class TextStyle:
    fontName: str
    fontSize: int
    textColor: RgbColor
    position: Position

    def fromJsonObject(jsonObject: dict):
        return TextStyle(
            fontName=jsonObject['fontName'],
            fontSize=jsonObject['fontSize'],
            textColor=RgbColor.fromJsonObject(jsonObject['textColor']),
            position=Position.fromJsonObject(jsonObject['position'])
        )


@dataclass()
class Description:
    text: str
    style: TextStyle

    def fromJsonObject(jsonObject: dict):
        return Description(
            text=jsonObject['text'],
            style=TextStyle.fromJsonObject(jsonObject['style'])
        )

@dataclass(frozen=True)
class FlightPatch:
    rectangle: Rectangle

    aircraftRegistration: str
    aircraftRegistrationStyle: TextStyle

    selCalCode: SelCalCode
    selCalCodeStyle: TextStyle

    callsign: Callsign
    callsignStyle: TextStyle

    descriptions: [Description]

    def toJson(self, indent=4) -> str:

        def custom_asdict_factory(data):
            def convert_value(obj):
                if isinstance(obj, Enum):
                    return obj.name
                return obj

            return dict((k, convert_value(v)) for k, v in data)

        return json.dumps(asdict(self, dict_factory=custom_asdict_factory), indent=indent)

    def fromJsonObject(jsonObject: dict):
        descriptions = [Description.fromJsonObject(element) for element in jsonObject['descriptions']]

        return FlightPatch(
            rectangle=Rectangle.fromJsonObject(jsonObject['rectangle']),
            aircraftRegistration=jsonObject['aircraftRegistration'],
            aircraftRegistrationStyle=TextStyle.fromJsonObject(jsonObject['aircraftRegistrationStyle']),
            selCalCode=SelCalCode.fromJsonObject(jsonObject['selCalCode']),
            selCalCodeStyle=TextStyle.fromJsonObject(jsonObject['selCalCodeStyle']),
            callsign=Callsign.fromJsonObject(jsonObject['callsign']),
            callsignStyle=TextStyle.fromJsonObject(jsonObject['callsignStyle']),
            descriptions=descriptions
        )

    def fromFile(path: str):
        file = open(path)
        jsonObject = json.load(file)
        file.close()

        return FlightPatch.fromJsonObject(jsonObject)

    def toFile(self, path: str, indent=4):
        file = open(path, 'w')
        file.write(self.toJson(indent=indent))
        file.close()


class FlightPatchComposer:

    def __init__(self, backgroundImagePath: str):
        self.__backgroundImagePath = backgroundImagePath
        self.__image = Image.open(backgroundImagePath)

    def composePatch(self, patch: FlightPatch, registration=True, selCalCode=True, callsign=True, descriptions=True) -> Image:

        if registration:
            # Draw Aircraft Registration
            self._drawText(patch.aircraftRegistration, patch.aircraftRegistrationStyle, patch.rectangle)

        if selCalCode:
            # Draw SelCal Code
            self._drawText(patch.selCalCode.getFullCode(), patch.selCalCodeStyle, patch.rectangle)

        if callsign:
            # Draw Callsign
            self._drawText(patch.callsign.getFullValue(), patch.callsignStyle, patch.rectangle)

        if descriptions:
            # Draw Description Labels
            for description in patch.descriptions:
                self._drawText(description.text, description.style, patch.rectangle)

        return self.__image

    def _calculateAbsolutePositionForItem(self, rectange: Rectangle, position: Position, width: int, height: int) -> (int, int):
        x = -1
        y = -1

        # Y
        if position.verticalReference == VerticalReference.Top:
            # Top
            y = rectange.y + position.verticalOffset
        elif position.verticalReference == VerticalReference.Bottom:
            # Bottom
            y = rectange.y + rectange.height - height + position.verticalOffset
        else:
            y = -1

        # X
        if position.horizontalReference == HorizontalReference.Left:
            # Left
            x = rectange.x + position.horizontalOffset
        elif position.horizontalReference == HorizontalReference.Right:
            # Right
            x = rectange.x + rectange.width - width + position.horizontalOffset
        else:
            x = -1

        return (x, y)

    def _drawText(self, text: str, style: TextStyle, rectange: Rectangle):
        draw = ImageDraw.Draw(self.__image)
        font = ImageFont.truetype(style.fontName, style.fontSize)
        w, h = draw.textsize(text=text, font=font)
        x, y = self._calculateAbsolutePositionForItem(
            rectange=rectange,
            position=style.position,
            width=w,
            height=h
        )
        draw.text((x, y), text, style.textColor.asTuple(), font=font)

    def getImage(self) -> Image:
        return self.__image


if __name__ == '__main__':
    backgroundImagePath = 'C:\\Users\\thors\\Desktop\\msfs_2020_flat_panel_background_airbus_a320.png'

    patch = FlightPatch.fromFile('themes/a320/patch.json')

    composer = FlightPatchComposer(backgroundImagePath)
    image = composer.composePatch(patch)
    image.show()
    #image.save('test.png', 'PNG')
