import uuid
import copy
from unittest.mock import patch

from models.payment import Payment
from starlette.datastructures import Address
from v1.dependencies.dao_dep import get_session_with_commit
from v1.users.dao import PaymentDAO


# TODO ТЕСТЫ нагрузочные написать напрмиер на 100/1000 закпросов и смотреть количество записей в БД
# TODO РПОБЛЕМА С ЗАПУСКОМ ДВУХ ТЕСТОВ ОДНОВРЕМЕННО - с сессией какая то фигня
class TestPaymentCallback:
    callback_mock_success = {
        "amount": {"currency": "RUB", "value": "32.00"},
        "authorization_details": {
            "auth_code": "235381",
            "rrn": "703693542966385",
            "three_d_secure": {
                "applied": False,
                "challenge_completed": False,
                "method_completed": False,
            },
        },
        "captured_at": "2025-05-26T09:59:37.989Z",
        "created_at": "2025-05-26T09:59:30.251Z",
        "description": "Проект Строительство мечети, айди 22",
        "id": "2fc64f42-000f-5000-8000-14945ca734f5",
        "income_amount": {"currency": "RUB", "value": "30.88"},
        "metadata": {
            "payment_id": 1,
            "project_id": 1,
            "user_id": 1,
        },
        "paid": True,
        "payment_method": {
            "card": {
                "card_product": {"code": "E"},
                "card_type": "MasterCard",
                "expiry_month": "12",
                "expiry_year": "2027",
                "first6": "555555",
                "issuer_country": "US",
                "last4": "4444",
            },
            "id": "2fc64f42-000f-5000-8000-14945ca734f5",
            "saved": False,
            "status": "inactive",
            "title": "Bank card *4444",
            "type": "bank_card",
        },
        "recipient": {"account_id": "469140", "gateway_id": "2324047"},
        "refundable": True,
        "refunded_amount": {"currency": "RUB", "value": "0.00"},
        "status": "succeeded",
        "test": True,
    }

    # TEST IT WORK BUT NOT IN SCOPE AND RUN SINGULAR
    @patch("fastapi.Request.client", Address("185.71.76.1", 1234))  # For ip_security checker
    async def test_callback_cancelled(self, ac) -> None:
        # Create an independent deep copy of the original dictionary,
        # including all nested structures, to prevent side effects during modification.
        callback_mock_canceled = copy.deepcopy(self.callback_mock_success)
        callback_mock_canceled["status"] = "canceled"

        response = await ac.post("/app/v1/payments/yookassa_callback", json={"object": callback_mock_canceled})
        assert response.status_code == 200

        session_gen = get_session_with_commit()
        session = await session_gen.__anext__()

        payment_dao = PaymentDAO(session=session)
        payments: list[Payment] = await payment_dao.find_all()
        assert len(payments) == 6  # sum of mocked data without new

    @patch("fastapi.Request.client", Address("185.71.76.1", 1234))  # For ip_security checker
    async def test_callback_success(self, ac) -> None:
        response = await ac.post("/app/v1/payments/yookassa_callback", json={"object": self.callback_mock_success})
        assert response.status_code == 200

        session_gen = get_session_with_commit()
        session = await session_gen.__anext__()

        payment_dao = PaymentDAO(session=session)
        payments: list[Payment] = await payment_dao.find_all()
        assert len(payments) == 7

        current_payment = payments[-1]
        assert current_payment.id == uuid.UUID("2fc64f42-000f-5000-8000-14945ca734f5")

        assert current_payment.project_id == 1
        assert current_payment.user_id == 1
        assert current_payment.stage_id == 2
        assert current_payment.amount == 32.0

    async def test_callback_forbidden(self, ac) -> None:
        response = await ac.post("/app/v1/payments/yookassa_callback", json={"object": self.callback_mock_success})
        assert response.status_code == 403
