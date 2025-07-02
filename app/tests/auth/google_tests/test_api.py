class TestGoogle:
    async def test_login(self, ac):
        url = (
            "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=82940823785-f0042dda793mqu66np8a"
            "9p72alrenme1.apps.googleusercontent.com&redirect_uri=http://localhost:8000/app/v1/google/callback/&scop"
            "e=openid%20profile%20email&access_type=offline"
        )
        response = await ac.get("/app/v1/google/login/")
        assert response.status_code == 200

        redirect_uri = response.json().get("redirect_url")
        assert redirect_uri == url


# TODO сделать фейк гугл клиент? если только в этом будет нужда
# TODO эмитаця регистрации нового пользака и проверка наличия ЖВТ токенов - не требуется ТК есть юнит тесты
