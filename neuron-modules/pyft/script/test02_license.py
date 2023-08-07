import pytest
import config
import subprocess
import os
from api.api import LoginAPI
from api.api import LicenseAPI
from api.api import NodeAPI
from api.api import GroupAPI
from api.api import TagAPI
from api.api import RWAPI
from data.error_codes import *
from config import NEURON_PATH
import time

class TestLicense:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.login_api = LoginAPI()
        self.license_api = LicenseAPI()
        self.node_api = NodeAPI()
        self.group_api = GroupAPI()
        self.tag_api = TagAPI()
        self.rw_api = RWAPI()

        start_dir = os.getcwd()
        os.chdir(NEURON_PATH)

        modbus_simulator_path = "./simulator/modbus_simulator"
        args_modbus = ["tcp", "60502"]
        command_modbus = [modbus_simulator_path] + args_modbus
        process_modbus = subprocess.Popen(command_modbus, stderr=subprocess.PIPE)

        neuron_path = "./neuron"
        args_neuron = ["--log"]
        command_neuron = [neuron_path] + args_neuron
        process_neuron = subprocess.Popen(command_neuron, stderr=subprocess.PIPE)
        time.sleep(1)
        os.chdir(start_dir)
        assert process_neuron.poll() is None

        yield

        node_data = {
            "name": "modbus-node"
        }
        self.node_api.delete_node(test_data=node_data, header_data=config.headers)
        os.chdir(NEURON_PATH) 
        process_modbus.kill()
        time.sleep(1)
        assert process_modbus.poll() is not None

        process_neuron.kill()
        time.sleep(1)
        _, err = process_neuron.communicate()
        assert process_neuron.poll() is not None, "Neuron process didn't stop"
        assert err.decode() == '', "stderr not empty: " + err.decode()
        os.remove("./persistence/sqlite.db")
        os.chdir(start_dir)

    test_data = {
        "node_data": {
            "name": "modbus-node",
            "plugin": "Modbus TCP"
        },
        "node_delete": {
            "name": "modbus-node"
        },
        "node_config": {
            "node": "modbus-node",
            "params": {
                "transport_mode": 0,
                "connection_mode": 0,
                "max_retries": 0,
                "retry_interval": 0, 
                "interval": 20,
                "host": "127.0.0.1",
                "port": 60502,
                "timeout": 3000
            }
        },
        "group_data": {
            "group": "modbus-group",
            "node": "modbus-node",
            "interval": 1000
        },
        "group_delete": {
            "group": "modbus-group",
            "node": "modbus-node"
        },
        "tag_config": {
            "node": "modbus-node",
            "group": "modbus-group",
            "tags": [
                {
                "name": "tag1",
                "address": "1!40001",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag2",
                "address": "1!40002",
                "attribute": 3,
                "type": 3,
                }
            ]
        },
        "tag_delete": {
            "node": "modbus-node",
            "group": "modbus-group",
            "tags": [
                "tag2"
            ]
        },
        "tag_config_31": {
            "node": "modbus-node",
            "group": "modbus-group",
            "tags": [
                {
                "name": "tag1",
                "address": "1!40001",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag2",
                "address": "1!40002",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag3",
                "address": "1!40003",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag4",
                "address": "1!40004",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag5",
                "address": "1!40005",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag6",
                "address": "1!40006",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag7",
                "address": "1!40007",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag8",
                "address": "1!40008",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag9",
                "address": "1!40009",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag10",
                "address": "1!40010",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag11",
                "address": "1!40011",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag12",
                "address": "1!40012",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag13",
                "address": "1!40013",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag14",
                "address": "1!40014",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag15",
                "address": "1!40015",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag16",
                "address": "1!40016",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag17",
                "address": "1!40017",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag18",
                "address": "1!40018",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag19",
                "address": "1!40019",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag20",
                "address": "1!40020",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag21",
                "address": "1!40021",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag22",
                "address": "1!40022",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag23",
                "address": "1!40023",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag24",
                "address": "1!40024",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag25",
                "address": "1!40025",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag26",
                "address": "1!40026",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag27",
                "address": "1!40027",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag28",
                "address": "1!40028",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag29",
                "address": "1!40029",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag30",
                "address": "1!40030",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag31",
                "address": "1!40031",
                "attribute": 3,
                "type": 3,
                }
            ]
        },
        "tag_config_5": {
            "node": "modbus-node",
            "group": "modbus-group",
            "tags": [
                {
                "name": "tag32",
                "address": "1!40032",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag33",
                "address": "1!40033",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag34",
                "address": "1!40034",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag35",
                "address": "1!40035",
                "attribute": 3,
                "type": 3,
                },
                {
                "name": "tag36",
                "address": "1!40036",
                "attribute": 3,
                "type": 3,
                }
            ]
        },
        "tag_write_data": {
            "node": "modbus-node",
            "group": "modbus-group",
            "tag": "tag1",
            "value": 666
        },
        "tag_read_data": {
            "node": "modbus-node",
            "group": "modbus-group",
        },
        "license_data": {
            "license": "-----BEGIN CERTIFICATE-----\nMIID7TCCAtWgAwIBAgIDOFVFMA0GCSqGSIb3DQEBCwUAMIGDMQswCQYDVQQGEwJD\nTjERMA8GA1UECAwIWmhlamlhbmcxETAPBgNVBAcMCEhhbmd6aG91MQwwCgYDVQQK\nDANFTVExDDAKBgNVBAsMA0VNUTESMBAGA1UEAwwJKi5lbXF4LmlvMR4wHAYJKoZI\nhvcNAQkBFg96aGFuZ3doQGVtcXguaW8wIBcNMjMwNzI2MDk1MjA2WhgPMjA5OTEy\nMzEwOTUyMDZaMH8xCzAJBgNVBAYTAkNOMScwJQYDVQQKDB7mna3lt57mmKDkupHn\np5HmioDmnInpmZDlhazlj7gxJzAlBgNVBAMMHuadreW3nuaYoOS6keenkeaKgOac\niemZkOWFrOWPuDEeMBwGCSqGSIb3DQEJARYPc3VwcG9ydEBlbXF4LmlvMIIBIjAN\nBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmTlAPpfFDEL7a92u/4Zd6owJXRPj\n5bpx6wNnnRz8nkwqnj8Eol/JStwOjuDsz/DG+lRWN0rfXsYdqGLfGMzCHJYEnWuB\nylrGPTxHspiS3crcxLhHL4Fex5mEPzvqpiOlyznn1k2sVxfOCANLYSUBTQpXyDVh\nrLCWWMnRqgHY5EZ8SeLWSmf+vMaRdY43ppYuCEIzJuBW90gQxbJJhyUSswP8ujUe\nqoArhKemXgNcaO9xOC8uHOpFsaCjiLubO30Jer4Lw6u3GvgW7PEnXQj4Z6WxPHOz\n3dCvdCSxxTyvMGSYsaLG8XFm4MuKaHiqgNB5KkmI3HmGADkvGNSlpn+BJwIDAQAB\no2swaTAUBgkrBgEEAYOaHQoEBwwFdHJpYWwwEQYJKwYBBAGDmh0EBAQMAi0xMBEG\nCSsGAQQBg5odCwQEDAIzMDARBgkrBgEEAYOaHQwEBAwCMzAwGAYJKwYBBAGDmh0N\nBAsMCTBYQkZGRUZGRjANBgkqhkiG9w0BAQsFAAOCAQEAapRj44Cv0jNMRovRc0av\nPZb/Q14fki+Gi0Wi0315N51w1eCyNDUASE/7XLW1rRoaCMTmlshl9pF4FWhcLmq2\nq0/1A/9AxYPaW4evN8x9LjZpHTfj7KoQkHzogJdOSY5ib93IwVwrymDjvvpKZtZZ\n7NLC9AXiQQ5t2Z9SDfVX1d+xfhVzAq5D/XYVieqjO9EaYAT9Ad/7NUckCE9Bgiwi\nnM+/EDq95k3XokQc3+K8FcHzFaFTS6InqUzrE3R2USsXen3KoHs/U9kTWmhOjyyw\neJIcDwpfk9lCAUOFV5a2Lj99P+UhuHnoraJ+RN3RID3kG6gR+jSvgF60UlBTRZM+\njg==\n-----END CERTIFICATE-----"
        },
        "license_data_3_35": {
            "license": "-----BEGIN CERTIFICATE-----\nMIIDuTCCAqGgAwIBAgIDSqu0MA0GCSqGSIb3DQEBCwUAMIGDMQswCQYDVQQGEwJD\nTjERMA8GA1UECAwIWmhlamlhbmcxETAPBgNVBAcMCEhhbmd6aG91MQwwCgYDVQQK\nDANFTVExDDAKBgNVBAsMA0VNUTESMBAGA1UEAwwJKi5lbXF4LmlvMR4wHAYJKoZI\nhvcNAQkBFg96aGFuZ3doQGVtcXguaW8wIBcNMjMwODAxMDM1MzU5WhgPMjA5OTEy\nMzEwMzUzNTlaME8xCzAJBgNVBAYTAkNOMQ0wCwYDVQQKDARFTVFYMQ0wCwYDVQQD\nDARFTVFYMSIwIAYJKoZIhvcNAQkBFhN4aW55dWFuLmhhbkBlbXF4LmlvMIIBIjAN\nBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyfj4b5Lpm+GfNG7JIFFctwH9t1/X\nM8g/gTcOnSleyC45M1fvOoRrT8atj3KhsfgEMEuT9QfvPcimiNZ98eR6BvBNTsdM\n3if8CX3km3WcHfm9Hob3y/jcRnpWT4VdJyvB2t/bHXpAi/x5TEb8KtXeVEfkWUZ9\nPnm9oplgYRWwHj7u6IK9Qkb9FWe34+9r3Qh5i7Ee/7vhSQQtTtiJ2G9Sr/B8QMfP\nKml/fCj3Z7nceXGYn+sVbYTMGQcnKff6ZpwHU8biKgZpAGD7PbZX01U5zc9JP0+6\n9H0FM3EDcgZe+8Rmz4LC7pdsNJRo+2gWkEqov0NR+5Ai7JfQ49L2hDxQtwIDAQAB\no2cwZTAUBgkrBgEEAYOaHQoEBwwFdHJpYWwwEQYJKwYBBAGDmh0EBAQMAi0xMBAG\nCSsGAQQBg5odCwQDDAEzMBEGCSsGAQQBg5odDAQEDAIzNTAVBgkrBgEEAYOaHQ0E\nCAwGMHhGRkZGMA0GCSqGSIb3DQEBCwUAA4IBAQCuQ8LyCBc7eCEMyor7xzcv6c2z\nHHb9dlc7xVCDFwsjCojqpx0Yu2RPPh95Fq/qTJvxQifptWdRsl94So3sQ9n8RGC2\nXwEPl+/v+nzg+IZoiAv7ZVITmsvX8KkqJn1fz4Wr+8BYfjwa6ttIj9MG0H7GNf4m\ns1ntZ1qx/3psP9b0xE6dne8AqBEgUn9NT6DAnpTQrgCRvXZhLj5O0M/5+qDjzYTD\nF37CkLwKRiWGF7qmOZ3TOabWa4SvFO10WaGALDrazJzAIvXaNIqsY0T4PSwaHCeV\nQd1fJ6uvxfCqzGL6Ks2deo9KapkUlOK3m5ykdWnI4K23bYRk3ccENOclr6OT\n-----END CERTIFICATE-----"
        }
        }

    def add_tags_less_than_30(self):
        test_data = TestLicense.test_data
        node_data = test_data['node_data']
        node_config = test_data['node_config']
        group_data = test_data['group_data']
        tag_config = test_data['tag_config']
        tag_write_data = test_data['tag_write_data']
        tag_read_data = test_data['tag_read_data']
    
        response = self.node_api.add_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
    
        response = self.node_api.configure_node(test_data=node_config, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
    
        response = self.group_api.add_group(test_data=group_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.tag_api.add_tag(test_data=tag_config, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.rw_api.write(test_data=tag_write_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = self.rw_api.read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert 666 == response.json()["tags"][0].get("value")

    def add_tags_more_than_30(self):
        test_data = TestLicense.test_data
        node_data = test_data['node_data']
        node_config = test_data['node_config']
        group_data = test_data['group_data']
        tag_config_31 = test_data['tag_config_31']
        tag_write_data = test_data['tag_write_data']
        tag_read_data = test_data['tag_read_data']
    
        response = self.node_api.add_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
    
        response = self.node_api.configure_node(test_data=node_config, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
    
        response = self.group_api.add_group(test_data=group_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.tag_api.add_tag(test_data=tag_config_31, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = self.rw_api.write(test_data=tag_write_data, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_LICENSE_INVALID == response.json().get("error")

        time.sleep(1)

        response = self.rw_api.read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_LICENSE_INVALID == response.json()['tags'][0].get("error")

    def test01_get_license_without_license_fail(self):
        os.remove(NEURON_PATH + f"/config/neuron-default.lic")
        os.remove(NEURON_PATH + f"/persistence/neuron.lic")
        response = self.license_api.get_license(header_data=config.headers)
        assert 404 == response.status_code
        assert NEU_ERR_LICENSE_NOT_FOUND == response.json().get("error")

    def test02_upload_invalid_license_fail(self):
        license_data_invalid = {
            "license": "-----BEGIN CERTIFICATE-----\nWRONGTCCAtWgAwIBAgIDOFVFMA0GCSqGSIb3DQEBCwUAMIGDMQswCQYDVQQGEwJD\nTjERMA8GA1UECAwIWmhlamlhbmcxETAPBgNVBAcMCEhhbmd6aG91MQwwCgYDVQQK\nDANFTVExDDAKBgNVBAsMA0VNUTESMBAGA1UEAwwJKi5lbXF4LmlvMR4wHAYJKoZI\nhvcNAQkBFg96aGFuZ3doQGVtcXguaW8wIBcNMjMwNzI2MDk1MjA2WhgPMjA5OTEy\nMzEwOTUyMDZaMH8xCzAJBgNVBAYTAkNOMScwJQYDVQQKDB7mna3lt57mmKDkupHn\np5HmioDmnInpmZDlhazlj7gxJzAlBgNVBAMMHuadreW3nuaYoOS6keenkeaKgOac\niemZkOWFrOWPuDEeMBwGCSqGSIb3DQEJARYPc3VwcG9ydEBlbXF4LmlvMIIBIjAN\nBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmTlAPpfFDEL7a92u/4Zd6owJXRPj\n5bpx6wNnnRz8nkwqnj8Eol/JStwOjuDsz/DG+lRWN0rfXsYdqGLfGMzCHJYEnWuB\nylrGPTxHspiS3crcxLhHL4Fex5mEPzvqpiOlyznn1k2sVxfOCANLYSUBTQpXyDVh\nrLCWWMnRqgHY5EZ8SeLWSmf+vMaRdY43ppYuCEIzJuBW90gQxbJJhyUSswP8ujUe\nqoArhKemXgNcaO9xOC8uHOpFsaCjiLubO30Jer4Lw6u3GvgW7PEnXQj4Z6WxPHOz\n3dCvdCSxxTyvMGSYsaLG8XFm4MuKaHiqgNB5KkmI3HmGADkvGNSlpn+BJwIDAQAB\no2swaTAUBgkrBgEEAYOaHQoEBwwFdHJpYWwwEQYJKwYBBAGDmh0EBAQMAi0xMBEG\nCSsGAQQBg5odCwQEDAIzMDARBgkrBgEEAYOaHQwEBAwCMzAwGAYJKwYBBAGDmh0N\nBAsMCTBYQkZGRUZGRjANBgkqhkiG9w0BAQsFAAOCAQEAapRj44Cv0jNMRovRc0av\nPZb/Q14fki+Gi0Wi0315N51w1eCyNDUASE/7XLW1rRoaCMTmlshl9pF4FWhcLmq2\nq0/1A/9AxYPaW4evN8x9LjZpHTfj7KoQkHzogJdOSY5ib93IwVwrymDjvvpKZtZZ\n7NLC9AXiQQ5t2Z9SDfVX1d+xfhVzAq5D/XYVieqjO9EaYAT9Ad/7NUckCE9Bgiwi\nnM+/EDq95k3XokQc3+K8FcHzFaFTS6InqUzrE3R2USsXen3KoHs/U9kTWmhOjyyw\neJIcDwpfk9lCAUOFV5a2Lj99P+UhuHnoraJ+RN3RID3kG6gR+jSvgF60UlBTRZM+\njg==\n-----END CERTIFICATE-----"
        }
        response = self.license_api.upload_license(test_data=license_data_invalid, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_LICENSE_INVALID == response.json().get("error")

    def test03_tag_less_than_30_without_license_success(self):
        self.add_tags_less_than_30()

    def test04_tag_more_than_30_without_license_fail(self):
        self.add_tags_more_than_30()

    def test05_upload_outdated_license_fail(self):
        license_data_invalid = {
            "license": "-----BEGIN CERTIFICATE-----\nWRONGTCCAtWgAwIBAgIDOFVFMA0GCSqGSIb3DQEBCwUAMIGDMQswCQYDVQQGEwJD\nTjERMA8GA1UECAwIWmhlamlhbmcxETAPBgNVBAcMCEhhbmd6aG91MQwwCgYDVQQK\nDANFTVExDDAKBgNVBAsMA0VNUTESMBAGA1UEAwwJKi5lbXF4LmlvMR4wHAYJKoZI\nhvcNAQkBFg96aGFuZ3doQGVtcXguaW8wIBcNMjMwNzI2MDk1MjA2WhgPMjA5OTEy\nMzEwOTUyMDZaMH8xCzAJBgNVBAYTAkNOMScwJQYDVQQKDB7mna3lt57mmKDkupHn\np5HmioDmnInpmZDlhazlj7gxJzAlBgNVBAMMHuadreW3nuaYoOS6keenkeaKgOac\niemZkOWFrOWPuDEeMBwGCSqGSIb3DQEJARYPc3VwcG9ydEBlbXF4LmlvMIIBIjAN\nBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmTlAPpfFDEL7a92u/4Zd6owJXRPj\n5bpx6wNnnRz8nkwqnj8Eol/JStwOjuDsz/DG+lRWN0rfXsYdqGLfGMzCHJYEnWuB\nylrGPTxHspiS3crcxLhHL4Fex5mEPzvqpiOlyznn1k2sVxfOCANLYSUBTQpXyDVh\nrLCWWMnRqgHY5EZ8SeLWSmf+vMaRdY43ppYuCEIzJuBW90gQxbJJhyUSswP8ujUe\nqoArhKemXgNcaO9xOC8uHOpFsaCjiLubO30Jer4Lw6u3GvgW7PEnXQj4Z6WxPHOz\n3dCvdCSxxTyvMGSYsaLG8XFm4MuKaHiqgNB5KkmI3HmGADkvGNSlpn+BJwIDAQAB\no2swaTAUBgkrBgEEAYOaHQoEBwwFdHJpYWwwEQYJKwYBBAGDmh0EBAQMAi0xMBEG\nCSsGAQQBg5odCwQEDAIzMDARBgkrBgEEAYOaHQwEBAwCMzAwGAYJKwYBBAGDmh0N\nBAsMCTBYQkZGRUZGRjANBgkqhkiG9w0BAQsFAAOCAQEAapRj44Cv0jNMRovRc0av\nPZb/Q14fki+Gi0Wi0315N51w1eCyNDUASE/7XLW1rRoaCMTmlshl9pF4FWhcLmq2\nq0/1A/9AxYPaW4evN8x9LjZpHTfj7KoQkHzogJdOSY5ib93IwVwrymDjvvpKZtZZ\n7NLC9AXiQQ5t2Z9SDfVX1d+xfhVzAq5D/XYVieqjO9EaYAT9Ad/7NUckCE9Bgiwi\nnM+/EDq95k3XokQc3+K8FcHzFaFTS6InqUzrE3R2USsXen3KoHs/U9kTWmhOjyyw\neJIcDwpfk9lCAUOFV5a2Lj99P+UhuHnoraJ+RN3RID3kG6gR+jSvgF60UlBTRZM+\njg==\n-----END CERTIFICATE-----"
        }
        response = self.license_api.upload_license(test_data=license_data_invalid, header_data=config.headers)
        assert 400 == response.status_code
        assert NEU_ERR_LICENSE_INVALID == response.json().get("error")

    def test06_tags_less_than_30_upload_license_success(self):
        test_data = TestLicense.test_data
        tag_write_data = test_data['tag_write_data']
        tag_read_data = test_data['tag_read_data']
        license_data = test_data['license_data']

        self.add_tags_less_than_30()

        response = self.license_api.upload_license(test_data=license_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.rw_api.write(test_data=tag_write_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = self.rw_api.read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert 666 == response.json()["tags"][0].get("value")

        os.remove(NEURON_PATH + f"/persistence/neuron.lic")

    def test07_tags_more_than_30_upload_license_success(self):
        test_data = TestLicense.test_data
        tag_write_data = test_data['tag_write_data']
        tag_read_data = test_data['tag_read_data']
        license_data_3_35 = test_data['license_data_3_35']

        self.add_tags_more_than_30()

        response = self.license_api.upload_license(test_data=license_data_3_35, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.rw_api.write(test_data=tag_write_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = self.rw_api.read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert 666 == response.json()["tags"][0].get("value")

        os.remove(NEURON_PATH + f"/persistence/neuron.lic")

    def test08_count_nodes_tags_with_license_success(self):
        test_data = TestLicense.test_data
        node_data = test_data['node_data']
        node_config = test_data['node_config']
        group_data = test_data['group_data']
        tag_config = test_data['tag_config']
        tag_delete = test_data['tag_delete']
        group_delete = test_data['group_delete']
        node_delete = test_data['node_delete']
        license_data = test_data['license_data']

        response = self.license_api.upload_license(test_data=license_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = self.license_api.get_license(header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        assert 0 == response.json().get("used_nodes")
        assert 0 == response.json().get("used_tags")

        response = self.node_api.add_node(test_data=node_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.node_api.configure_node(test_data=node_config, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.license_api.get_license(header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        assert 1 == response.json().get("used_nodes")
        assert 0 == response.json().get("used_tags")

        response = self.group_api.add_group(test_data=group_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.license_api.get_license(header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        assert 1 == response.json().get("used_nodes")
        assert 0 == response.json().get("used_tags")

        response = self.tag_api.add_tag(test_data=tag_config, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.license_api.get_license(header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        assert 1 == response.json().get("used_nodes")
        assert 2 == response.json().get("used_tags")

        response = self.tag_api.delete_tag(test_data=tag_delete, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.license_api.get_license(header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        assert 1 == response.json().get("used_nodes")
        assert 1 == response.json().get("used_tags")

        response = self.group_api.delete_group(test_data=group_delete, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.license_api.get_license(header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        assert 1 == response.json().get("used_nodes")
        assert 0 == response.json().get("used_tags")

        response = self.node_api.delete_node(test_data=node_delete, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.license_api.get_license(header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        assert 0 == response.json().get("used_nodes")
        assert 0 == response.json().get("used_tags")

        os.remove(NEURON_PATH + f"/persistence/neuron.lic")

    def test09_tags_limit_test(self):
        test_data = TestLicense.test_data
        tag_write_data = test_data['tag_write_data']
        tag_read_data = test_data['tag_read_data']
        license_data = test_data['license_data']
        tag_delete = test_data['tag_delete']

        self.add_tags_more_than_30()

        response = self.license_api.upload_license(test_data=license_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.rw_api.write(test_data=tag_write_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_LICENSE_MAX_TAGS == response.json().get("error")

        time.sleep(1)

        response = self.rw_api.read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_LICENSE_MAX_TAGS == response.json()['tags'][0].get("error")

        response = self.tag_api.delete_tag(test_data=tag_delete, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.rw_api.write(test_data=tag_write_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = self.rw_api.read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert 666 == response.json()["tags"][0].get("value")       

        os.remove(NEURON_PATH + f"/persistence/neuron.lic")
    
    def test10_nodes_limit_test(self):
        test_data = TestLicense.test_data
        tag_write_data = test_data['tag_write_data']
        tag_read_data = test_data['tag_read_data']
        license_data = test_data['license_data']
        node_data_1 = {
            "name": "modbus-node-1",
            "plugin": "Modbus TCP"
        }
        node_data_2 = {
            "name": "modbus-node-2",
            "plugin": "Modbus TCP"
        }
        node_data_3 = {
            "name": "modbus-node-3",
            "plugin": "Modbus TCP"
        }
        node_data_4 = {
            "name": "modbus-node-4",
            "plugin": "Modbus TCP"
        }
        node_data_5 = {
            "name": "modbus-node-5",
            "plugin": "Modbus TCP"
        }
        node_data_6 = {
            "name": "modbus-node-6",
            "plugin": "Modbus TCP"
        }
        node_data_7 = {
            "name": "modbus-node-7",
            "plugin": "Modbus TCP"
        }
        node_data_8 = {
            "name": "modbus-node-8",
            "plugin": "Modbus TCP"
        }
        node_data_9 = {
            "name": "modbus-node-9",
            "plugin": "Modbus TCP"
        }
        node_data_10 = {
            "name": "modbus-node-10",
            "plugin": "Modbus TCP"
        }
        node_data_11 = {
            "name": "modbus-node-11",
            "plugin": "Modbus TCP"
        }
        node_data_12 = {
            "name": "modbus-node-12",
            "plugin": "Modbus TCP"
        }
        node_data_13 = {
            "name": "modbus-node-13",
            "plugin": "Modbus TCP"
        }
        node_data_14 = {
            "name": "modbus-node-14",
            "plugin": "Modbus TCP"
        }
        node_data_15 = {
            "name": "modbus-node-15",
            "plugin": "Modbus TCP"
        }
        node_data_16 = {
            "name": "modbus-node-16",
            "plugin": "Modbus TCP"
        }
        node_data_17 = {
            "name": "modbus-node-17",
            "plugin": "Modbus TCP"
        }
        node_data_18 = {
            "name": "modbus-node-18",
            "plugin": "Modbus TCP"
        }
        node_data_19 = {
            "name": "modbus-node-19",
            "plugin": "Modbus TCP"
        }
        node_data_20 = {
            "name": "modbus-node-20",
            "plugin": "Modbus TCP"
        }
        node_data_21 = {
            "name": "modbus-node-21",
            "plugin": "Modbus TCP"
        }
        node_data_22 = {
            "name": "modbus-node-22",
            "plugin": "Modbus TCP"
        }
        node_data_23 = {
            "name": "modbus-node-23",
            "plugin": "Modbus TCP"
        }
        node_data_24 = {
            "name": "modbus-node-24",
            "plugin": "Modbus TCP"
        }
        node_data_25 = {
            "name": "modbus-node-25",
            "plugin": "Modbus TCP"
        }
        node_data_26 = {
            "name": "modbus-node-26",
            "plugin": "Modbus TCP"
        }
        node_data_27 = {
            "name": "modbus-node-27",
            "plugin": "Modbus TCP"
        }
        node_data_28 = {
            "name": "modbus-node-28",
            "plugin": "Modbus TCP"
        }
        node_data_29 = {
            "name": "modbus-node-29",
            "plugin": "Modbus TCP"
        }
        node_data_30 = {
            "name": "modbus-node-30",
            "plugin": "Modbus TCP"
        }
        node_data_31 = {
            "name": "modbus-node-31",
            "plugin": "Modbus TCP"
        }
        node_delete_31 = {
            "name": "modbus-node-31"
        }
        node_delete_30 = {
            "name": "modbus-node-30"
        }

        self.add_tags_less_than_30()

        response = self.license_api.upload_license(test_data=license_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.node_api.add_node(test_data=node_data_1, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_2, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_3, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_4, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_5, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_6, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_7, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_8, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_9, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_10, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_11, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_12, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_13, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_14, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_15, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_16, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_17, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_18, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_19, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_20, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_21, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_22, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_23, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_24, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_25, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_26, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_27, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_28, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_29, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_30, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.add_node(test_data=node_data_31, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        time.sleep(1)
        response = self.rw_api.write(test_data=tag_write_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_LICENSE_MAX_NODES == response.json().get("error")

        time.sleep(1)

        response = self.rw_api.read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_LICENSE_MAX_NODES == response.json()['tags'][0].get("error")

        response = self.node_api.delete_node(test_data=node_delete_31, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
        response = self.node_api.delete_node(test_data=node_delete_30, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        response = self.rw_api.write(test_data=tag_write_data, header_data=config.headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        time.sleep(1)

        response = self.rw_api.read(test_data=tag_read_data, header_data=config.headers)
        assert 200 == response.status_code
        assert 666 == response.json()["tags"][0].get("value")       

        os.remove(NEURON_PATH + f"/persistence/neuron.lic")