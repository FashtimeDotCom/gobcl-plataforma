from django.utils.deprecation import MiddlewareMixin

from governments.models import Government


class GovernmentSetter(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.government = Government.objects.get_or_none(
            current_government=True)
