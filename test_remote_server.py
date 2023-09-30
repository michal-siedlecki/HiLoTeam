import requests




def test_can_user_login():
    name = 'janusz'
    r = requests.get('http://127.0.0.1:8000', auth=(name, '1234'))
    assert name in r.content.decode('utf-8')
