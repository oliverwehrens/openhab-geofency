import requests
import os.path

enter_leave = {
    "enter": "ON",
    "leave": "OFF",
    "0": "OFF",
    "1": "ON"
}

openhab_base_url = ""
openhab_file = "conf/openhab-config.txt"
openhab_is_configured: bool


class Openhab:
    def __init__(self):
        self.openhab_is_configured = False
        if os.path.isfile(openhab_file):
            config_file = open('conf/openhab-config.txt', 'r', encoding='utf-8')
            self.openhab_base_url = config_file.read().rstrip('\n')
            config_file.close()
            print(f"Openhab Connection: {self.openhab_base_url}.")
            self.openhab_is_configured = True
        else:
            print(f"Could not find Openhab config file at '{openhab_file}'. Openhab is not configured.")

    def inform(self, username: str, action: str, location: str) -> bool:
        """
        Send the action to openhab for the current user and location. A switch named
        Presence_<NAME>_<LOCATION> needs to be available as item in Openhab.
        :param username: <NAME> part of the Presence_<NAME>_<LOCATION> switch
        :param action: enter/leave are supported from locative
        :param location: <LOCATION> part of the Presence_<NAME>_<LOCATION> switch
        :return: 200 or 404 response code
        """
        print(f"User: {username} Action: {action} Location: {location}")

        if action in enter_leave and username is not None and location is not None and self.openhab_is_configured:
            headers = {'content-type': 'text/plain', 'Accept': 'application/json'}
            url = f"{self.openhab_base_url}/rest/items/Presence_{username}_{location}"
            response = requests.post(url, data=enter_leave.get(action), headers=headers)
            if 200 <= response.status_code < 300:
                return True
            else:
                return False
        else:
            return False
