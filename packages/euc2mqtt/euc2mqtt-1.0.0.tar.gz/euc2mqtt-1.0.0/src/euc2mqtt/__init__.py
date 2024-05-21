from .EatonAPI import EatonClient
from .HassioAPI import HassioClient
from .InteropE2H import UpsDevice, UpsEntity, UpsEntityCollection

class UpdateHandler:
    on_register = []
    on_com_lost = []
    on_update = []
    on_unregister = []

    def __init__(self, name: str, eaton_host: str = 'localhost', eaton_port: int = 4679, mqtt_host: str = 'homeassistant.local', mqtt_port: int = 1883, mqtt_username: str = None, mqtt_password: str = None, mqtt_opts = {}):
        self._eaton_client = EatonClient(eaton_host, eaton_port)
        self._hassio_client = HassioClient(mqtt_host, mqtt_port, username=mqtt_username, password=mqtt_password, kv_opts=mqtt_opts)
        self._name = name
        self._last_update = 0
        self._collection = None

    def _add_sensors(self):
        c = self._collection
        c.add_sensor('status.outputPower', 'Output Power', 'power', 'W')
        c.add_sensor('status.energy', 'Energy', 'energy', 'kWh', 'total', lambda x: round(x / 3600.0 / 1000.0, 2))
        c.add_sensor('status.batteryCapacity', 'Battery Capacity', 'battery', '%')
        c.add_sensor('status.batteryRunTime', 'Battery Run Time', 'duration', 's')
        c.add_sensor('status.remainingCapacityLimit', 'Remaining Capacity Limit', None, '%')
        c.add_sensor('status.runTimeToShutdown', 'Run Time to Shutdown', 'duration', 's', update_func=lambda x: x if x > 0 else None)
        c.add_binary_sensor('status.acPresent', 'AC Present', 'power')
        c.add_binary_sensor('status.charging', 'Charging', 'battery_charging')
        c.add_binary_sensor('status.overload', 'Overload', 'problem')
        c.add_binary_sensor('status.outputStatus', 'Output', 'power')
        c.add_binary_sensor('status.internalFailure', 'Internal Failure', 'problem')
        c.add_binary_sensor('status.batteryLow', 'Battery Low', 'battery')
        c.add_binary_sensor('status.batteryFault', 'Battery Fault', 'problem')
        c.add_binary_sensor('status.shutdownImminent', 'Shutdown Imminent', 'problem')

    def _notify_register(self, entity: UpsEntity):
        for fn in self.on_register:
            fn(entity)

    def _notify_com_lost(self):
        for fn in self.on_com_lost:
            fn()

    def _notify_update(self, entity: UpsEntity, value):
        for fn in self.on_update:
            fn(entity, value)

    def _notify_unregister(self, entity: UpsEntity):
        for fn in self.on_register:
            fn(entity)

    def _register_entities(self):
        for i in range(0, len(self._collection.entities)):
            e = self._collection.entities[i]
            self._hassio_client.register(e, i > 0)
            self._notify_register(e)

    def _unregister_entities(self):
        for e in self._collection.entities:
            self._hassio_client.unregister(e)
            self._notify_unregister(e)

    def start(self):
        # Get initial data, create device and sensors
        device = UpsDevice(self._name,
                           self._eaton_client.get_data(),
                           self._eaton_client.admin_url)
        if self._name is None:
            self._name = device.name
        self._collection = UpsEntityCollection(self._name, device)
        self._add_sensors()
        # Start MQTT and register entities with Hassio
        self._hassio_client.start()
        self._register_entities()
        # Prepare update loop
        self._last_update = 0

    def update(self, full_update: bool = False):
        data = self._eaton_client.get_data(0 if full_update else self._last_update)
        if 'lastUpdate' in data:
            # Update reference timestamp
            self._last_update = data['lastUpdate']
        if ('status' in data) and ('comLost' in data['status']) and bool(data['status']['comLost']):
            # Communication loss
            for e in self._collection.entities:
                self._hassio_client.update_availability(e, False)
            self._notify_com_lost()
        for e in self._collection.entities:
            # Update sensors
            result = e.update(data)
            if result is not None:
                self._hassio_client.update_availability(e, True)
                self._hassio_client.update_state(e, result)
                self._notify_update(e, result)

    def stop(self):
        self._unregister_entities()
        self._hassio_client.stop()