import argparse
import logging
import sys
import time
from . import UpdateHandler

class DefaultConfig:
    EUC_HOST: str = 'localhost'
    EUC_PORT: int = 4679
    HASSIO_HOST: str = 'homeassistant.local'
    HASSIO_PORT: int = 1883
    INTERVAL: int = 30
    FULL_UPDATE_INTERVAL: int = 9

def main():
    parser = argparse.ArgumentParser(prog='euc2mqtt', description='MQTT Publisher for Eaton UPS Companion status messages to Home Assistant. See https://github.com/islandcontroller/euc2mqtt for more info!')
    parser.add_argument('--name', help='Device name', type=str, default=None)
    parser.add_argument('--mqtt', help='MQTT broker hostname and port (hostname[:port])', type=str, default=f"{DefaultConfig.HASSIO_HOST}:{DefaultConfig.HASSIO_PORT}")
    parser.add_argument('--euc', help='Eaton UPS Companion hostname and port (hostname[:port])', type=str, default=f"{DefaultConfig.EUC_HOST}:{DefaultConfig.EUC_PORT}")
    parser.add_argument('--username', help='Username for MQTT broker authentication', type=str, default=None)
    parser.add_argument('--password', help='Password for MQTT broker authentication', type=str, default=None)
    parser.add_argument('--interval', help='Update interval in seconds', type=int, default=DefaultConfig.INTERVAL)
    parser.add_argument('--full-update', help='Number of incremental dataset fetches between full updates', type=int, default=DefaultConfig.FULL_UPDATE_INTERVAL)
    parser.add_argument('--logfile', help='Output log messages to a file', type=str, default=None)
    parser.add_argument('--verbose', help='Enable verbose logging', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(filename=args.logfile,
                        level=logging.DEBUG if args.verbose else logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S%z')
    sys.excepthook = lambda type, value, tb: logging.log(logging.ERROR, f"Caught unhandled exception: {value}")
    
    eaton_conf = args.euc.split(':')
    eaton_host = eaton_conf[0]
    eaton_port = DefaultConfig.EUC_PORT if len(eaton_conf) < 2 else int(eaton_conf[1], base=10)
    logging.log(logging.DEBUG, f"Using EUC service at {eaton_host}:{eaton_port}")

    mqtt_conf = args.mqtt.split(':')
    mqtt_host = mqtt_conf[0]
    mqtt_port = DefaultConfig.HASSIO_PORT if len(mqtt_conf) < 2 else int(mqtt_conf[1], base=10)
    logging.log(logging.DEBUG, f"Using MQTT broker at {mqtt_host}:{mqtt_port}")

    logging.log(logging.INFO, 'Configuring update handler...')
    handler = UpdateHandler(args.name, eaton_host, eaton_port, mqtt_host, mqtt_port, args.username, args.password)
    handler.on_com_lost = [lambda: logging.log(logging.WARNING, 'EUC lost communication with UPS')]
    handler.on_register = [lambda e: logging.log(logging.DEBUG, f"Entity registered: {e.unique_id}")]
    handler.on_update = [lambda e, v: logging.log(logging.DEBUG, f"Entity updated: {e.unique_id} = {v}")]
    handler.on_unregister = [lambda e: logging.log(logging.DEBUG, f"Entity unregistered: {e.unique_id}")]

    logging.log(logging.INFO, f"Starting update loop ({args.interval}s update interval)...")
    handler.start()
    update_count = 0
    while True:
        try:
            logging.log(logging.DEBUG, f"Fetching {'full' if update_count == 0 else 'incremental'} dataset")
            handler.update(update_count == 0)
            if update_count == 0:
                update_count = max(args.full_update, 0)
            else:
                update_count -= 1
            time.sleep(args.interval)
        except KeyboardInterrupt:
            logging.log(logging.WARNING, 'Caught KeyboardInterrupt, exiting...')
            break
    logging.log(logging.INFO, 'Stopping update loop...')
    handler.stop()