
# Library description

This library allows you live readout the data from the BTMETER BT-856A Digital Anemometer (https://www.btmeter-store.com/products/bt-meter-bt-856a-digital-vane-anemometer-usb)

Example usage:

```
$ pip install bt856a

$ bt856a --help
usage: bt856a [-h] [--debug] [--output {text,json,none}] [--mqtt-host MQTT_HOST] [--mqtt-port MQTT_PORT] [--mqtt-username MQTT_USERNAME]
              [--mqtt-password MQTT_PASSWORD] [--mqtt-topic MQTT_TOPIC] [--mqtt-json]
              serial_port

Readout software for the BTMETER BT-856A digital anemometer

positional arguments:
  serial_port           Serial port where the BT-856A is connected

options:
  -h, --help            show this help message and exit
  --debug, -d           Enable debug mode (default: False)
  --output {text,json,none}, -o {text,json,none}
                        Data output format (default: text)
  --mqtt-host MQTT_HOST
                        MQTT Server hostname to send the data to (set to enable sending to the mqtt server) (default: None)
  --mqtt-port MQTT_PORT
                        MQTT Server port to send the data to (default: 1883)
  --mqtt-username MQTT_USERNAME
                        MQTT Server username (default: None)
  --mqtt-password MQTT_PASSWORD
                        MQTT Server password (default: None)
  --mqtt-topic MQTT_TOPIC
                        MQTT Server topic (default: bt856a)
  --mqtt-json           Send data to the MQTT Server as json instead of separate topics (default: False)

$ bt856a /dev/ttyUSB0 # Or COM_
INFO:root:Sending readout start command (it might take a while for the meter to pick this up)
INFO:root:Received frame with invalid start byte
Flow live: 32.47CMM | 1.2m2
Flow live: 33.76CMM | 1.2m2
Flow live: 33.55CMM | 1.2m2
Flow live: 27.64CMM | 1.2m2
Velocity live: 0.327m/s | 22.0C
Velocity live: 0.364m/s | 22.0C
Velocity live: 0.489m/s | 22.0C
```

# Meter protocol

The connection is a serial connection over a USB cable (via a CP2102 to UART Bridge Controller in the meter). The serial parameters used by the device are:

* Baudrate: 9600
* Databits: 8
* Parity: None
* Stopbits: 1


## Commands

The following commands are known:

| Command | Description   | Notes         |
| :------ | :------------ | :------------ |
| 0xeba0  | Start readout | Request the meter to start sending data |
| 0xebb0  | Stop readout  | Request the meter to stop sending data |

## Readout format

Data is 8 bytes long and is send in big-endian format;

> 0x eb a0 b1 b2 v1 v1 v2 v2

| Byte      | Description        | Notes      |
| :-------- | :----------------- | :--------- |
| 0xeb      | Start of frame     | Indicates the beginning of the packet |
| 0xa0      | Packet type        | Always seems to be 0xa0 |
| b1 & 0x80 | Max mode           | Set when the meter is in max mode |
| b1 & 0x40 | Min mode           | Set when the meter is in min mode |
| b1 & 0x20 | ???                | ??? |
| b1 & 0x10 | 2/3 Max mode       | Set when the meter is in 2/3 max mode |
| b1 & 0x08 | Temperature unit   | 0=C / 1=F |
| b1 & 0x07 | Velocity unit      | 0=Not in velocity mode (in flow mode) / 1=m/s 2=km/h 3=ft/min 4=knots 5=mph|
| b2 & 0xC0 | ???                | ??? |
| b2 & 0x30 | Flow unit          | 0x20=CMM 0x30=CFM |
| b2 & 0x0C | Value 1 multiplier | 0b00=*1 0b01=*1/10 0b10=*1/100 0b11=*1/1000 |
| b2 & 0x03 | Value 2 multiplier | 0b00=*1 0b01=*1/10 0b10=*1/100 0b11=*1/1000 |
| v1 v1     | Value 1            | 2-byte BE short encoding value1: Temperature in velocity mode, area in flow mode |
| v2 v2     | Value 1            | 2-byte BE short encoding value1: Velocity in velocity mode, flow in flow mode |
