from django.contrib.admin import TabularInline

from journey_map.mixins.admin.permission import InlinePermissionControlMixin


class BaseTabularInline(
    InlinePermissionControlMixin, TabularInline
):
    """Base tabular inline admin interface with common functionality for all
    inlines.

    This class serves as the foundation for all inlines. Any tabular inline can inherit from this
    class to reuse its common functionality.

    """

    extra = 0
    show_change_link = True
