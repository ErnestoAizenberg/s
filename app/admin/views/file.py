from admin.views.base_classes.image_as_field_upload import FileModelPictureUploadField
from models.file import File


class FileAdmin(FileModelPictureUploadField, model=File):
    # TODO у файла поля отображаются только заполненные все сотальные скрывать
    # TODO тк привязка напрмиер только к юзеру а все остальное ненужно видеть в таком случае

    icon = "fa-solid fa-file-alt"
    name = "Файл"
    name_plural = "Файлы"
