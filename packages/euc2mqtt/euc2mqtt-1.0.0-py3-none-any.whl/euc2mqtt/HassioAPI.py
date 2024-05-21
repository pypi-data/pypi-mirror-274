from enum import StrEnum
import json
import paho.mqtt.client as mqtt
import platform

class HassioDevice:
    identifiers: list[str] = None
    name: str = None
    manufacturer: str = None
    model: str = None
    serial_number: str = None
    sw_version: str = None
    configuration_url: str = None

    def __init__(self, identifiers: list[str], name: str, manufacturer: str, model: str, serial_number: str, sw_version: str, configuration_url: str):
        self.identifiers = identifiers
        self.name = name
        self.manufacturer = manufacturer
        self.model = model
        self.serial_number = serial_number
        self.sw_version = sw_version
        self.configuration_url = configuration_url

    @property
    def discovery_data(self) -> dict:
        return {
            "identifiers": self.identifiers,
            "name": self.name,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "serial_number": self.serial_number,
            "sw_version": self.sw_version,
            "configuration_url": self.configuration_url
        }

class HassioComponent(StrEnum):
    SENSOR = 'sensor'
    BINARY_SENSOR = 'binary_sensor'

class HassioEntity:
    component: HassioComponent = None
    name: str = None
    device_class: str = None
    unique_id: str = None
    device: HassioDevice = None

    def __init__(self, component: HassioComponent, name: str, device_class: str | None, unique_id: str, device: HassioDevice):
        self.component  = component
        self.name = name
        self.device_class = device_class
        self.unique_id = unique_id
        self.device = device

    @property
    def topic(self) -> str:
        return f"{self.component}/{self.unique_id}"

    @property
    def discovery_data(self) -> dict:
        return {
            "name": self.name,
            "device_class": self.device_class,
            "unique_id": self.unique_id
        }

class HassioBinarySensorEntity(HassioEntity):
    def __init__(self, name: str, device_class: str | None, unique_id: str, device: HassioDevice):
        super().__init__(HassioComponent.BINARY_SENSOR, name, device_class, unique_id, device)

class HassioSensorEntity(HassioEntity):
    unit_of_measurement: str = None
    state_class: str = None

    def __init__(self, name: str, device_class: str | None, unit_of_measurement: str | None, state_class: str | None, unique_id: str, device: HassioDevice):
        super().__init__(HassioComponent.SENSOR, name, device_class, unique_id, device)
        self.unit_of_measurement = unit_of_measurement
        self.state_class = state_class

    @property
    def discovery_data(self) -> dict:
        return {
            **super().discovery_data,
            "unit_of_measurement": self.unit_of_measurement,
            "state_class": self.state_class
        }

class HassioClient:
    def __init__(self, host: str = 'homeassistant.local', port: int = 1883, discovery_prefix: str = 'homeassistant', username: str = None, password: str = None, kv_opts = {}):
        self._host = host
        self._port = port
        self._prefix = discovery_prefix
        self._mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, platform.node(), **kv_opts)
        self._mqtt.username_pw_set(username, password)

    def _entity_topic(self, entity: HassioEntity) -> str:
        return f"{self._prefix}/{entity.topic}"

    def _discovery_topic(self, entity: HassioEntity) -> str:
        return f"{self._entity_topic(entity)}/config"

    def _state_topic(self, entity: HassioEntity) -> str:
        return f"{self._entity_topic(entity)}/state"
    
    def _availability_topic(self, entity: HassioEntity) -> str:
        return f"{self._entity_topic(entity)}/availability"

    def start(self) -> None:
        res = self._mqtt.connect(self._host, self._port)
        if res != mqtt.MQTTErrorCode.MQTT_ERR_SUCCESS:
            raise ConnectionError(res)
        self._mqtt.loop_start()

    def stop(self) -> None:
        self._mqtt.loop_stop()

    def register(self, entity: HassioEntity, device_ident_only: bool = False) -> None:
        payload = json.dumps({
            **entity.discovery_data,
            "state_topic": self._state_topic(entity),
            "availability_topic": self._availability_topic(entity),
            "device": {
                "identifiers": entity.device.identifiers
            } if device_ident_only else {
                **entity.device.discovery_data
            }
        })
        self._mqtt.publish(self._discovery_topic(entity), payload, qos=1, retain=True).wait_for_publish()

    def unregister(self, entity: HassioEntity) -> None:
        self._mqtt.publish(self._discovery_topic(entity), '', qos=1).wait_for_publish()

    def update_availability(self, entity: HassioEntity, available: bool) -> None:
        self._mqtt.publish(self._availability_topic(entity), 'online' if available else 'offline').wait_for_publish()

    def update_state(self, entity: HassioEntity, payload) -> None:
        self._mqtt.publish(self._state_topic(entity), payload).wait_for_publish()