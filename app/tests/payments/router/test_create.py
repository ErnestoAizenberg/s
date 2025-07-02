class TestPaymentCreate:
    project_id = 1
    amount = 100

    async def test_400_authorization(self, ac) -> None:
        response = await ac.post(f"/app/v1/payments/{self.project_id}/{self.amount}")
        assert response.status_code == 400
        assert response.json() == {"detail": "Токен отсутствует в заголовке"}

    async def test_project_id_validate(self, auth_ac) -> None:
        response = await auth_ac.client.post(f"/app/v1/payments/{99}/{self.amount}", cookies=auth_ac.cookies.dict())
        assert response.status_code == 422

    async def test_create(self, auth_ac) -> None:
        response = await auth_ac.client.post(f"/app/v1/payments/{1}/{self.amount}", cookies=auth_ac.cookies.dict())
        assert response.status_code == 200
        assert "https://yoomoney.ru/checkout/payments/v2/contract?orderId=" in response.json().get("redirect_url", None)
