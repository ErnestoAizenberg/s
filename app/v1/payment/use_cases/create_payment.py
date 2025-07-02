import var_dump as var_dump
from models.project import Project
from models.user import User
from pydantic_core import Url
from sqlalchemy.ext.asyncio import AsyncSession
from v1.payment.schemas import YooMetadataInputSchema, YooPaymentUrlSchema
from v1.payment.validators import project_id_validator
from v1.users.dao import ProjectDAO
from yookassa import Payment as YookassaStockPayment
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.models.currency import Currency
from yookassa.domain.models.receipt import Receipt, ReceiptItem
from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder


class CreateYooPaymentUseCaseImpl:
    def __init__(self, amount: int, user_data: User, project_id: int, return_url: Url, session: AsyncSession):
        self.session = session
        self.amount = amount
        self.user_data = user_data
        self.project_id = project_id
        self.return_url = return_url

    async def execute(self) -> YooPaymentUrlSchema:
        await project_id_validator(project_id=self.project_id, session=self.session)
        built_payment = await self.yoo_payment_build()
        return YooPaymentUrlSchema(redirect_url=Url(built_payment.confirmation.confirmation_url))

    @property
    async def project(self) -> Project:
        project_dao = ProjectDAO(session=self.session)
        project = await project_dao.find_one_or_none_by_id(data_id=self.project_id)
        return project

    async def yoo_payment_build(self) -> YookassaStockPayment:
        project = await self.project
        metadata = YooMetadataInputSchema(project_id=str(project.id), user_id=str(self.user_data.id))

        receipt = Receipt()
        receipt.customer = {"email": self.user_data.email}
        receipt.tax_system_code = 1
        receipt.items = [
            ReceiptItem(
                {
                    "description": f"Пожертвование на проект {project.description}",
                    "quantity": 2.0,
                    "amount": {"value": self.amount, "currency": Currency.RUB},
                    "vat_code": 2,
                }
            ),
        ]

        builder = PaymentRequestBuilder()
        (
            builder.set_amount({"value": self.amount, "currency": Currency.RUB})
            .set_confirmation({"type": ConfirmationType.REDIRECT, "return_url": self.return_url})
            .set_capture(True)
            .set_description(f"{project.description}, айди {self.project_id}")
            .set_metadata((metadata.model_dump()))
            .set_receipt(receipt)
        )

        request = builder.build()
        built_payment = YookassaStockPayment.create(request)

        var_dump.var_dump(built_payment)  # вывод всей структуры в логи
        return built_payment
