from admin.views.auth_permissions import FundAdminAccess
from admin.views.base_classes.image_as_file_multiple_preview import MultipleFilesPreviewAdmin
from models.project import Project


class ProjectAdmin(MultipleFilesPreviewAdmin, FundAdminAccess, model=Project):
    column_list = ["name", "status", "documents_preview", "pictures_preview"]
    icon = "fa-solid fa-diagram-project"
    name = "Проект"
    name_plural = "Проекты"

    form_excluded_columns = ["payments", "stages"]  # because sqladmin error for relations
    column_searchable_list = [Project.fund_id]
