import pytest
import config
import subprocess
import os
import shutil
from pathlib import Path
from api.api import *
from data.error_codes import *
from common.common import *
import time
import json
import random

@pytest.fixture()
def setup_and_teardown_neuron(autouse=True):

    process_neuron = subprocess.Popen(['./neuron'], stderr=subprocess.PIPE, cwd='build/')
    time.sleep(1)
    assert process_neuron.poll() is None

    yield

    process_neuron.kill()
    time.sleep(1)
    _, err = process_neuron.communicate()
    assert process_neuron.poll() is not None, "Neuron process didn't stop"
    assert err.decode() == '', "stderr not empty: " + err.decode()
    os.remove("build/persistence/sqlite.db")

@pytest.fixture()
def random_port():
    while True:
        port = random.randint(1025, 60000)
        if port != 7000:
            return port

@pytest.fixture()
def setup_and_teardown_modbus(random_port):

    process_modbus = subprocess.Popen(['./modbus_simulator', 'tcp', str(random_port)], stderr=subprocess.PIPE, cwd='build/simulator')
    time.sleep(1)
    assert process_modbus.poll() is None

    yield
    
    process_modbus.kill()
    time.sleep(1)
    assert process_modbus.poll() is not None

@pytest.fixture(scope="session", autouse=True)
def move_and_delete_logs():
    yield
    
    report_directory = "report"
    Path(report_directory).mkdir(exist_ok=True)
    if os.path.exists("build/logs/neuron.log"):
        shutil.copy2("build/logs/neuron.log", "neu-ft/neuron_modules/report/test02_license_neuron.log")
        shutil.copy2("build/logs/modbus-tcp-node.log", "neu-ft/neuron_modules/report/test02_license_modbus_tcp_node.log")
        os.remove("build/logs/neuron.log")

