import pytest
from .HttpClient import HttpClient
import requests
import logging
import allure

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def update_headers_with_token():
    headers = {'x-api-key': 'reqres-free-v1'}
    res = requests.post("https://reqres.in/api/login", json={"email": "eve.holt@reqres.in", "password": "cityslicka"}, headers=headers)
    headers['Authorization'] = f"Bearer {res.json()['token']}"
    return headers

@pytest.fixture(scope="session")
def client():
    return Httpclient("https://reqres.in/api")

@allure.title("登录接口参数化测试")
@pytest.mark.parametrize("email,password", [
    ("eve.holt@reqres.in", "cityslicka"),
    ("user2", ""),
    ("", ""),
], ids=["有效账号", "缺失密码", "空参数"])
def test_login(email, password, client):
    headers = {'x-api-key': 'reqres-free-v1'}
    data = {'email':email, 'password':password}
    with allure.step(f"发送登录请求: email={email}, password={password}"):
        logger.info(f"测试登录参数: {data}")
        res = client.post('/login', data=data, headers=headers)
        logger.info(f"响应内容: {res.json()}")

    if email == "eve.holt@reqres.in" and password == 'cityslicka':
        assert res.status_code == 200
    else:
        assert res.status_code != 200

@allure.title("用户列表查询")
def test_get_user_info(client, update_headers_with_token):
    headers = update_headers_with_token
    with allure.step("调用 /users 接口查询用户列表"):
        res = client.get('/users?page=2', headers=headers)
        logger.info(f"用户信息响应: {res.json()}")
    assert res.status_code == 200
    assert "data" in res.json()

@allure.title("创建新用户")
def test_create_user(client, update_headers_with_token):
    headers = update_headers_with_token
    payload = {'name': 'Xueying', 'job': 'student'}
    with allure.step(f"创建用户: {payload}"):
        res = client.post('/users', data=payload, headers=headers)
        logger.info(f"创建响应: {res.json()}")
    res = client.post('/users', data ={'name': 'Xueying', 'job': 'student'}, headers=headers)
    assert  res.status_code == 201
    assert res.json()['name'] == 'Xueying'
