import requests

url = "http://localhost:8000/app/v1/payments/yookassa_callback"
callback_mock_canceled = {
    "amount": {"currency": "RUB", "value": "32.00"},
    "authorization_details": {
        "auth_code": "235381",
        "rrn": "703693542966385",
        "three_d_secure": {"applied": False, "challenge_completed": False, "method_completed": False},
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
    "status": "canceled",
    "test": True,
}

response = requests.post(url, json={"object": callback_mock_canceled})
