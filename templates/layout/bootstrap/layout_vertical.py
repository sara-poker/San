from django.conf import settings
import copy

from ..bootstrap.menu_dict import menu_user, menu_manager, menu_admin

from web_project.template_helpers.theme import TemplateHelper

API_BASE = settings.BASE_URL


"""
This is an entry and Bootstrap class for the theme level.
The init() function will be called in web_project/__init__.py
"""


class TemplateBootstrapLayoutVertical:
    def init(context):
        context.update(
            {
                "layout": "vertical",
                "content_navbar": True,
                "is_navbar": True,
                "is_menu": True,
                "is_footer": True,
                "navbar_detached": True,
            }
        )

        # map_context according to updated context values
        TemplateHelper.map_context(context)

        TemplateBootstrapLayoutVertical.init_menu_data(context)

        return context

    def init_menu_data(context):
        # Load the menu data from the JSON
        view = context.get('view')
        request = getattr(view, 'request', None)

        user = request.user if request else None

        if user and user.is_authenticated:
            if user.role == "manager":
                selected_menu = menu_manager
            elif user.role == "admin":
                selected_menu = menu_admin
            else:
                selected_menu = menu_user
        else:
            selected_menu = menu_user

        menu_data = copy.deepcopy(selected_menu)

        # Updated context with menu_data
        context.update({"menu_data": menu_data})
