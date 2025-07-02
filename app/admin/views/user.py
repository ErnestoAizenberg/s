from admin.views.auth_permissions import SuperAdminPerm
from admin.views.base_classes.image_as_file_singular_preview import AdminPicturePreview
from models.user import User


class UserAdmin(AdminPicturePreview, SuperAdminPerm, model=User):
    name_plural = "Пользователи"
    name = "Пользователь"

    icon = "fa-solid fa-user"
    column_searchable_list = [User.name, User.email]
    column_sortable_list = [User.id, User.name, User.email]
    column_labels = {
        User.id: "ID",
        User.name: "Имя",
        User.email: "Email",
        User.language: "Язык",
    }

    form_excluded_columns = [
        "payments",
    ]  # because sqladmin error for relations
