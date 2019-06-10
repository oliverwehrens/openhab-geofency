import requests

enter_leave = {
    "enter": "ON",
    "leave": "OFF"
}

openhab_base_url = ""


class Openhab:
    def __init__(self):
        config_file = open('openhab-config.txt', 'r', encoding='utf-8')
        self.openhab_base_url = config_file.read().rstrip('\n')
        config_file.close()
        print(f"Openhab Connection: {self.openhab_base_url}.")

    def inform(self, username: str, action: str, location: str):
        """
        Send the action to openhab for the current user and location. A switch named
        Presence_<NAME>_<LOCATION> needs to be available as item in Openhab.
        :param username: <NAME> part of the Presence_<NAME>_<LOCATION> switch
        :param action: enter/leave are supported from locative
        :param location: <LOCATION> part of the Presence_<NAME>_<LOCATION> switch
        :return: 200 or 404 response code
        """

        if action in enter_leave and username is not None and location is not None:
            headers = {'content-type': 'text/plain', 'Accept': 'application/json'}
            url = f"{self.openhab_base_url}/rest/items/Presence_{username}_{location}"
            requests.post(url, data=enter_leave.get(action), headers=headers)
            return True
        else:
            return False

