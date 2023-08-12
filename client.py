import json
import time
from string import Template

import websocket
import requests

from vm import VirtualMachine


class Config:
    def __init__(self, url: str, username: str, password: str):
        self.Url = url
        self.Username = username
        self.Password = password


# self.http_url = f'http://{url}/rest/v0'
# self.http_cookie = {'authenticationToken': token}

class Client:
    def __init__(self, config: Config):
        url = config.Url
        username = config.Username
        password = config.Password

        signinPayload = Template('''{
                "method": "session.signInWithPassword",
                "params": {
                    "email": "$username",
                    "password": "$password"
                },
                "id": $callID,
                "jsonrpc": "2.0"
            }''')

        tokenPayload = Template('''{
                        "method": "token.create",
                        "params": {},
                        "id": $callID,
                        "jsonrpc": "2.0"
                    }''')

        self.ws = websocket.WebSocket()
        # websocket.enableTrace(True)
        self.ws.connect(f'ws://{url}/api/')
        self.ws.send(signinPayload.substitute({'username': username, 'password': password, 'callID': time.time_ns()}))
        print(self.ws.recv())
        self.ws.send(tokenPayload.substitute({'callID': time.time_ns()}))
        t = self.ws.recv()
        token = json.loads(t)
        self.http_url = f'http://{url}/rest/v0'
        self.http_cookie = {'authenticationToken': token['result']}

    def __del__(self):
        print("calling ws close")
        self.ws.close()

    def get_vm(self, uuid: str) -> VirtualMachine:
        r = requests.get(f'{self.http_url}/vms/{uuid}', cookies=self.http_cookie)
        r = r.json()
        return VirtualMachine(r['uuid'], r['name_label'], r['name_description'], r['power_state'], r['tags'], r['addresses'], r['$VBDs'], r['current_operations'], r['$container'], r['$pool'])

    def get_vms(self) -> list[VirtualMachine]:
        r = requests.get(f'{self.http_url}/vms?fields=uuid,name_label,name_description,power_state,tags,addresses,$VBDs,current_operations,$container,$pool', cookies=self.http_cookie)
        v: list[VirtualMachine] = []
        for vm in r.json():
            m = VirtualMachine(vm['uuid'], vm['name_label'], vm['name_description'], vm['power_state'], vm['tags'], vm['addresses'], vm['$VBDs'], vm['current_operations'], vm['$container'], vm['$pool'])
            v.append(m)
        return v


if __name__ == "__main__":
    c = Client(Config('10.10.20.50', 'ha', 'py965hyb'))
