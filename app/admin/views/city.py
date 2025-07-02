from admin.views.auth_permissions import SuperAdminPerm
from admin.views.base_classes.image_as_file_singular_preview import BaseAdminView
from models.city import City


class CityAdmin(BaseAdminView, SuperAdminPerm, model=City):
    icon = "fa-solid fa-city"
    name = "Город"
    name_plural = "Города"
