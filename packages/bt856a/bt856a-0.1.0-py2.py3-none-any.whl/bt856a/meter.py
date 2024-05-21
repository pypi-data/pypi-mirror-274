import enum
import typing
import struct
import dataclasses
from aenum import MultiValueEnum

cmd_readout_start = bytes.fromhex('eb a0')
cmd_readout_stop  = bytes.fromhex('eb b0')

number_multiplier = {
    0: 1.0,
    1: 1.0 / 10.0,
    2: 1.0 / 100.0,
    3: 1.0 / 1000.0,
}

class BT856AFrameLengthException( Exception ):
    pass

class BT856AMode(enum.Enum):
    VELOCITY = 'velocity'
    FLOW     = 'flow'

class BT856AVelocityUnit(MultiValueEnum):
    UNIT_NA     = "invalid", 0
    UNIT_m_s    = "m/s",     1
    UNIT_km_h   = "km/h",    2
    UNIT_ft_min = "ft/min",  3
    UNIT_knots  = "knots",   4
    UNIT_mph    = "mph",     5

class BT856ATemperatureUnit(MultiValueEnum):
    CELSIUS    = 'C', 0
    FAHRENHEIT = 'F', 1

class BT856AFlowUnit(enum.Enum):
     CMM = 'CMM'
     CFM = 'CFM'

class BT856AAreaUnit(enum.Enum):
    m2 = 'm2'
    ft2 = 'ft2'

class BT856AValueType( enum.Enum ):
    VAL_LIVE = 'live'
    VAL_23_MAX = '2/3 max'
    VAL_MIN = 'min'
    VAL_MAX = 'max'

@dataclasses.dataclass
class BT856AData:
    value_type: BT856AValueType
    is_max_value: bool
    is_min_value: bool
    is_23_max_value: bool
    is_live_value: bool
    mode: BT856AMode
    is_flow_mode: bool
    is_velocity_mode: bool
    flow: typing.Optional[float]
    flow_unit: typing.Optional[BT856AFlowUnit]
    area: typing.Optional[float]
    area_unit: typing.Optional[BT856AAreaUnit]
    velocity: typing.Optional[float]
    velocity_unit: typing.Optional[BT856AVelocityUnit]
    temperature: typing.Optional[float]
    temperature_unit: typing.Optional[BT856ATemperatureUnit]

def parseData( data: bytes ) -> BT856AData:
    if len(data) != 8:
        raise BT856AFrameLengthException()

    sof, a0, unit, multipliers, value1, value2 = struct.unpack('>BBBBHH', data)
    is_max_value     = (unit & 0xf0) == 0x80
    is_min_value     = (unit & 0xf0) == 0x40
    #is_???_value     = (unit & 0xf0) == 0x20
    is_23_max_value  = (unit & 0xf0) == 0x10
    is_live_value = (unit & 0xf0) == 0x00
    value_type = BT856AValueType.VAL_LIVE if is_live_value else ( BT856AValueType.VAL_23_MAX if is_23_max_value else ( BT856AValueType.VAL_MIN if is_min_value else (BT856AValueType.VAL_MAX if is_max_value else None) ) )

    is_flow_mode = (unit & 0x0f) == 0
    is_velocity_mode = not is_flow_mode
    mode = BT856AMode.FLOW if is_flow_mode else BT856AMode.VELOCITY
    temperature_unit = BT856ATemperatureUnit((unit & 0b00001000)>>3)
    velocity_unit = BT856AVelocityUnit(unit & 0b111)

    value1 = value1 * number_multiplier[ (multipliers & 0b1100) >> 2 ]
    value2 = value2 * number_multiplier[ (multipliers & 0b0011) >> 0 ]
    if (multipliers & 0b00110000) == 0x20:
        flow_unit = BT856AFlowUnit.CMM # Cubic Meter Per Minute (m3/min)
        area_unit = BT856AAreaUnit.m2
    elif (multipliers & 0b00110000) == 0x30:
        flow_unit = BT856AFlowUnit.CFM # Cubic Feet Per Minute (ft3/min)
        area_unit = BT856AAreaUnit.ft2
    else:
        flow_unit = None
        area_unit = None
    # Unknown bits: multipliers & (0b11000000) = ??? ## Related to the x10 / x100 ??

    if is_flow_mode:
        area = value1
        flow = value2
        temperature = None
        velocity =  None
    else:
        area = None
        flow =  None
        temperature = value1
        velocity = value2

    return BT856AData(
        value_type = value_type,
        is_max_value = is_max_value,
        is_min_value = is_min_value,
        is_23_max_value = is_23_max_value,
        is_live_value = is_live_value,
        mode = mode,
        is_flow_mode = is_flow_mode,
        is_velocity_mode = is_velocity_mode,
        flow = flow,
        flow_unit = flow_unit,
        area = area,
        area_unit = area_unit,
        velocity = velocity,
        velocity_unit = velocity_unit,
        temperature = temperature,
        temperature_unit = temperature_unit,
    )
