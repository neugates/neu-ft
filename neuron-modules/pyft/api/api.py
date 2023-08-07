import requests

class LoginAPI:
    def __init__(self):
        self.url_login = "http://127.0.0.1:7000/api/v2/login"
        self.url_password = "http://127.0.0.1:7000/api/v2/password"

    def login(self, test_data):
        return requests.post(url=self.url_login, json=test_data)
    
    def change_password(self, test_data, header_data):
        return requests.post(url=self.url_password, json=test_data, headers= header_data)

class LicenseAPI:
    def __init__(self):
        self.url_license = "http://127.0.0.1:7000/api/v2/license"

    def upload_license(self, test_data, header_data):
        return requests.post(url=self.url_license, json=test_data, headers= header_data)
    
    def get_license(self, header_data):
        return requests.get(url=self.url_license, headers= header_data)

class NodeAPI:
    def __init__(self):
        self.url_node = "http://127.0.0.1:7000/api/v2/node"
        self.url_node_setting = "http://127.0.0.1:7000/api/v2/node/setting"
        self.url_node_ctl = "http://127.0.0.1:7000/api/v2/node/ctl"
        self.url_node_state = "http://127.0.0.1:7000/api/v2/node/state"

    def add_node(self, test_data, header_data):
        return requests.post(url=self.url_node, json=test_data, headers= header_data)
    
    def update_node(self, test_data, header_data):
        return requests.put(url=self.url_node, json=test_data, headers= header_data)

    def get_node(self, header_data, type):
        return requests.get(url=self.url_node + f"?type={type}", headers= header_data)

    def configure_node(self, test_data, header_data):
        return requests.post(url=self.url_node_setting, json=test_data, headers= header_data)

    def get_node_setting(self, header_data, node_name):
        return requests.get(url=self.url_node_setting + f"?node={node_name}", headers= header_data)

    def ctl_node(self, test_data, header_data):
        return requests.post(url=self.url_node_ctl, json=test_data, headers= header_data)

    def get_node_state(self, header_data, node_name):
        return requests.get(url=self.url_node_state + f"?node={node_name}", headers= header_data)

    def delete_node(self, test_data, header_data):
        return requests.delete(url=self.url_node, json=test_data, headers= header_data)

class GroupAPI:
    def __init__(self):
        self.url_group = "http://127.0.0.1:7000/api/v2/group"

    def add_group(self, test_data, header_data):
        return requests.post(url=self.url_group, json=test_data, headers= header_data)

    def delete_group(self, test_data, header_data):
        return requests.delete(url=self.url_group, json=test_data, headers= header_data)

    def update_group(self, test_data, header_data):
        return requests.put(url=self.url_group, json=test_data, headers= header_data)

    def get_group(self, header_data):
        return requests.get(url=self.url_group, headers= header_data)

class TagAPI:
    def __init__(self):
        self.url_tag = "http://127.0.0.1:7000/api/v2/tags"

    def add_tag(self, test_data, header_data):
        return requests.post(url=self.url_tag, json=test_data, headers= header_data)

    def delete_tag(self, test_data, header_data):
        return requests.delete(url=self.url_tag, json=test_data, headers= header_data)

    def update_tag(self, test_data, header_data):
        return requests.put(url=self.url_tag, json=test_data, headers= header_data)

    def get_tag(self, header_data, node_name, group_name):
        return requests.get(url=self.url_tag + f"?node={node_name}&group={group_name}", headers= header_data)

class RWAPI:
    def __init__(self):
        self.url_read = "http://127.0.0.1:7000/api/v2/read"
        self.url_write = "http://127.0.0.1:7000/api/v2/write"

    def read(self, test_data, header_data):
        return requests.post(url=self.url_read, json=test_data, headers= header_data)

    def write(self, test_data, header_data):
        return requests.post(url=self.url_write, json=test_data, headers= header_data)