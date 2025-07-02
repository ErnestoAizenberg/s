from admin.views.auth import MyAuthenticationBackend
from admin.views.city import CityAdmin
from admin.views.country import CountryAdmin
from admin.views.file import FileAdmin
from admin.views.fund import FundAdmin
from admin.views.payment import PaymentAdmin
from admin.views.project import ProjectAdmin
from admin.views.region import RegionAdmin
from admin.views.stage import StageAdmin
from admin.views.user import UserAdmin
from fastapi import FastAPI
from settings import settings
from sqladmin import Admin
from v1.dao.database import engine


def create_admin_panel(app: FastAPI):
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=MyAuthenticationBackend(secret_key=settings.SECRET_KEY),
        title="Садака app админка",
        logo_url="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
        debug=True,  # Enable debug mode for better error reporting
    )

    admin.add_view(CountryAdmin)
    admin.add_view(RegionAdmin)
    admin.add_view(CityAdmin)

    admin.add_view(UserAdmin)

    admin.add_view(FundAdmin)
    admin.add_view(ProjectAdmin)
    admin.add_view(StageAdmin)
    admin.add_view(FileAdmin)

    admin.add_view(PaymentAdmin)
