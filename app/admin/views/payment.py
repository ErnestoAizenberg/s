from admin.views.auth_permissions import FundAdminAccess
from admin.views.base_classes.image_as_file_singular_preview import BaseAdminView
from models.payment import Payment


class PaymentAdmin(BaseAdminView, FundAdminAccess, model=Payment):
    column_list = [Payment.id]
    icon = "fa-solid fa-credit-card"
    name = "Платёж"
    name_plural = "Платежи"

    column_searchable_list = [Payment.project_id]
