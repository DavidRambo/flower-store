import os

from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField

# for event listener to delete thumbnail
# from flask_admin.form import thumbgen_filename

# from flask_admin.form import SecureForm
from flask_login import current_user

from flower_store.utils import image_rename


IMAGE_PATH = os.path.join(os.path.dirname(__file__), "static/flower_imgs")


class FlowerView(ModelView):
    # form_base_class = SecureForm()
    create_modal = True
    edit_modal = True

    form_extra_fields = {
        "image_file": ImageUploadField(
            "Image",
            base_path=IMAGE_PATH,
            namegen=image_rename,
            # thumbnail_size=(125, 125, True),
            max_size=(500, 500, True),
        )
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name):
        return redirect(url_for("login"))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
