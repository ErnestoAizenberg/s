from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException
from v1.payment.use_cases.callback import YooCallbackSuccessUseCaseImpl


class TestYookassaClientIpSecurityChecker:
    async def test_ip_in_range(self):
        request = AsyncMock()
        request.client.host = "185.71.76.1"

        use_case = YooCallbackSuccessUseCaseImpl(request, AsyncMock())
        try:
            await use_case._YooCallbackSuccessUseCaseImpl__yookassa_client_ip_security_checker()
        except HTTPException:
            pytest.fail("Unexpected YookassaCallbackForbiddenException")

    async def test_ip_not_in_range(self):
        request = AsyncMock()
        request.client.host = "192.168.1.1"

        use_case = YooCallbackSuccessUseCaseImpl(request, AsyncMock())

        with pytest.raises(HTTPException):
            await use_case._YooCallbackSuccessUseCaseImpl__yookassa_client_ip_security_checker()
