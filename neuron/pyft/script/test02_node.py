from api.api import LoginAPI
from api.api import NodeAPI
import pytest
import os
import time
import subprocess
import config
from data.error_codes import *
from data.codes import *
from config import NEURON_PATH

class TestNode:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        
        self.login_api = LoginAPI()
        self.node_api = NodeAPI()

        start_dir = os.getcwd()
        os.chdir(NEURON_PATH)
        neuron_path = "./neuron"
        args_neuron = ["--log"]
        command_neuron = [neuron_path] + args_neuron
        process_neuron = subprocess.Popen(command_neuron)
        time.sleep(1)
        os.chdir(start_dir)
        assert process_neuron.poll() is None

        yield
        
        os.chdir(NEURON_PATH)
        process_neuron.kill()
        time.sleep(1)
        assert process_neuron.poll() is not None
        os.chdir(start_dir)

    def test01_add_node_success(self):
        node_data = {
            "name": "modbus-node",
            "plugin": "Modbus TCP"
        }
        response = self.node_api.add_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
    
    def test02_add_node_with_the_same_name_fail(self):
        node_data = {
            "name": "modbus-node",
            "plugin": "Modbus TCP"
        }
        response = self.node_api.add_node(test_data=node_data, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_EXIST == response.json().get("error")   

    def test03_add_node_with_plugin_not_existed_fail(self):
        node_data = {
            "name": "modbus-node-not-exist",
            "plugin": "Modbus"
        }
        response = self.node_api.add_node(test_data=node_data, header_data=config.headers)
        assert 404 == response.status_code
        assert NEU_ERR_LIBRARY_NOT_FOUND == response.json().get("error")

    def test04_add_app_node_success(self):
        node_data = {
            "name": "mqtt-node-old",
            "plugin": "MQTT"
        }
        response = self.node_api.add_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test05_update_app_node_success(self):
        node_data = {
            "name": "mqtt-node-old",
            "new_name": "mqtt-node"
        }
        response = self.node_api.update_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test06_update_node_success(self):
        node_data = {
            "name": "modbus-node",
            "new_name": "modbus-tcp-node"
        }
        response = self.node_api.update_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test07_update_node_name_to_empty_string_fail(self):
        node_data = {
            "name": "modbus-tcp-node",
            "new_name": ""
        }
        response = self.node_api.update_node(test_data=node_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_NODE_NAME_EMPTY == response.json().get("error")

    def test08_update_node_name_to_excessive_long_string_fail(self):
        name = 'a'*200
        node_data = {
            "name": "modbus-tcp-node",
            "new_name": f"{name}"
        }
        response = self.node_api.update_node(test_data=node_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_NODE_NAME_TOO_LONG == response.json().get("error")

    def test09_update_node_name_nonexistent_fail(self):
        node_data = {
            "name": "modbus-tcp-node_nonexistent",
            "new_name": "modbus"
        }
        response = self.node_api.update_node(test_data=node_data, header_data=config.headers)
        assert 404 == response.status_code
        assert NEU_ERR_NODE_NOT_EXIST == response.json().get("error")

    def test10_update_node_name_conflict_fail(self):
        node_data = {
            "name": "modbus-tcp-node",
            "new_name": "mqtt-node"
        }
        response = self.node_api.update_node(test_data=node_data, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_EXIST == response.json().get("error")

    def test11_update_node_name_to_the_same_conflict_fail(self):
        node_data_1 = {
            "name": "modbus-tcp-node",
            "new_name": "modbus-tcp-node"
        }
        response = self.node_api.update_node(test_data=node_data_1, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_EXIST == response.json().get("error")

        node_data_2 = {
            "name": "mqtt-node",
            "new_name": "mqtt-node"
        }
        response = self.node_api.update_node(test_data=node_data_2, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_EXIST == response.json().get("error")

    def test12_update_monitor_node_fail(self):
        node_data = {
            "name": "monitor",
            "new_name": "monitor-new"
        }
        response = self.node_api.update_node(test_data=node_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_NODE_NOT_ALLOW_UPDATE == response.json().get("error")

    def test13_update_node_name_to_monitor_fail(self):
        node_data = {
            "name": "modbus-tcp-node",
            "new_name": "monitor"
        }
        response = self.node_api.update_node(test_data=node_data, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_EXIST == response.json().get("error")

    def test14_get_driver_node_success(self):
        response = self.node_api.get_node(header_data=config.headers, type=NODE_DRIVER)
        assert 200 == response.status_code
        print(response.json())

    def test15_get_app_node_success(self):
        response = self.node_api.get_node(header_data=config.headers, type=NODE_APP)
        assert 200 == response.status_code
        print(response.json())

    def test16_get_unknown_type_node_fail(self):
        response = self.node_api.get_node(header_data=config.headers, type=3)
        assert 400 == response.status_code
        assert NEU_ERR_PARAM_IS_WRONG == response.json().get("error")

    def test17_get_node_setting_not_set_fail(self):
        response = self.node_api.get_node_setting(header_data=config.headers, node_name="modbus-tcp-node")
        assert 200 == response.status_code
        assert NEU_ERR_NODE_SETTING_NOT_FOUND == response.json().get("error")
    
    def test18_start_node_not_set_fail(self):
        node_data = {
            "node": "modbus-tcp-node",
            "cmd": 0
        }
        response = self.node_api.ctl_node(test_data=node_data, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_NOT_READY == response.json().get("error")

    def test19_stop_node_not_set_fail(self):
        node_data = {
            "node": "modbus-tcp-node",
            "cmd": 1
        }
        response = self.node_api.ctl_node(test_data=node_data, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_NOT_RUNNING == response.json().get("error")

    def test20_configure_node_success(self):
        node_data = {
            "node": "modbus-tcp-node",
            "params": {
                "transport_mode": 0,
                "connection_mode": 0,
                "max_retries": 0,
                "retry_interval": 0, 
                "interval": 20,
                "host": "127.0.0.1",
                "port": 502,
                "timeout": 3000
            }
        }
        response = self.node_api.configure_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test21_configure_node_non_existent_fail(self):
        node_data = {
            "node": "none",
            "params": {
                "transport_mode": 0,
                "connection_mode": 0,
                "max_retries": 0,
                "retry_interval": 0, 
                "interval": 20,
                "host": "127.0.0.1",
                "port": 502,
                "timeout": 3000
            }
        }
        response = self.node_api.configure_node(test_data=node_data, header_data=config.headers)
        assert 404 == response.status_code
        assert NEU_ERR_NODE_NOT_EXIST == response.json().get("error")

    def test22_get_non_existent_node_setting_fail(self):
        response = self.node_api.get_node_setting(header_data=config.headers, node_name="none")
        assert 404 == response.status_code
        assert NEU_ERR_NODE_NOT_EXIST == response.json().get("error")

    def test23_get_node_setting_success(self):
        response = self.node_api.get_node_setting(header_data=config.headers, node_name="modbus-tcp-node")
        assert 200 == response.status_code
        assert "modbus-tcp-node" == response.json().get("node")
        assert 0 == response.json().get("params").get("transport_mode")
        assert 0 == response.json().get("params").get("connection_mode")
        assert 0 == response.json().get("params").get("max_retries")
        assert 0 == response.json().get("params").get("retry_interval")
        assert 20 == response.json().get("params").get("interval")
        assert 502 == response.json().get("params").get("port")
        assert 3000 == response.json().get("params").get("timeout")
        assert "127.0.0.1" == response.json().get("params").get("host")

    def test24_stop_node_success(self):
        node_data = {
            "node": "modbus-tcp-node",
            "cmd": 1
        }
        response = self.node_api.ctl_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test25_stop_stopped_node_fail(self):
        node_data = {
            "node": "modbus-tcp-node",
            "cmd": 1
        }
        response = self.node_api.ctl_node(test_data=node_data, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_IS_STOPED == response.json().get("error")
    
    def test26_start_node_success(self):
        node_data = {
            "node": "modbus-tcp-node",
            "cmd": 0
        }
        response = self.node_api.ctl_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test27_start_running_node_fail(self):
        node_data = {
            "node": "modbus-tcp-node",
            "cmd": 0
        }
        response = self.node_api.ctl_node(test_data=node_data, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_IS_RUNNING == response.json().get("error")

    def test28_get_node_state_success(self):
        response = self.node_api.get_node_state(header_data=config.headers, node_name= "modbus-tcp-node")
        assert 200 == response.status_code
        assert NODE_STATE_RUNNING == response.json().get("running")
        assert NODE_LINK_STATE_DISCONNECTED == response.json().get("link")
    
    def test29_node_status_not_change_after_configuration_success(self):
        node_config = {
            "node": "modbus-tcp-node",
            "params": {
                "transport_mode": 0,
                "connection_mode": 0,
                "max_retries": 0,
                "retry_interval": 0, 
                "interval": 20,
                "host": "127.0.0.1",
                "port": 502,
                "timeout": 3000
            }
        }
        self.node_api.configure_node(test_data=node_config, header_data=config.headers)

        response = self.node_api.get_node_state(header_data=config.headers, node_name= "modbus-tcp-node")
        assert 200 == response.status_code
        assert NODE_STATE_RUNNING == response.json().get("running")
        assert NODE_LINK_STATE_DISCONNECTED == response.json().get("link")

        stop_node = {
            "node": "modbus-tcp-node",
            "cmd": 1
        }
        self.node_api.ctl_node(test_data=stop_node, header_data=config.headers)

        self.node_api.configure_node(test_data=node_config, header_data=config.headers)

        response = self.node_api.get_node_state(header_data=config.headers, node_name= "modbus-tcp-node")
        assert NODE_STATE_STOP == response.json().get("running")
        assert NODE_LINK_STATE_DISCONNECTED == response.json().get("link")


    def test30_delete_node_success(self):
        node_data = {
            "name": "modbus-tcp-node"
        }
        response = self.node_api.delete_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test31_delete_app_node_success(self):
        node_data = {
            "name": "mqtt-node"
        }
        response = self.node_api.delete_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
    
    def test32_delete_node_nonexistent_fail(self):
        node_data = {
            "name": "not-exist"
        }
        response = self.node_api.delete_node(test_data=node_data, header_data=config.headers)
        assert 404 == response.status_code
        assert NEU_ERR_NODE_NOT_EXIST == response.json().get("error")