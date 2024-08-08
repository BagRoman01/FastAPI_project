import pytest
from starlette import status

# global access_token, refresh_token
# access_token: str | None = None
# refresh_token: str | None = None
#


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
        self,
        client,
        username: str,
        password: str,
        age: int,
        exp_status_code: int,
        expected_response: dict
):
    response = await client.post('/auth/register', json={
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
        self,
        client,
        username: str,
        password: str,
        exp_status_code: int
):
    response = await client.post('/auth/login',
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

    access_token = response.cookies.get('access_token')
    refresh_token = response.cookies.get('refresh_token')
    if response.status_code == status.HTTP_200_OK:
        assert access_token == response.json().get('access_token'), \
            "access_token не был установлен в куки!"
        assert refresh_token, "refresh_token не установлен в куки!"
        new_response = await client.get('/auth/authorize', cookies={
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        assert new_response.status_code == status.HTTP_200_OK
        assert new_response.json() == username

#
# async def test_update():
#
