
import sys
import os
import json
import base64

import requests

from utils import general
from utils import dbase_handler
from utils import config_handler

def get_all_user(term_id):

    terminal_details = dbase_handler.get_terminal_details(term_id)
    ip_addr = terminal_details[2]

    url = 'http://' + ip_addr + '/action/SearchPersonList'
    headers =   {
                    'Content-Type': "application/json",
                    'Accept': "*/*",
                    'Cache-Control': "no-cache",
                    'Host': ip_addr,
                    'Accept-Encoding': "gzip, deflate",
                    'Content-Length': "",
                    'Connection': "keep-alive",
                    'cache-control': "no-cache"
                }

    body =      {
                    "operator": "SearchPersonList",
                    "info":{
                        "DeviceID":int(term_id),
                        "PersonType":2,
                        "BeginTime":"",
                        "EndTime":"",
                        "Name":"",
                        "RequestCount":500
                    }
                }

    response = requests.request("POST",url, headers=headers, auth=requests.auth.HTTPBasicAuth("admin", "admin"), json=body)
    json_data = json.loads(response.text)
    return json_data

def get_device_param(ip_addr, username, password):

    url = 'http://' + ip_addr + '/action/GetSysParam'

    response = requests.request("POST",url, auth=requests.auth.HTTPBasicAuth(username, password))    

    json_data = json.loads(response.text)    

    return str(json_data["info"]["DeviceID"])

def set_device_subscribe(device_id, ip_addr, username, password):

    url = 'http://' + ip_addr + '/action/Subscribe'
    server_ip = 'http://' + config_handler.get_server_ip() + ':' + config_handler.get_server_port()
    print(server_ip)
    body =  {
                "operator": "Subscribe",
                "info": {
                    "DeviceID": int(device_id),
                    "Num": 2,
                    "Topics":["Snap", "VerifyWithSnap"],
                    "SubscribeAddr":server_ip,
                    "SubscribeUrl":{"Snap":"/Subscribe/Snap", "Verify":"/Subscribe/Verify", "HeartBeat":"/Subscribe/heartbeat"},
                    "Auth":"Basic",
                    "User": "admin",
                    "Pwd": "admin",
                    "BeatInterval":5
                    }
            }

    response = requests.request("POST", url, auth=requests.auth.HTTPBasicAuth(username, password), json=body)
    json_data = json.loads(response.text)
    print(json_data)

def register_user(device_id, user_id, blacklist, name, img_name):

    terminal_details = dbase_handler.get_terminal_details(device_id)
    ip_addr = terminal_details[2]

    with open(os.getcwd()+"\\static\\snapshot\\" + img_name, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    picjson = "data:image/jpeg;base64,"+encoded_string.decode("utf-8")

    url = 'http://' + ip_addr + '/action/AddPerson'

    body =  {
                "operator": "AddPerson",
                "info": {
                    "DeviceID":int(device_id),
                    "IdType":2,
                    "PersonType": blacklist,
                    "Name":name,
                    "PersonUUID":user_id,
                    "Native": "",
                    "Tempvalid": 0
                    },
                    "picinfo": picjson
            }

    response = requests.request("POST",url, auth=requests.auth.HTTPBasicAuth("admin", "admin"), json=body)
    json_data = json.loads(response.text)
    print(json_data)

def edit_user(device_id, user_id, blacklist):
    terminal_details = dbase_handler.get_terminal_details(device_id)
    ip_addr = terminal_details[2]

    url = 'http://' + ip_addr + '/action/EditPerson'

    body =  {
                
                "operator": "EditPerson",
                "info": {
                            "DeviceID":int(device_id),
                            "IdType":2,
                            "PersonUUID": user_id,
                            "PersonType": blacklist
                        }
            }

    response = requests.request("POST",url, auth=requests.auth.HTTPBasicAuth("admin", "admin"), json=body)
    json_data = json.loads(response.text)
    print(json_data)

def sync(term_id):
    ...

def reset_device_subscription(term_id):

    terminal_details = dbase_handler.get_terminal_details(term_id)
    ip_addr = terminal_details[2]

    url = 'http://' + ip_addr + '/action/Subscribe'
    server_ip = 'http://' + '0.0.0.0' + ':8080'
    print(server_ip)
    body =  {
                "operator": "Subscribe",
                "info": {
                    "DeviceID": int(term_id),
                    "Num": 2,
                    "Topics":["Snap", "VerifyWithSnap"],
                    "SubscribeAddr":server_ip,
                    "SubscribeUrl":{"Snap":"/Subscribe/Snap", "Verify":"/Subscribe/Verify", "HeartBeat":"/Subscribe/heartbeat"},
                    "Auth":"Basic",
                    "User": "admin",
                    "Pwd": "admin",
                    "BeatInterval":5
                    }
            }

    response = requests.request("POST", url, auth=requests.auth.HTTPBasicAuth('admin', 'admin'), json=body)
    json_data = json.loads(response.text)
    print(json_data)

def reset_device_list(term_id):

    terminal_details = dbase_handler.get_terminal_details(term_id)
    ip_addr = terminal_details[2]

    url = 'http://' + ip_addr + '/action/SetFactoryDefault'
    
    body =  {   "operator": "SetFactoryDefault",
                "info": {
                "DefaltDoorSet": 0,
                "DefaltSoundSet": 0,
                "DefaltNetPar": 0,
                "DefaltCenterPar": 0,
                "DefaltCapture": 0,
                "DefaltLog": 0,
                "DefaltPerson": 1,
                "DefaltRecord": 0,
                "DefaltMaintainTime": 0,
                "DefaltSystemSettings": 0,
                "DefaltEnterIPC": 0,
                "DefaltServerBasicPara": 0,
                "DefaltWorktype": 0
                }
            }

    response = requests.request("POST", url, auth=requests.auth.HTTPBasicAuth('admin', 'admin'), json=body)
    json_data = json.loads(response.text)
    print(json_data)

def delete_user(device_id, user_id):

    terminal_details = dbase_handler.get_terminal_details(device_id)
    ip_addr = terminal_details[2]

    url = 'http://' + ip_addr + '/action/DeletePerson'

    body =  {
                "operator": "DeletePerson",
                "info": {
                    "DeviceID":int(device_id),
                    "TotalNum":1,
                    "IdType":2,
                    "PersonUUID":[str(user_id)]
                    }
            }

    response = requests.request("POST",url, auth=requests.auth.HTTPBasicAuth("admin", "admin"), json=body)
    json_data = json.loads(response.text)
    print(json_data)