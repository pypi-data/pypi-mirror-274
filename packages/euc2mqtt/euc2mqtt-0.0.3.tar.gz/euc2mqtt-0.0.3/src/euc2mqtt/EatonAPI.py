from enum import StrEnum
import requests

class EatonClient:
    """EatonClient([hostname, [port]])

    API Client for the Eaton UPS Companion webservice.

    This client grants access to API functions of the Eaton UPS Companion
    webservice. The service is installed as part of the Eaton UPS Companion
    software, and is usually accessible at address 'http://localhost:4679/'.
    The API entrypoint is located under path `/euc-data.js`,

    Usage:
        ```python
        client = EatonClient()
        data = client.get_data()
        print(f"AC power status: {data['status']['acPresent']}")
        ```
    """

    API_ENDP_PATH: str = '/euc-data.js'

    class Command(StrEnum):
        GET_DATA = 'getData'
        SET_DATA = 'setData'
        CLEAR_LOGS = 'clearLogs'

    def __init__(self, hostname: str = 'localhost', port: int = 4679):
        """Create a new client.

        Args:
            hostname (str, optional): Hostname of the UPS Companion webservice. Defaults to 'localhost'.
            port (int, optional): Webservice port number. Defaults to 4679.
        """
        self._base_url =  f"http://{hostname}:{port}"
        self._api_endpoint = f"{self._base_url}{self.API_ENDP_PATH}"

    def _transfer(self, cmd: Command, data: dict = {}) -> dict:
        response = requests.post(self._api_endpoint, json={'cmd': cmd, **data})
        response.raise_for_status()
        return response.json()

    @property
    def admin_url(self) -> str:
        """Get the Eaton UPS Companion Webadmin URL."""
        return f"{self._base_url}/"

    def get_data(self, from_date: int = 0) -> dict:
        """Get system and UPS status data.

        Args:
            from_date (int, optional): Timestamp of last update (see Usage below). Defaults to 0.

        Returns:
            dict: Parsed JSON data structure containing system and UPS status data.

        Usage:
            ```python
            client = EatonClient()

            last_update = 0 # Request all data
            while (True):
                data = client.get_data(last_update)
                last_update = data['lastUpdate'] # Only fetch changes on next query
                # ...
            ```
        """
        return self._transfer(self.Command.GET_DATA, {'fromDate': from_date})

    def set_data(self, item_path: str, value: str) -> None:
        """Set configuration item value.

        Args:
            item_path (str): Item path as specified in the EUC web UI, formatted as `<subset>.<item_id>`.
            value (str): New item value.

        Usage:
            ```python
            client = EatonClient()
            client.set_data('systemCfg.systemTray', True)
            ```
        """
        [subset, item_id] = item_path.split('.')
        self._transfer(self.Command.SET_DATA, {'subset': subset, 'itemID': item_id, 'itemValue': value})

    def clear_logs(self) -> None:
        """Clear UPS Companion event history.

        Usage:
            ```python
            client = EatonClient()
            client.clear_logs()
            ```
        """
        self._transfer(self.Command.CLEAR_LOGS)
