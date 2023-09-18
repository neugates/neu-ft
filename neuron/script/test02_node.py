from api.api import *
import pytest
import os
import shutil
from pathlib import Path
import time
import json
import subprocess
import config
from data.error_codes import *
from data.codes import *

@pytest.fixture(autouse=True)
def setup_and_teardown_neuron():
    os.system("mkdir -p build/persistence")
    process_neuron = subprocess.Popen(['./neuron'], stderr=subprocess.PIPE, cwd='build/')
    time.sleep(1)
    assert process_neuron.poll() is None

    yield

    process_neuron.kill()
    time.sleep(1)
    _, err = process_neuron.communicate()
    assert process_neuron.poll() is not None, "Neuron process didn't stop"
    assert err.decode() == '', "stderr not empty: " + err.decode()

@pytest.fixture(scope="class", autouse=True)
def move_and_delete_logs():
    yield
    
    report_directory = "neu-ft/neuron/report"
    Path(report_directory).mkdir(exist_ok=True)
    if os.path.exists("build/logs/neuron.log"):
        shutil.copy2("build/logs/neuron.log", "neu-ft/neuron/report/test02_node_neuron.log")
        os.remove("build/logs/neuron.log")

class TestNode:

    with open('neu-ft/neuron/data/test02_node_data.json') as f:
        test_data = json.load(f)

    def test01_add_node_success(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:add south node, then:success---")
        test_data = TestNode.test_data
        node_data = test_data['node_data']

        response = add_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
    
    def test02_add_node_with_the_same_name_fail(self, setup_and_teardown_neuron):
        print("---given:same node name, when:add south node, then:add failed and return error---")
        test_data = TestNode.test_data
        node_data = test_data['node_data']

        response = add_node(test_data=node_data, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_EXIST == response.json().get("error")   

    def test03_add_node_with_plugin_not_existed_fail(self, setup_and_teardown_neuron):
        print("---given:plugin not existed, when:add south node, then:add failed and return error---")
        test_data = TestNode.test_data
        node_data = test_data['node_data_none']

        response = add_node(test_data=node_data, header_data=config.headers)
        assert 404 == response.status_code
        assert NEU_ERR_LIBRARY_NOT_FOUND == response.json().get("error")

    def test04_add_app_node_success(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:add app node, then:success---")
        test_data = TestNode.test_data
        node_data = test_data['node_data_app_old']

        response = add_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test05_update_app_node_success(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:update app node name, then:success---")
        test_data = TestNode.test_data
        node_data = test_data['node_data_app_new']

        response = update_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test06_update_node_success(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:update south node name, then:success---")
        test_data = TestNode.test_data
        node_data = test_data['update_to_modbus_tcp_node']

        response = update_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test07_update_node_name_to_empty_string_fail(self, setup_and_teardown_neuron):
        print("---given:new name is an empty string, when:update south node name, then:update failed and return error---")
        test_data = TestNode.test_data
        node_data = test_data['update_to_null']

        response = update_node(test_data=node_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_NODE_NAME_EMPTY == response.json().get("error")

    def test08_update_node_name_to_excessive_long_string_fail(self, setup_and_teardown_neuron):
        print("---given:new name is an excessive long string, when:update south node name, then:update failed and return error---")
        name = 'a'*200
        node_data = {
            "name": "modbus-tcp-node",
            "new_name": f"{name}"
        }
        response = update_node(test_data=node_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_NODE_NAME_TOO_LONG == response.json().get("error")

    def test09_update_node_name_nonexistent_fail(self, setup_and_teardown_neuron):
        print("---given:old name not existent, when:update south node name, then:update failed and return error---")
        test_data = TestNode.test_data
        node_data = test_data['update_modbus_tcp_node_nonexistent']

        response = update_node(test_data=node_data, header_data=config.headers)
        assert 404 == response.status_code
        assert NEU_ERR_NODE_NOT_EXIST == response.json().get("error")

    def test10_update_node_name_conflict_fail(self, setup_and_teardown_neuron):
        print("---given:new name is conflicting, when:update south node name, then:update failed and return error---")
        test_data = TestNode.test_data
        node_data = test_data['update_to_conflicting_name']

        response = update_node(test_data=node_data, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_EXIST == response.json().get("error")

    def test11_update_node_name_to_the_same_conflict_fail(self, setup_and_teardown_neuron):
        print("---given:new name is same with the old name, when:update node name, then:update failed and return error---")
        test_data = TestNode.test_data
        node_data_1 = test_data['south_same_name']

        response = update_node(test_data=node_data_1, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_EXIST == response.json().get("error")

        node_data_2 = test_data['south_same_name']

        response = update_node(test_data=node_data_2, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_EXIST == response.json().get("error")

    def test14_get_driver_node_success(self, setup_and_teardown_neuron):
        print("---given:correct request configuration, when:get driver node, then:success---")
        response = get_node(header_data=config.headers, type=NODE_DRIVER)
        assert 200 == response.status_code

    def test15_get_app_node_success(self, setup_and_teardown_neuron):
        print("---given:correct request configuration, when:get app node, then:success---")
        response = get_node(header_data=config.headers, type=NODE_APP)
        assert 200 == response.status_code

    def test16_get_unknown_type_node_fail(self, setup_and_teardown_neuron):
        print("---given:noncorrect request configuration with unknown node_type, when:get node, then:get failed and return error---")
        response = get_node(header_data=config.headers, type=3)
        assert 400 == response.status_code
        assert NEU_ERR_PARAM_IS_WRONG == response.json().get("error")

    def test17_get_node_setting_not_set_fail(self, setup_and_teardown_neuron):
        print("---given:node not set, when:get node setting, then:get failed and return error---")
        response = get_node_setting(header_data=config.headers, node_name="modbus-tcp-node")
        assert 200 == response.status_code
        assert NEU_ERR_NODE_SETTING_NOT_FOUND == response.json().get("error")
    
    def test18_start_node_not_set_fail(self, setup_and_teardown_neuron):
        print("---given:node not set, when:start node, then:start failed and return error---")
        test_data = TestNode.test_data
        node_data = test_data['start_node_not_set']

        response = ctl_node(test_data=node_data, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_NOT_READY == response.json().get("error")

    def test19_stop_node_not_set_fail(self, setup_and_teardown_neuron):
        print("---given:node not set, when:stop node, then:stop failed and return error---")
        test_data = TestNode.test_data
        node_data = test_data['stop_node_not_set']

        response = ctl_node(test_data=node_data, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_NOT_RUNNING == response.json().get("error")

    def test20_configure_node_success(self, setup_and_teardown_neuron):
        print("---given:correct configuration and node not set, when:config node, then:success---")
        test_data = TestNode.test_data
        node_data = test_data['node_config']

        response = configure_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test21_configure_node_non_existent_fail(self, setup_and_teardown_neuron):
        print("---given:node not exist, when:config node, then:config failed and return error---")
        test_data = TestNode.test_data
        node_data = test_data['non_node_config']

        response = configure_node(test_data=node_data, header_data=config.headers)
        assert 404 == response.status_code
        assert NEU_ERR_NODE_NOT_EXIST == response.json().get("error")

    def test22_get_non_existent_node_setting_fail(self, setup_and_teardown_neuron):
        print("---given:node not exist, when:get node setting, then:get failed and return error---")
        response = get_node_setting(header_data=config.headers, node_name="none")
        assert 404 == response.status_code
        assert NEU_ERR_NODE_NOT_EXIST == response.json().get("error")

    def test23_get_node_setting_success(self, setup_and_teardown_neuron):
        print("---given:node exist, when:get node setting, then:success with configuration back---")
        response = get_node_setting(header_data=config.headers, node_name="modbus-tcp-node")
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

    def test24_stop_node_success(self, setup_and_teardown_neuron):
        print("---given:node is running, when:stop node, then:success---")
        test_data = TestNode.test_data
        node_data = test_data['node_stop']

        response = ctl_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test25_stop_stopped_node_fail(self, setup_and_teardown_neuron):
        print("---given:node is stopped, when:stop node, then:return error---")
        test_data = TestNode.test_data
        node_data = test_data['node_stop']

        response = ctl_node(test_data=node_data, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_IS_STOPED == response.json().get("error")
    
    def test26_start_node_success(self, setup_and_teardown_neuron):
        print("---given:node is stopped, when:start node, then:success---")
        test_data = TestNode.test_data
        node_data = test_data['node_start']

        response = ctl_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test27_start_running_node_fail(self, setup_and_teardown_neuron):
        print("---given:node is running, when:start node, then:return error---")
        test_data = TestNode.test_data
        node_data = test_data['node_start']

        response = ctl_node(test_data=node_data, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_NODE_IS_RUNNING == response.json().get("error")

    def test28_get_node_state_success(self, setup_and_teardown_neuron):
        print("---given:node is running&disconnected, when:get node state, then:success---")
        response = get_node_state(header_data=config.headers, node_name= "modbus-tcp-node")
        assert 200 == response.status_code
        assert NODE_STATE_RUNNING == response.json().get("running")
        assert NODE_LINK_STATE_DISCONNECTED == response.json().get("link")
    
    def test29_node_status_not_change_after_configuration_success(self, setup_and_teardown_neuron):
        print("---given:node, when:check node status whether change after configing, then:not changed")
        test_data = TestNode.test_data
        node_config = test_data['node_config']

        configure_node(test_data=node_config, header_data=config.headers)

        response = get_node_state(header_data=config.headers, node_name= "modbus-tcp-node")
        assert 200 == response.status_code
        assert NODE_STATE_RUNNING == response.json().get("running")
        assert NODE_LINK_STATE_DISCONNECTED == response.json().get("link")

        stop_node = test_data['node_stop']

        ctl_node(test_data=stop_node, header_data=config.headers)

        configure_node(test_data=node_config, header_data=config.headers)

        response = get_node_state(header_data=config.headers, node_name= "modbus-tcp-node")
        assert NODE_STATE_STOP == response.json().get("running")
        assert NODE_LINK_STATE_DISCONNECTED == response.json().get("link")


    def test30_delete_node_success(self, setup_and_teardown_neuron):
        print("---given:south node, when:delete south node, then:success")
        test_data = TestNode.test_data
        node_data = test_data['delete_modbus_tcp_node']

        response = delete_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test31_delete_app_node_success(self, setup_and_teardown_neuron):
        print("---given:app node, when:delete app node, then:success")
        test_data = TestNode.test_data
        node_data = test_data['delete_mqtt_node']

        response = delete_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
    
    def test32_delete_node_nonexistent_fail(self, setup_and_teardown_neuron):
        print("---given:node not exist, when:delete the node, then:return error")
        test_data = TestNode.test_data
        node_data = test_data['delete_null_node']

        response = delete_node(test_data=node_data, header_data=config.headers)
        assert 404 == response.status_code
        assert NEU_ERR_NODE_NOT_EXIST == response.json().get("error")