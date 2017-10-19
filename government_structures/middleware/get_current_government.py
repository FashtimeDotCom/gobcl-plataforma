from django.utils.deprecation import MiddlewareMixin

from government_structures.models import GovernmentStructure


class GovernmentSetter(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.government_structure = GovernmentStructure.objects.get_or_none(
            current_government=True)
