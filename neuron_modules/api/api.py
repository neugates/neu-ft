import requests
from config import BASE_URL

url_login = BASE_URL + f"/api/v2/login"
url_password = BASE_URL + f"/api/v2/password"

url_license = BASE_URL + f"/api/v2/license"

url_node = BASE_URL + f"/api/v2/node"
url_node_setting = BASE_URL + f"/api/v2/node/setting"
url_node_ctl = BASE_URL + f"/api/v2/node/ctl"
url_node_state = BASE_URL + f"/api/v2/node/state"

url_group = BASE_URL + f"/api/v2/group"

url_tag = BASE_URL + f"/api/v2/tags"

url_read = BASE_URL + f"/api/v2/read"
url_write = BASE_URL + f"/api/v2/write"

def login(test_data):
    return requests.post(url=url_login, json=test_data)
def change_password(test_data, header_data):
    return requests.post(url=url_password, json=test_data, headers= header_data)

def upload_license(test_data, header_data):
    return requests.post(url=url_license, json=test_data, headers= header_data)
def get_license(header_data):
    return requests.get(url=url_license, headers= header_data)

def add_node(test_data, header_data):
    return requests.post(url=url_node, json=test_data, headers= header_data) 
def update_node(test_data, header_data):
    return requests.put(url=url_node, json=test_data, headers= header_data)
def get_node(header_data, type):
    return requests.get(url=url_node + f"?type={type}", headers= header_data)
def configure_node(test_data, header_data):
    return requests.post(url=url_node_setting, json=test_data, headers= header_data)
def get_node_setting(header_data, node_name):
    return requests.get(url=url_node_setting + f"?node={node_name}", headers= header_data)
def ctl_node(test_data, header_data):
    return requests.post(url=url_node_ctl, json=test_data, headers= header_data)
def get_node_state(header_data, node_name):
    return requests.get(url=url_node_state + f"?node={node_name}", headers= header_data)
def delete_node(test_data, header_data):
    return requests.delete(url=url_node, json=test_data, headers= header_data)

def add_group(test_data, header_data):
    return requests.post(url=url_group, json=test_data, headers= header_data)
def delete_group(test_data, header_data):
    return requests.delete(url=url_group, json=test_data, headers= header_data)
def update_group(test_data, header_data):
    return requests.put(url=url_group, json=test_data, headers= header_data)
def get_group(header_data):
    return requests.get(url=url_group, headers= header_data)

def add_tag(test_data, header_data):
    return requests.post(url=url_tag, json=test_data, headers= header_data)
def delete_tag(test_data, header_data):
    return requests.delete(url=url_tag, json=test_data, headers= header_data)
def update_tag(test_data, header_data):
    return requests.put(url=url_tag, json=test_data, headers= header_data)
def get_tag(header_data, node_name, group_name):
    return requests.get(url=url_tag + f"?node={node_name}&group={group_name}", headers= header_data)

def read(test_data, header_data):
    return requests.post(url=url_read, json=test_data, headers= header_data)
def write(test_data, header_data):
    return requests.post(url=url_write, json=test_data, headers= header_data)