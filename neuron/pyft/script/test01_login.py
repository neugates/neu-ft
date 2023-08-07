from api.api import LoginAPI
import pytest
import time
import os
import subprocess
import config
from data.error_codes import *
from config import NEURON_PATH

class TestLogin:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        
        self.login_api = LoginAPI()

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

    def test01_login_success(self):
        user_data = {
            "name": "admin",
            "pass": "0000"
        }
        response = self.login_api.login(test_data=user_data)
        assert 200 == response.status_code
        print(response.json())
        config.TOKEN = response.json().get("token")
    
    def test02_login_invalid_user_fail(self):
        user_data = {
            "name": "wrong_name",
            "pass": "0000"
        }
        response = self.login_api.login(test_data=user_data)
        assert 401 == response.status_code
        assert NEU_ERR_INVALID_USER == response.json().get("error")

    def test03_login_invalid_password_fail(self):
        user_data = {
            "name": "admin",
            "pass": "wrong_password"
        }
        response = self.login_api.login(test_data=user_data)
        assert 401 == response.status_code
        assert NEU_ERR_INVALID_PASSWORD == response.json().get("error")
    
    def test04_login_change_password_success(self):
        user_data1 = {
            "name": "admin",
            "old_pass": "0000",
            "new_pass": "1234"
        }
        headers = {
            "Authorization": f"Bearer {config.TOKEN}"
        }
        config.headers = headers
        response = self.login_api.change_password(test_data=user_data1, header_data=headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        user_data2 = {
            "name": "admin",
            "old_pass": "1234",
            "new_pass": "0000"
        }
        response = self.login_api.change_password(test_data=user_data2, header_data=headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
    