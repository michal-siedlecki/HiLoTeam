import os
import requests


def test_user_can_login():
    name = "janusz"
    r = requests.get("http://127.0.0.1:8000/panel", auth=(name, "1234"))
    assert name in r.content.decode("utf-8")


def test_user_can_not_login():
    name = "janusz"
    r = requests.get("http://127.0.0.1:8000/panel", auth=(name, "1234999"))
    assert r.status_code == 403


def test_user_can_put_key():
    name = "janusz"
    data = {"key_text": "123456"}
    requests.post("http://127.0.0.1:8000/panel", auth=(name, "1234"), data=data)
    filename = f"test_{name}_id_rsa.pub"
    assert filename in os.listdir(".")
    os.remove(filename)
