from admin.views.auth_permissions import SuperAdminPerm
from admin.views.base_classes.image_as_file_singular_preview import AdminPicturePreview
from models.fund import Fund


class FundAdmin(SuperAdminPerm, AdminPicturePreview, model=Fund):
    icon = "fa-solid fa-hand-holding-heart"
    name = "Фонд"
    name_plural = "Фонды"

    form_excluded_columns = [
        "projects",
    ]  # because sqladmin error for relations
