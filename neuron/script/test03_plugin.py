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
        shutil.copy2("build/logs/neuron.log", "neu-ft/neuron/report/test03_node_neuron.log")
        os.remove("build/logs/neuron.log")

class TestPlugin:

    with open('neu-ft/neuron/data/test03_library_data.json') as f:
        test_data = json.load(f)

    def test01_add_plugin_fail0(self, setup_and_teardown_neuron):
        print("---given:incorrect configuration, when:add plugin, then:fail---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['library'] = test_data['library_c1']
        plugin_data['so_file'] = test_data['so_file_c1_err']
        plugin_data['schema_file'] = test_data['schema_file']

        response = add_plugin(test_data=plugin_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_LIBRARY_MODULE_INVALID == response.json().get("error")

    def test02_add_plugin_fail1(self, setup_and_teardown_neuron):
        print("---given:incorrect configuration, when:add plugin, then:fail---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['library'] = test_data['library_c1']
        plugin_data['so_file'] = ''
        plugin_data['schema_file'] = test_data['schema_file']

        response = add_plugin(test_data=plugin_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_BODY_IS_WRONG == response.json().get("error")

    def test03_add_plugin_fail2(self, setup_and_teardown_neuron):
        print("---given:incorrect configuration, when:add plugin, then:fail---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['library'] = test_data['library_c1']
        plugin_data['so_file'] = test_data['so_file_c1']
        plugin_data['schema_file'] = ''

        response = add_plugin(test_data=plugin_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_BODY_IS_WRONG == response.json().get("error")


    def test04_add_plugin_fail3(self, setup_and_teardown_neuron):
        print("---given:incorrect configuration, when:add plugin, then:fail---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['library'] = test_data['library_sc1']
        plugin_data['so_file'] = test_data['so_file_sc1']
        plugin_data['schema_file'] = test_data['schema_file']

        response = add_plugin(test_data=plugin_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_LIBRARY_MODULE_KIND_NOT_SUPPORT == response.json().get("error")

    def test05_add_plugin_success0(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:add plugin, then:success---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['library'] = test_data['library_c1']
        plugin_data['so_file'] = test_data['so_file_c1']
        plugin_data['schema_file'] = test_data['schema_file']

        response = add_plugin(test_data=plugin_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test06_add_plugin_success1(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:add plugin, then:success---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['library'] = test_data['library_s1']
        plugin_data['so_file'] = test_data['so_file_s1']
        plugin_data['schema_file'] = test_data['schema_file']

        response = add_plugin(test_data=plugin_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test04_add_plugin_fail4(self, setup_and_teardown_neuron):
        print("---given:incorrect configuration, when:add plugin, then:fail---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['library'] = test_data['library_c1']
        plugin_data['so_file'] = test_data['so_file_c1']
        plugin_data['schema_file'] = test_data['schema_file']

        response = add_plugin(test_data=plugin_data, header_data=config.headers)
        assert 409 == response.status_code
        assert NEU_ERR_LIBRARY_NAME_CONFLICT == response.json().get("error")

    
    def test07_update_plugin_fail0(self, setup_and_teardown_neuron):
        print("---given:incorrect configuration, when:update plugin, then:fail---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['library'] = test_data['library_c1']
        plugin_data['so_file'] = test_data['so_file_sc1']
        plugin_data['schema_file'] = test_data['schema_file']

        response = updata_plugin(test_data=plugin_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_LIBRARY_MODULE_NOT_EXISTS == response.json().get("error")
        
    def test08_update_plugin_fail1(self, setup_and_teardown_neuron):
        print("---given:incorrect configuration, when:update plugin, then:fail---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['library'] = '123'
        plugin_data['so_file'] = test_data['so_file_c1_2']
        plugin_data['schema_file'] = test_data['schema_file']

        response = updata_plugin(test_data=plugin_data, header_data=config.headers)
        assert 404 == response.status_code
        assert NEU_ERR_LIBRARY_NOT_FOUND == response.json().get("error")

    def test09_update_plugin_fail2(self, setup_and_teardown_neuron):
        print("---given:incorrect configuration, when:update plugin, then:fail---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['library'] = test_data['library_c1']
        plugin_data['so_file'] = test_data['so_file_c1_2']
        plugin_data['schema_file'] = ''

        response = updata_plugin(test_data=plugin_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_BODY_IS_WRONG == response.json().get("error")

    def test10_update_plugin_fail3(self, setup_and_teardown_neuron):
        print("---given:incorrect configuration, when:update plugin, then:fail---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['library'] = test_data['library_c1']
        plugin_data['so_file'] = ''
        plugin_data['schema_file'] = test_data['schema_file']

        response = updata_plugin(test_data=plugin_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_BODY_IS_WRONG == response.json().get("error")

    def test11_update_plugin_success0(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:update plugin, then:success---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['library'] = test_data['library_s1']
        plugin_data['so_file'] = test_data['so_file_s1_2']
        plugin_data['schema_file'] = test_data['schema_file']

        response = updata_plugin(test_data=plugin_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test12_add_node_success(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:add south node, then:success---")
        
        node_data = {}
        node_data['name'] = 'c1-a'
        node_data['plugin'] = 'c1'

        response = add_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")   


    def test13_configure_node_success(self, setup_and_teardown_neuron):
        print("---given:correct configuration and node not set, when:config node, then:success---")
        test_data = TestPlugin.test_data
        node_data = test_data['node_config']

        response = configure_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")


    def test14_update_plugin_success1(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:update plugin, then:success---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['library'] = test_data['library_c1']
        plugin_data['so_file'] = test_data['so_file_c1_2']
        plugin_data['schema_file'] = test_data['schema_file']

        response = updata_plugin(test_data=plugin_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

    def test15_del_plugin_fail0(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:del plugin, then:fail---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['plugin'] = 'c1'

        response = del_plugin(test_data=plugin_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_LIBRARY_IN_USE == response.json().get("error")

    def test16_del_plugin_fail0(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:del plugin, then:fail---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['plugin'] = 's1'

        response = del_plugin(test_data=plugin_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_LIBRARY_SYSTEM_NOT_ALLOW_DEL == response.json().get("error")

    def test17_del_node_success(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:del south node, then:success---")
        
        node_data = {}
        node_data['name'] = 'c1-a'

        response = delete_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error") 


    def test18_add_template_success(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:add template, then:success---")
        test_data = TestPlugin.test_data
        template_data = test_data['template_config']

        response = add_template(test_data=template_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")


    def test19_del_plugin_fail0(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:del plugin, then:fail---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['plugin'] = 'c1'

        response = del_plugin(test_data=plugin_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_LIBRARY_IN_USE == response.json().get("error")

    def test20_del_template_success(self, setup_and_teardown_neuron):
        print("---given:correct del template, when:del template, then:success---")
        test_data = TestPlugin.test_data

        response = del_template(name='c1 template', header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")


    def test21_del_plugin_sucess(self, setup_and_teardown_neuron):
        print("---given:correct configuration, when:del plugin, then:sucess---")
        test_data = TestPlugin.test_data
        plugin_data = {}
        plugin_data['plugin'] = 'c1'

        response = del_plugin(test_data=plugin_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")