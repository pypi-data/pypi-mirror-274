from euc2mqtt.HassioAPI import HassioComponent
from .HassioAPI import HassioDevice, HassioSensorEntity, HassioBinarySensorEntity, HassioEntity
from .Utility import id_format

class UpsDevice(HassioDevice):
    def __init__(self, name: str, data: dict, config_url: str):
        super().__init__(identifiers=[data['status']['serialNumber']],
                         name=name if name is not None else data['deviceInfo']['name'],
                         manufacturer=data['sysInfo']['manufacturer'],
                         model=f"{data['status']['product']} {data['status']['model']}",
                         serial_number=data['status']['serialNumber'],
                         sw_version=data['status']['firmwareVersion'],
                         configuration_url=config_url)

class UpsEntityMixin:
    def __init__(self, path: str) -> None:
        self._path = path

    def update(self, data: dict):
        for p in self._path.split('.'):
            if p in data:
                data = data[p]
            else:
                return None
        return self.on_update(data)

    def on_update(self, data):
        return None

class UpsEntity(HassioEntity, UpsEntityMixin):
    def __init__(self, path: str, component: HassioComponent, name: str, device_class: str | None, unique_id: str, device: HassioDevice):
        HassioEntity.__init__(self, component, name, device_class, unique_id, device)
        UpsEntityMixin.__init__(self, path)

class UpsSensorEntity(HassioSensorEntity, UpsEntityMixin):
    def __init__(self, path: str, name: str, device_class: str | None, unit_of_measurement: str | None, state_class: str | None, unique_id: str, device: HassioDevice, update_func):
        HassioSensorEntity.__init__(self, name, device_class, unit_of_measurement, state_class, unique_id, device)
        UpsEntityMixin.__init__(self, path)
        self._update_func = update_func

    def on_update(self, data):
        return self._update_func(data)

class UpsBinarySensorEntity(HassioBinarySensorEntity, UpsEntityMixin):
    def __init__(self, path: str, name: str, device_class: str | None, unique_id: str, device: HassioDevice):
        HassioBinarySensorEntity.__init__(self, name, device_class, unique_id, device)
        UpsEntityMixin.__init__(self, path)

    def on_update(self, data):
        return 'ON' if bool(data) else 'OFF'

class UpsEntityCollection:
    def __init__(self, name: str, device: UpsDevice):
        self._name = name
        self._device = device
        self._entities = []

    @property
    def entities(self) -> list[UpsEntity]:
        return self._entities

    def add_sensor(self, path: str, name: str, device_class: str | None, unit_of_measurement: str | None = None, state_class: str | None = 'measurement', update_func = lambda x: x):
        sensor = UpsSensorEntity(path=path,
                                   name=name,
                                   device_class=device_class,
                                   unit_of_measurement=unit_of_measurement,
                                   state_class=state_class,
                                   unique_id=id_format(f"{self._name} {name}").lower(),
                                   device=self._device,
                                   update_func=update_func)
        self._entities.append(sensor)

    def add_binary_sensor(self, path: str, name: str, device_class: str | None):
        binary_sensor = UpsBinarySensorEntity(path=path,
                                                name=name,
                                                device_class=device_class,
                                                unique_id=id_format(f"{self._name} {name}").lower(),
                                                device=self._device)
        self._entities.append(binary_sensor)