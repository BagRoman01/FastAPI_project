from contextlib import nullcontext as does_not_raise
import pytest
from starlette import status


class TestAuthentication:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "username, password, age, exp_exception, exp_status_code",
        [
            # ("username_test", "admin", 18, pytest.raises(UserAlreadyExistsError), status.HTTP_400_BAD_REQUEST),
            ("username_test", "admin", 18, does_not_raise(), status.HTTP_200_OK),
        ]
    )
    async def test_registration(
            self,
            client,
            username,
            password,
            age,
            exp_exception,
            exp_status_code
    ):
        response = await client.post('/auth/register', json={
            "username": username,
            "password": password,
            "age": age
        })
        with exp_exception:
            assert response.status_code == exp_status_code
            assert response.json().get('username') == username


