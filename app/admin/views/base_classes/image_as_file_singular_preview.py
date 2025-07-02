from markupsafe import Markup
from sqladmin import ModelView


class BaseAdminView(ModelView):
    form_excluded_columns = ["created_at", "updated_at"]
    column_list = ["id", "name"]


class AdminPicturePreview(BaseAdminView):
    column_list = ["id", "name", "picture_url"]
    form_excluded_columns = ["created_at", "updated_at", "upload"]

    column_details_list = ["picture_url"]

    @staticmethod
    def _picture_preview(model, name):
        url = getattr(model, "picture_url")
        if url:
            return Markup(f'<img src="{url}" width="50" height="50" style="object-fit:cover;border-radius:40px;" />')
        return "—"

    column_formatters = {
        "picture_url": _picture_preview,
    }

    column_formatters_list = column_formatters
    column_formatters_detail = column_formatters

    column_labels = {
        "picture_url": "Превью",
    }
