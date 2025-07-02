from admin.views.auth_permissions import FundAdminAccess
from admin.views.base_classes.image_as_file_singular_preview import BaseAdminView
from models.project import Stage


class StageAdmin(BaseAdminView, FundAdminAccess, model=Stage):
    column_list = [Stage.id, Stage.name]
    icon = "fa-solid fa-layer-group"
    name = "Этап"
    name_plural = "Этапы"

    form_excluded_columns = [
        "payments",
    ]  # because sqladmin error for relations

    column_searchable_list = [Stage.project_id]
