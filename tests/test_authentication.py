import asyncio
import string
import random
import pytest
from starlette import status


@pytest.fixture(scope="module")
def token_storage():
    return {
        "access_token": None,
        "refresh_token": None
    }


def generate_random_token(length: int = 32) -> str:
    """
    Генерирует случайную строку для использования в качестве токена.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password, age, exp_status_code, expected_response",
    [
        ("username_test", "admin", 18, status.HTTP_200_OK, {"username": "username_test"}),
        ("username_test", "admin", 18, status.HTTP_400_BAD_REQUEST,
         {"detail": "User with username 'username_test' already exists."})
    ]
)
async def test_registration(
        async_client,
        username: str,
        password: str,
        age: int,
        exp_status_code: int,
        expected_response: dict
):
    response = await async_client.post('/auth/register', json={
        "username": username,
        "password": password,
        "age": age
    })

    assert response.status_code == exp_status_code
    assert response.json() == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password, exp_status_code",
    [
        ("wrong_login", "admin", status.HTTP_404_NOT_FOUND),
        ("username_test", "wrong_password", status.HTTP_403_FORBIDDEN),
        ("username_test", "admin", status.HTTP_200_OK),
    ]
)
async def test_login_and_authorize(
        async_client,
        username: str,
        password: str,
        exp_status_code: int,
        token_storage: dict  # Pass the token storage fixture
):
    response = await async_client.post('/auth/login',
                                       json={
                                           "username": username,
                                           "password": password
                                       })
    r_s_c = response.status_code
    assert r_s_c == exp_status_code, "Login Failed"

    if r_s_c == status.HTTP_404_NOT_FOUND:
        assert response.json() == {"detail": "User not found!"}
    elif r_s_c == status.HTTP_403_FORBIDDEN:
        assert response.json() == {"detail": "Login or password is not valid"}

    if response.status_code == status.HTTP_200_OK:
        token_storage['access_token'] = response.cookies.get('access_token')
        token_storage['refresh_token'] = response.cookies.get('refresh_token')
        assert token_storage['access_token'] == response.json().get('access_token'), \
            "access_token не был установлен в куки!"
        assert token_storage['refresh_token'], "refresh_token не установлен в куки!"
        async_client.cookies.set('access_token', token_storage['access_token'])
        async_client.cookies.set('refresh_token', token_storage['refresh_token'])
        new_response = await async_client.get('/auth/authorize')
        assert new_response.status_code == status.HTTP_200_OK
        assert new_response.json() == username


@pytest.mark.asyncio
async def test_refresh(async_client, token_storage: dict):
    m_access_token = token_storage['access_token']
    m_refresh_token = token_storage['refresh_token']

    async_client.cookies.set('access_token', m_access_token)
    async_client.cookies.set('refresh_token',m_refresh_token)

    response = await async_client.post("/auth/refresh")

    assert response.status_code == status.HTTP_200_OK

    assert response.cookies.get('access_token') != m_access_token, "access токен не обновлен!"
    assert response.cookies.get('refresh_token') != m_refresh_token, "refresh токен не обновлен!"

    token_storage['access_token'] = response.cookies.get('access_token')
    token_storage['refresh_token'] = response.cookies.get('refresh_token')


async def test_auto_refresh(async_client, token_storage: dict):
    await asyncio.sleep(61)
    async_client.cookies.set('access_token',  token_storage['access_token'])
    async_client.cookies.set('refresh_token', token_storage['refresh_token'])
    response = await async_client.get("/auth/authorize")

    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get('access_token') != token_storage[
        'access_token'], "Токен доступа не был обновлен!"
    assert response.cookies.get('refresh_token') != token_storage[
        'refresh_token'], "Рефреш токен не был обновлен!"

    token_storage['access_token'] = response.cookies.get('access_token')
    token_storage['refresh_token'] = response.cookies.get('refresh_token')

    async_client.cookies.set('access_token',  '')
    async_client.cookies.set('refresh_token', token_storage['refresh_token'])

    response = await async_client.get("/auth/authorize")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid access token'}
