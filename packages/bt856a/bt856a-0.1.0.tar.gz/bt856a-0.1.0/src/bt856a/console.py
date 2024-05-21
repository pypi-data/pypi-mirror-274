
import paho.mqtt.client
import serial
import json
import argparse
import dataclasses
import logging

import bt856a

def run():
    parser = argparse.ArgumentParser(description='Readout software for the BTMETER BT-856A digital anemometer', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--debug', '-d', help="Enable debug mode", action='store_true', default=False)
    parser.add_argument('--output', '-o', help="Data output format", choices=["text", "json", "none"], default="text")
    parser.add_argument('--mqtt-host', help="MQTT Server hostname to send the data to (set to enable sending to the mqtt server)", default=None)
    parser.add_argument('--mqtt-port', help="MQTT Server port to send the data to", default=1883)
    parser.add_argument('--mqtt-username', help="MQTT Server username", default=None)
    parser.add_argument('--mqtt-password', help="MQTT Server password", default=None)
    parser.add_argument('--mqtt-topic', help="MQTT Server topic", default='bt856a')
    parser.add_argument('--mqtt-json', help="Send data to the MQTT Server as json instead of separate topics", default=False, action='store_true')
    parser.add_argument('serial_port', help="Serial port where the BT-856A is connected")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    if args.mqtt_host:
        client = paho.mqtt.client.Client()
        if args.mqtt_username or args.mqtt_password:
            client.username_pw_set(args.mqtt_username, args.mqtt_password)
        client.connect( args.mqtt_host, args.mqtt_port )

    connection = serial.Serial( port=args.serial_port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.8 )
    try:
        while not connection.read():
            logging.info('Sending readout start command (it might take a while for the meter to pick this up)')
            connection.write( bt856a.cmd_readout_start )
        connection.flush()
        
        while True:
            data = connection.read(8)
            if not data:
                continue # timeout

            logging.debug(f"Received frame: {data.hex(' ')}")
            if data[0] != 0xeb:
                logging.info("Received frame with invalid start byte")
                continue

            try:
                parsed_data = bt856a.parseData( data )
                if args.output == "text":
                    if parsed_data.is_flow_mode:
                        print(f"Flow {parsed_data.value_type.value}: {parsed_data.flow}{parsed_data.flow_unit.value} | {parsed_data.area}{parsed_data.area_unit.value}")
                    else:
                        print(f"Velocity {parsed_data.value_type.value}: {parsed_data.velocity}{parsed_data.velocity_unit.value} | {parsed_data.temperature}{parsed_data.temperature_unit.value}")
                elif args.output == "json":
                    print(json.dumps(dataclasses.asdict(parsed_data), default=lambda x: x.value))
                
                if args.mqtt_host:
                    mqtt_data = json.dumps(dataclasses.asdict(parsed_data), default=lambda x: x.value)
                    if args.mqtt_json:
                        client.publish(f"{args.mqtt_topic}/json", mqtt_data)
                    else:
                        for key, value in json.loads(mqtt_data).items():
                            client.publish(f"{args.mqtt_topic}/{key}", value)

            except bt856a.BT856AFrameLengthException:
                logging.warning(f"Expected only 8 bytes of data but got {len(data)}: {data.hex(' ')}")

    finally:
        if args.mqtt_host:
            client.disconnect()
        connection.write( bt856a.cmd_readout_stop )

if __name__ == "__main__":
    run()
