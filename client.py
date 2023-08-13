import json
import time
from string import Template

import websocket
import requests

from host import Host
from pool import Pool
from sr import StorageRepository
from vm import VirtualMachine


# self.http_url = f'http://{url}/rest/v0'
# self.http_cookie = {'authenticationToken': token}

class Client:
    def __init__(self, url: str, username: str, password: str):
        signin_payload = Template('''{
                "method": "session.signInWithPassword",
                "params": {
                    "email": "$username",
                    "password": "$password"
                },
                "id": $callID,
                "jsonrpc": "2.0"
            }''')

        token_payload = Template('''{
                        "method": "token.create",
                        "params": {},
                        "id": $callID,
                        "jsonrpc": "2.0"
                    }''')

        self.ws = websocket.WebSocket()
        # websocket.enableTrace(True)
        self.ws.connect(f'ws://{url}/api/')
        self.ws.send(signin_payload.substitute({'username': username, 'password': password, 'callID': time.time_ns()}))
        print(self.ws.recv())
        self.ws.send(token_payload.substitute({'callID': time.time_ns()}))
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

    def get_pool(self, uuid: str) -> Pool:
        r = requests.get(f'{self.http_url}/pools/{uuid}', cookies=self.http_cookie)
        r = r.json()
        return Pool(r['HA_enabled'], r['haSrs'], r['master'], r['tags'], r['name_description'], r['name_label'], r['uuid'])

    def get_pools(self) -> list[Pool]:
        r = requests.get(f'{self.http_url}/pools?fields=HA_enabled,haSrs,master,tags,name_description,name_label,cpus,uuid', cookies=self.http_cookie)
        v: list[Pool] = []
        for pool in r.json():
            p = Pool(pool['HA_enabled'], pool['haSrs'], pool['master'], pool['tags'], pool['name_description'], pool['name_label'], pool['uuid'])
            v.append(p)
        return v

    def get_host(self, uuid: str) -> Host:
        r = requests.get(f'{self.http_url}/hosts/{uuid}', cookies=self.http_cookie)
        r = r.json()
        return Host(r['hostname'], r['name_description'], r['name_label'], r['memory'], r['power_state'], r['residentVms'], r['rebootRequired'], r['tags'], r['uuid'], r['$pool'])

    def get_hosts(self) -> list[Host]:
        r = requests.get(f'{self.http_url}/hosts?fields=hostname,name_description,name_label,memory,power_state,residentVms,rebootRequired,tags,uuid,$pool', cookies=self.http_cookie)
        hosts: list[Host] = []
        for host in r.json():
            h = Host(host['hostname'], host['name_description'], host['name_label'], host['memory'], host['power_state'], host['residentVms'], host['rebootRequired'], host['tags'], host['uuid'], host['$pool'])
            hosts.append(h)
        return hosts

    def get_sr(self, uuid: str) -> StorageRepository:
        r = requests.get(f'{self.http_url}/srs/{uuid}', cookies=self.http_cookie)
        r = r.json()
        return StorageRepository(r['physical_usage'], r['name_description'], r['name_label'], r['size'], r['tags'], r['VDIs'], r['$pool'], r['uuid'])

    def get_srs(self) -> list[StorageRepository]:
        r = requests.get((f'{self.http_url}/srs?fields=physical_usage,name_description,name_label,size,tags,VDIs,$pool,uuid'), cookies=self.http_cookie)
        srs: list[StorageRepository] = []
        for sr in r.json():
            s = StorageRepository(sr['physical_usage'], sr['name_description'], sr['name_label'], sr['size'], sr['tags'], sr['VDIs'], sr['$pool'], sr['uuid'])
            srs.append(s)
        return srs
