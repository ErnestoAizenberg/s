from admin.views.base_classes.image_as_file_singular_preview import BaseAdminView
from markupsafe import Markup


class MultipleFilesPreviewAdmin(BaseAdminView):
    column_list = ["id", "documents_preview", "pictures_preview"]
    form_excluded_columns = [
        "documents",
        "pictures",
    ]

    column_labels = {
        "documents_preview": "Документы",
        "pictures_preview": "Изображения",
    }

    @staticmethod
    def _render_preview_list(items: list, label: str) -> str:
        if not items:
            return "—"

        previews = []
        for item in items:
            url = getattr(item, "url", None)
            if url:
                previews.append(
                    f'<img src="{url}" width="60" height="60" '
                    'style="object-fit:cover; margin-right:4px; border-radius:6px;" />'
                )
        return Markup("".join(previews)) if previews else "—"

    @staticmethod
    def _documents_preview(model, name):
        return MultipleFilesPreviewAdmin._render_preview_list(getattr(model, "documents", []), "Документы")

    @staticmethod
    def _pictures_preview(model, name):
        return MultipleFilesPreviewAdmin._render_preview_list(getattr(model, "pictures", []), "Изображения")

    column_formatters = {
        "documents_preview": _documents_preview,
        "pictures_preview": _pictures_preview,
    }

    column_formatters_list = column_formatters
    column_formatters_detail = column_formatters