class TestLicense:

    with open('neu-ft/neuron_modules/data/test02_license_data.json') as f:
        test_data = json.load(f)

    def add_tags_less_than_30(self, random_port):
        test_data = TestLicense.test_data
        node_data = test_data['node_data']
        group_data = test_data['group_data']
        tag_config = test_data['tag_config']
        tag_write_data = test_data['tag_write_data']
        tag_read_data = test_data['tag_read_data']
        node_config = {
            "node": "modbus-node",
            "params": {
                "transport_mode": 0,
                "connection_mode": 0,
                "max_retries": 0,
                "retry_interval": 0, 
                "interval": 20,
                "host": "127.0.0.1",
                "port": random_port,
                "timeout": 3000
            }
        }
    
        response = add_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
    
        response = configure_node(test_data=node_config, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
    
        response = add_group(test_data=group_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = add_tag(test_data=tag_config, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = write(test_data=tag_write_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(2)

        response = read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert 666 == response.json()["tags"][0].get("value")

    def add_tags_more_than_30(self, random_port):
        test_data = TestLicense.test_data
        node_data = test_data['node_data']
        group_data = test_data['group_data']
        tag_config_31 = test_data['tag_config_31']
        tag_write_data = test_data['tag_write_data']
        tag_read_data = test_data['tag_read_data']
        node_config = {
            "node": "modbus-node",
            "params": {
                "transport_mode": 0,
                "connection_mode": 0,
                "max_retries": 0,
                "retry_interval": 0, 
                "interval": 20,
                "host": "127.0.0.1",
                "port": random_port,
                "timeout": 3000
            }
        }
    
        response = add_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
    
        response = configure_node(test_data=node_config, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
    
        response = add_group(test_data=group_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = add_tag(test_data=tag_config_31, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = write(test_data=tag_write_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_LICENSE_INVALID == response.json().get("error")

        time.sleep(2)

        response = read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_LICENSE_INVALID == response.json()['tags'][0].get("error")

    def test01_get_license_without_license_fail(self, setup_and_teardown_neuron):
        print("---given:without license, when:get license, then:get failed and return error---")
        try:
            os.remove("build/config/neuron-default.lic")
        except FileNotFoundError:
            pass
        try:
            os.remove("build/persistence/neuron.lic")
        except FileNotFoundError:
            pass
        response = get_license(header_data=config.headers)
        assert 404 == response.status_code
        assert NEU_ERR_LICENSE_NOT_FOUND == response.json().get("error")

    def test02_upload_invalid_license_fail(self, setup_and_teardown_neuron):
        print("---given:without license, when:upload invalid license, then:upload failed and return error---")
        license_data_invalid = {
            "license": "-----BEGIN CERTIFICATE-----\nWRONGTCCAtWgAwIBAgIDOFVFMA0GCSqGSIb3DQEBCwUAMIGDMQswCQYDVQQGEwJD\nTjERMA8GA1UECAwIWmhlamlhbmcxETAPBgNVBAcMCEhhbmd6aG91MQwwCgYDVQQK\nDANFTVExDDAKBgNVBAsMA0VNUTESMBAGA1UEAwwJKi5lbXF4LmlvMR4wHAYJKoZI\nhvcNAQkBFg96aGFuZ3doQGVtcXguaW8wIBcNMjMwNzI2MDk1MjA2WhgPMjA5OTEy\nMzEwOTUyMDZaMH8xCzAJBgNVBAYTAkNOMScwJQYDVQQKDB7mna3lt57mmKDkupHn\np5HmioDmnInpmZDlhazlj7gxJzAlBgNVBAMMHuadreW3nuaYoOS6keenkeaKgOac\niemZkOWFrOWPuDEeMBwGCSqGSIb3DQEJARYPc3VwcG9ydEBlbXF4LmlvMIIBIjAN\nBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmTlAPpfFDEL7a92u/4Zd6owJXRPj\n5bpx6wNnnRz8nkwqnj8Eol/JStwOjuDsz/DG+lRWN0rfXsYdqGLfGMzCHJYEnWuB\nylrGPTxHspiS3crcxLhHL4Fex5mEPzvqpiOlyznn1k2sVxfOCANLYSUBTQpXyDVh\nrLCWWMnRqgHY5EZ8SeLWSmf+vMaRdY43ppYuCEIzJuBW90gQxbJJhyUSswP8ujUe\nqoArhKemXgNcaO9xOC8uHOpFsaCjiLubO30Jer4Lw6u3GvgW7PEnXQj4Z6WxPHOz\n3dCvdCSxxTyvMGSYsaLG8XFm4MuKaHiqgNB5KkmI3HmGADkvGNSlpn+BJwIDAQAB\no2swaTAUBgkrBgEEAYOaHQoEBwwFdHJpYWwwEQYJKwYBBAGDmh0EBAQMAi0xMBEG\nCSsGAQQBg5odCwQEDAIzMDARBgkrBgEEAYOaHQwEBAwCMzAwGAYJKwYBBAGDmh0N\nBAsMCTBYQkZGRUZGRjANBgkqhkiG9w0BAQsFAAOCAQEAapRj44Cv0jNMRovRc0av\nPZb/Q14fki+Gi0Wi0315N51w1eCyNDUASE/7XLW1rRoaCMTmlshl9pF4FWhcLmq2\nq0/1A/9AxYPaW4evN8x9LjZpHTfj7KoQkHzogJdOSY5ib93IwVwrymDjvvpKZtZZ\n7NLC9AXiQQ5t2Z9SDfVX1d+xfhVzAq5D/XYVieqjO9EaYAT9Ad/7NUckCE9Bgiwi\nnM+/EDq95k3XokQc3+K8FcHzFaFTS6InqUzrE3R2USsXen3KoHs/U9kTWmhOjyyw\neJIcDwpfk9lCAUOFV5a2Lj99P+UhuHnoraJ+RN3RID3kG6gR+jSvgF60UlBTRZM+\njg==\n-----END CERTIFICATE-----"
        }
        response = upload_license(test_data=license_data_invalid, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_LICENSE_INVALID == response.json().get("error")

    def test03_tag_less_than_30_without_license_success(self, setup_and_teardown_neuron, setup_and_teardown_modbus, random_port):
        print("---given:without license, when:add 2 tags and write&read, then:success---")
        self.add_tags_less_than_30(random_port)

    def test04_tag_more_than_30_without_license_fail(self, setup_and_teardown_neuron, setup_and_teardown_modbus, random_port):
        print("---given:without license, when:add 31 tags and write&read, then:failed and return error---")
        self.add_tags_more_than_30(random_port)

    def test05_upload_outdated_license_fail(self, setup_and_teardown_neuron):
        print("---given:without license, when:upload outdated license, then:upload failed and return error---")
        license_data_invalid = {
            "license": "-----BEGIN CERTIFICATE-----\nWRONGTCCAtWgAwIBAgIDOFVFMA0GCSqGSIb3DQEBCwUAMIGDMQswCQYDVQQGEwJD\nTjERMA8GA1UECAwIWmhlamlhbmcxETAPBgNVBAcMCEhhbmd6aG91MQwwCgYDVQQK\nDANFTVExDDAKBgNVBAsMA0VNUTESMBAGA1UEAwwJKi5lbXF4LmlvMR4wHAYJKoZI\nhvcNAQkBFg96aGFuZ3doQGVtcXguaW8wIBcNMjMwNzI2MDk1MjA2WhgPMjA5OTEy\nMzEwOTUyMDZaMH8xCzAJBgNVBAYTAkNOMScwJQYDVQQKDB7mna3lt57mmKDkupHn\np5HmioDmnInpmZDlhazlj7gxJzAlBgNVBAMMHuadreW3nuaYoOS6keenkeaKgOac\niemZkOWFrOWPuDEeMBwGCSqGSIb3DQEJARYPc3VwcG9ydEBlbXF4LmlvMIIBIjAN\nBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmTlAPpfFDEL7a92u/4Zd6owJXRPj\n5bpx6wNnnRz8nkwqnj8Eol/JStwOjuDsz/DG+lRWN0rfXsYdqGLfGMzCHJYEnWuB\nylrGPTxHspiS3crcxLhHL4Fex5mEPzvqpiOlyznn1k2sVxfOCANLYSUBTQpXyDVh\nrLCWWMnRqgHY5EZ8SeLWSmf+vMaRdY43ppYuCEIzJuBW90gQxbJJhyUSswP8ujUe\nqoArhKemXgNcaO9xOC8uHOpFsaCjiLubO30Jer4Lw6u3GvgW7PEnXQj4Z6WxPHOz\n3dCvdCSxxTyvMGSYsaLG8XFm4MuKaHiqgNB5KkmI3HmGADkvGNSlpn+BJwIDAQAB\no2swaTAUBgkrBgEEAYOaHQoEBwwFdHJpYWwwEQYJKwYBBAGDmh0EBAQMAi0xMBEG\nCSsGAQQBg5odCwQEDAIzMDARBgkrBgEEAYOaHQwEBAwCMzAwGAYJKwYBBAGDmh0N\nBAsMCTBYQkZGRUZGRjANBgkqhkiG9w0BAQsFAAOCAQEAapRj44Cv0jNMRovRc0av\nPZb/Q14fki+Gi0Wi0315N51w1eCyNDUASE/7XLW1rRoaCMTmlshl9pF4FWhcLmq2\nq0/1A/9AxYPaW4evN8x9LjZpHTfj7KoQkHzogJdOSY5ib93IwVwrymDjvvpKZtZZ\n7NLC9AXiQQ5t2Z9SDfVX1d+xfhVzAq5D/XYVieqjO9EaYAT9Ad/7NUckCE9Bgiwi\nnM+/EDq95k3XokQc3+K8FcHzFaFTS6InqUzrE3R2USsXen3KoHs/U9kTWmhOjyyw\neJIcDwpfk9lCAUOFV5a2Lj99P+UhuHnoraJ+RN3RID3kG6gR+jSvgF60UlBTRZM+\njg==\n-----END CERTIFICATE-----"
        }
        response = upload_license(test_data=license_data_invalid, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_LICENSE_INVALID == response.json().get("error")

    def test06_tags_less_than_30_upload_license_success(self, setup_and_teardown_neuron, setup_and_teardown_modbus, random_port):
        print("---given:without license and add 2 tags, when:upload license and write&read, then:success---")
        test_data = TestLicense.test_data
        tag_write_data = test_data['tag_write_data']
        tag_read_data = test_data['tag_read_data']
        license_data = test_data['license_data']

        self.add_tags_less_than_30(random_port)

        response = upload_license(test_data=license_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = write(test_data=tag_write_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert 666 == response.json()["tags"][0].get("value")

        os.remove("build/persistence/neuron.lic")

    def test07_tags_more_than_30_upload_license_success(self, setup_and_teardown_neuron, setup_and_teardown_modbus, random_port):
        print("---given:without license and add 31 tags, when:upload license and write&read, then:success---")
        test_data = TestLicense.test_data
        tag_write_data = test_data['tag_write_data']
        tag_read_data = test_data['tag_read_data']
        license_data_3_35 = test_data['license_data_3_35']

        self.add_tags_more_than_30(random_port)

        response = upload_license(test_data=license_data_3_35, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = write(test_data=tag_write_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(2)

        response = read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert 666 == response.json()["tags"][0].get("value")

        os.remove("build/persistence/neuron.lic")

    def test08_count_nodes_tags_with_license_success(self, setup_and_teardown_neuron, random_port):
        print("---given:upload license, when:count nodes&tags after add&delete node&group&tag, then:success with correct number---")
        test_data = TestLicense.test_data
        node_data = test_data['node_data']
        group_data = test_data['group_data']
        tag_config = test_data['tag_config']
        tag_delete = test_data['tag_delete']
        group_delete = test_data['group_delete']
        node_delete = test_data['node_delete']
        license_data = test_data['license_data']
        node_config = {
            "node": "modbus-node",
            "params": {
                "transport_mode": 0,
                "connection_mode": 0,
                "max_retries": 0,
                "retry_interval": 0, 
                "interval": 20,
                "host": "127.0.0.1",
                "port": random_port,
                "timeout": 3000
            }
        }

        response = upload_license(test_data=license_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = get_license(header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        assert 0 == response.json().get("used_nodes")
        assert 0 == response.json().get("used_tags")

        response = add_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = configure_node(test_data=node_config, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = get_license(header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        assert 1 == response.json().get("used_nodes")
        assert 0 == response.json().get("used_tags")

        response = add_group(test_data=group_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = get_license(header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        assert 1 == response.json().get("used_nodes")
        assert 0 == response.json().get("used_tags")

        response = add_tag(test_data=tag_config, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = get_license(header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        assert 1 == response.json().get("used_nodes")
        assert 2 == response.json().get("used_tags")

        response = delete_tag(test_data=tag_delete, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = get_license(header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        assert 1 == response.json().get("used_nodes")
        assert 1 == response.json().get("used_tags")

        response = delete_group(test_data=group_delete, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = get_license(header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        assert 1 == response.json().get("used_nodes")
        assert 0 == response.json().get("used_tags")

        response = delete_node(test_data=node_delete, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = get_license(header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        assert 0 == response.json().get("used_nodes")
        assert 0 == response.json().get("used_tags")

        os.remove("build/persistence/neuron.lic")

    def test09_tags_limit_test(self, setup_and_teardown_neuron, setup_and_teardown_modbus, random_port):
        print("---given:add 31 tags and upload license_30, when:write&read before&after delete 1 tag, then:failed before deleting and success after deleting---")
        test_data = TestLicense.test_data
        tag_write_data = test_data['tag_write_data']
        tag_read_data = test_data['tag_read_data']
        license_data = test_data['license_data']
        tag_delete = test_data['tag_delete']

        self.add_tags_more_than_30(random_port)

        response = upload_license(test_data=license_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = write(test_data=tag_write_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_LICENSE_MAX_TAGS == response.json().get("error")

        time.sleep(2)

        response = read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_LICENSE_MAX_TAGS == response.json()['tags'][0].get("error")

        response = delete_tag(test_data=tag_delete, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = write(test_data=tag_write_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(2)

        response = read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert 666 == response.json()["tags"][0].get("value")       

        os.remove("build/persistence/neuron.lic")
    
    def test10_nodes_limit_test(self, setup_and_teardown_neuron, setup_and_teardown_modbus, random_port):
        print("---given:add 32 nodes and upload license_30, when:write&read before&after delete 2 nodes, then:failed before deleting and success after deleting---")
        test_data = TestLicense.test_data
        tag_write_data = test_data['tag_write_data']
        tag_read_data = test_data['tag_read_data']
        license_data = test_data['license_data']
        
        node_delete_31 = {
            "name": "modbus-node-31"
        }
        node_delete_30 = {
            "name": "modbus-node-30"
        }
        node_data_templates = [{ 
            "name": f"modbus-node-{i}", 
            "plugin": "Modbus TCP" 
        } for i in range(1, 32)]

        self.add_tags_less_than_30(random_port)

        response = upload_license(test_data=license_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        add_nodes(node_data_templates, add_node, config)

        time.sleep(1)
        response = write(test_data=tag_write_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_LICENSE_MAX_NODES == response.json().get("error")

        time.sleep(2)

        response = read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_LICENSE_MAX_NODES == response.json()['tags'][0].get("error")

        response = delete_node(test_data=node_delete_31, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = delete_node(test_data=node_delete_30, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = write(test_data=tag_write_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(2)

        response = read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert 666 == response.json()["tags"][0].get("value")       

        os.remove("build/persistence/neuron.lic")