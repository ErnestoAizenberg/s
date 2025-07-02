from admin.views.auth_permissions import SuperAdminPerm
from admin.views.base_classes.image_as_file_singular_preview import BaseAdminView
from models.country import Country


class CountryAdmin(BaseAdminView, SuperAdminPerm, model=Country):
    icon = "fa-solid fa-globe"
    name = "Страна"
    name_plural = "Страны"
