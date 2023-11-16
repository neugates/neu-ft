from api.api import login, change_password
import pytest
import time
import os
import shutil
from pathlib import Path
import json
import subprocess
import config
from data.error_codes import *

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
        shutil.copy2("build/logs/neuron.log", "neu-ft/neuron/report/test01_login_neuron.log")
        os.remove("build/logs/neuron.log")

class TestLogin:

    with open('neu-ft/neuron/data/test01_login_data.json') as f:
        test_data = json.load(f)

    def test01_login_success(self, setup_and_teardown_neuron):
        print("---given:name and password, when:login, then:success with token---")
        test_data = TestLogin.test_data
        user_data = test_data['correct_user_data']

        response = login(test_data=user_data)
        assert 200 == response.status_code
        print(response.json())
        config.TOKEN = response.json().get("token")
    
    def test02_login_invalid_user_fail(self, setup_and_teardown_neuron):
        print("---given:invalid user name, when:login, then:login failed and return error---")
        test_data = TestLogin.test_data
        user_data = test_data['invalid_user']

        response = login(test_data=user_data)
        assert 401 == response.status_code
        assert NEU_ERR_INVALID_USER_OR_PASSWORD == response.json().get("error")

    def test03_login_invalid_password_fail(self, setup_and_teardown_neuron):
        print("---given:invalid password, when:login, then:login failed and return error---")
        test_data = TestLogin.test_data
        user_data = test_data['invalid_password']

        response = login(test_data=user_data)
        assert 401 == response.status_code
        assert NEU_ERR_INVALID_USER_OR_PASSWORD == response.json().get("error")
    
    def test04_login_change_password_success(self, setup_and_teardown_neuron):
        print("---given:name, old and new password, when:login, then:success---")
        test_data = TestLogin.test_data
        user_data1 = test_data['change_password1']
        headers = {
            "Authorization": f"Bearer {config.TOKEN}"
        }
        config.headers = headers
        response = change_password(test_data=user_data1, header_data=headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")

        user_data2 = test_data['change_password2']
        response = change_password(test_data=user_data2, header_data=headers)
        assert 200 == response.status_code
        assert NEU_ERR_SUCCESS == response.json().get("error")
